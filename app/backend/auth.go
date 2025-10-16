// Authentication middleware
// Created: January 31, 2025
// Purpose: Handle authentication and authorization for community-first platform

package middleware

import (
	"net/http"
	"strings"
	"log"

	"github.com/gin-gonic/gin"
	"github.com/your-org/resilience-mapping/pkg/auth"
	"github.com/your-org/resilience-mapping/internal/config"
)

// AuthMiddleware provides JWT authentication functionality
type AuthMiddleware struct {
	jwtManager *auth.JWTManager
}

// NewAuthMiddleware creates a new authentication middleware
func NewAuthMiddleware(cfg *config.JWTConfig) *AuthMiddleware {
	return &AuthMiddleware{
		jwtManager: auth.NewJWTManager(cfg.Secret, cfg.Issuer),
	}
}

// RequireAuth validates JWT token and sets user context
func (a *AuthMiddleware) RequireAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "Authorization header required",
				"message": "Please log in to access this feature",
				"community_message": "You need to be logged in to access this feature",
			})
			c.Abort()
			return
		}

		// Extract token from "Bearer <token>"
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == authHeader {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "Invalid authorization format",
				"message": "Please use Bearer token format",
				"community_message": "Login format is incorrect, please try logging in again",
			})
			c.Abort()
			return
		}

		// Validate JWT token
		claims, err := a.jwtManager.ValidateToken(tokenString)
		if err != nil {
			log.Printf("🔒 Authentication failed: %v", err)
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "Invalid or expired token",
				"message": "Please log in again",
				"community_message": "Your login session has expired, please log in again",
			})
			c.Abort()
			return
		}

		// Set user context for downstream handlers
		c.Set("user_id", claims.UserID)
		c.Set("user_email", claims.Email)
		c.Set("user_role", claims.Role)
		c.Set("user_type", claims.UserType)
		if claims.CommunityID != nil {
			c.Set("community_id", *claims.CommunityID)
		}
		c.Set("jwt_claims", claims)

		// Log authentication success (without sensitive data)
		log.Printf("🔓 User authenticated: ID=%d, Role=%s, Type=%s", 
			claims.UserID, claims.Role, claims.UserType)

		c.Next()
	}
}

// RequireRole checks if user has required role
func RequireRole(requiredRole string) gin.HandlerFunc {
	return func(c *gin.Context) {
		userRole, exists := c.Get("user_role")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "User role not found",
				"message": "Please log in again",
				"community_message": "We couldn't verify your permissions, please log in again",
			})
			c.Abort()
			return
		}

		// Admin role can access everything
		if userRole == "admin" {
			c.Next()
			return
		}

		// Check specific role requirement
		if userRole != requiredRole {
			c.JSON(http.StatusForbidden, gin.H{
				"error": "Insufficient permissions",
				"message": "This feature requires additional verification",
				"required_role": requiredRole,
				"community_message": "This feature requires additional permissions. Please contact our team if you believe this is an error.",
			})
			c.Abort()
			return
		}

		c.Next()
	}
}

// RequireUserType checks if user has required user type
func RequireUserType(requiredType string) gin.HandlerFunc {
	return func(c *gin.Context) {
		userType, exists := c.Get("user_type")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "User type not found",
				"message": "Please log in again",
			})
			c.Abort()
			return
		}

		// Admin can access everything
		userRole, _ := c.Get("user_role")
		if userRole == "admin" {
			c.Next()
			return
		}

		// Check specific type requirement
		if userType != requiredType {
			c.JSON(http.StatusForbidden, gin.H{
				"error": "Access restricted",
				"message": "This feature is restricted to specific user types",
				"required_type": requiredType,
				"community_message": "This feature is available to specific user groups. Please contact support if you need access.",
			})
			c.Abort()
			return
		}

		c.Next()
	}
}

// RequireCommunityMember checks if user is a member of specific community
func RequireCommunityMember(communityID int) gin.HandlerFunc {
	return func(c *gin.Context) {
		claims, exists := c.Get("jwt_claims")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "Authentication required",
				"message": "Please log in to access community features",
			})
			c.Abort()
			return
		}

		jwtClaims, ok := claims.(*auth.Claims)
		if !ok {
			c.JSON(http.StatusInternalServerError, gin.H{
				"error": "Invalid authentication data",
			})
			c.Abort()
			return
		}

		// Admin can access all communities
		if jwtClaims.HasRole("admin") {
			c.Next()
			return
		}

		// Check community membership
		if !jwtClaims.IsCommunityMember(communityID) {
			c.JSON(http.StatusForbidden, gin.H{
				"error": "Community access required",
				"message": "You must be a member of this community to access this feature",
				"community_message": "This feature is only available to community members",
			})
			c.Abort()
			return
		}

		c.Next()
	}
}

// OptionalAuth validates JWT token if present but doesn't require it
func (a *AuthMiddleware) OptionalAuth() gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			// No auth header provided, continue without authentication
			c.Next()
			return
		}

		// Extract token from "Bearer <token>"
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == authHeader {
			// Invalid format, but continue without authentication
			c.Next()
			return
		}

		// Try to validate JWT token
		claims, err := a.jwtManager.ValidateToken(tokenString)
		if err != nil {
			// Invalid token, but continue without authentication
			log.Printf("🔒 Optional authentication failed: %v", err)
			c.Next()
			return
		}

		// Set user context for downstream handlers
		c.Set("user_id", claims.UserID)
		c.Set("user_email", claims.Email)
		c.Set("user_role", claims.Role)
		c.Set("user_type", claims.UserType)
		if claims.CommunityID != nil {
			c.Set("community_id", *claims.CommunityID)
		}
		c.Set("jwt_claims", claims)
		c.Set("authenticated", true)

		c.Next()
	}
}

// ValidateWebhook validates webhook signatures
func ValidateWebhook() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Get webhook signature from header
		signature := c.GetHeader("X-Hub-Signature-256")
		if signature == "" {
			c.JSON(http.StatusUnauthorized, gin.H{
				"error": "Missing webhook signature",
			})
			c.Abort()
			return
		}

		// TODO: Implement proper webhook signature validation
		// This would involve:
		// 1. Reading the webhook secret from environment/config
		// 2. Computing HMAC of request body
		// 3. Comparing with provided signature
		
		// For now, just log and continue
		log.Printf("🔗 Webhook received with signature: %s", signature)
		
		c.Next()
	}
}

// Global middleware functions (for backward compatibility)

// RequireAuth is a global function that creates auth middleware
func RequireAuth() gin.HandlerFunc {
	// This will need to be updated when we have access to config
	// For now, return a placeholder
	return func(c *gin.Context) {
		c.JSON(http.StatusNotImplemented, gin.H{
			"error": "Authentication not fully implemented",
			"message": "Please initialize auth middleware properly",
		})
		c.Abort()
	}
}

// Helper functions

// GetUserID extracts user ID from context
func GetUserID(c *gin.Context) (int, bool) {
	if userID, exists := c.Get("user_id"); exists {
		if id, ok := userID.(int); ok {
			return id, true
		}
	}
	return 0, false
}

// GetUserRole extracts user role from context
func GetUserRole(c *gin.Context) (string, bool) {
	if role, exists := c.Get("user_role"); exists {
		if roleStr, ok := role.(string); ok {
			return roleStr, true
		}
	}
	return "", false
}

// GetClaims extracts JWT claims from context
func GetClaims(c *gin.Context) (*auth.Claims, bool) {
	if claims, exists := c.Get("jwt_claims"); exists {
		if jwtClaims, ok := claims.(*auth.Claims); ok {
			return jwtClaims, true
		}
	}
	return nil, false
}

// IsAuthenticated checks if request is authenticated
func IsAuthenticated(c *gin.Context) bool {
	if auth, exists := c.Get("authenticated"); exists {
		if isAuth, ok := auth.(bool); ok {
			return isAuth
		}
	}
	// Also check if user_id exists (from RequireAuth)
	_, hasUserID := GetUserID(c)
	return hasUserID
}