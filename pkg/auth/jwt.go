// JWT authentication utilities
// Created: January 31, 2025
// Purpose: Handle JWT tokens for secure authentication

package auth

import (
	"errors"
	"time"
	
	"github.com/golang-jwt/jwt/v5"
)

// Claims represents JWT claims with community-specific data
type Claims struct {
	UserID      int    `json:"user_id"`
	Email       string `json:"email"`
	UserType    string `json:"user_type"`
	Role        string `json:"role"`
	CommunityID *int   `json:"community_id,omitempty"`
	jwt.RegisteredClaims
}

// JWTManager handles JWT operations
type JWTManager struct {
	secretKey string
	issuer    string
}

// NewJWTManager creates a new JWT manager
func NewJWTManager(secretKey, issuer string) *JWTManager {
	return &JWTManager{
		secretKey: secretKey,
		issuer:    issuer,
	}
}

// GenerateToken creates a new JWT token
func (m *JWTManager) GenerateToken(userID int, email, userType, role string, communityID *int, duration time.Duration) (string, error) {
	claims := &Claims{
		UserID:      userID,
		Email:       email,
		UserType:    userType,
		Role:        role,
		CommunityID: communityID,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(duration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			NotBefore: jwt.NewNumericDate(time.Now()),
			Issuer:    m.issuer,
			Subject:   email,
			ID:        generateTokenID(),
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(m.secretKey))
}

// ValidateToken validates and parses a JWT token
func (m *JWTManager) ValidateToken(tokenString string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (interface{}, error) {
		return []byte(m.secretKey), nil
	})

	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(*Claims)
	if !ok || !token.Valid {
		return nil, errors.New("invalid token")
	}

	return claims, nil
}

// RefreshToken creates a new token from an existing valid token
func (m *JWTManager) RefreshToken(tokenString string, duration time.Duration) (string, error) {
	claims, err := m.ValidateToken(tokenString)
	if err != nil {
		return "", err
	}

	// Create new token with extended expiration
	return m.GenerateToken(
		claims.UserID,
		claims.Email,
		claims.UserType,
		claims.Role,
		claims.CommunityID,
		duration,
	)
}

// ExtractClaims extracts claims from token without full validation (for expired tokens)
func (m *JWTManager) ExtractClaims(tokenString string) (*Claims, error) {
	token, _, err := jwt.NewParser().ParseUnverified(tokenString, &Claims{})
	if err != nil {
		return nil, err
	}

	claims, ok := token.Claims.(*Claims)
	if !ok {
		return nil, errors.New("invalid token claims")
	}

	return claims, nil
}

// Helper function to generate unique token IDs
func generateTokenID() string {
	return time.Now().Format("20060102150405") + "-" + generateRandomString(8)
}

// generateRandomString creates a random string of specified length
func generateRandomString(length int) string {
	const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	b := make([]byte, length)
	for i := range b {
		b[i] = charset[time.Now().UnixNano()%int64(len(charset))]
	}
	return string(b)
}

// TokenInfo provides information about a token
type TokenInfo struct {
	Valid       bool      `json:"valid"`
	UserID      int       `json:"user_id,omitempty"`
	Email       string    `json:"email,omitempty"`
	UserType    string    `json:"user_type,omitempty"`
	Role        string    `json:"role,omitempty"`
	CommunityID *int      `json:"community_id,omitempty"`
	IssuedAt    time.Time `json:"issued_at,omitempty"`
	ExpiresAt   time.Time `json:"expires_at,omitempty"`
	Error       string    `json:"error,omitempty"`
}

// GetTokenInfo returns detailed information about a token
func (m *JWTManager) GetTokenInfo(tokenString string) TokenInfo {
	claims, err := m.ValidateToken(tokenString)
	if err != nil {
		return TokenInfo{
			Valid: false,
			Error: err.Error(),
		}
	}

	info := TokenInfo{
		Valid:       true,
		UserID:      claims.UserID,
		Email:       claims.Email,
		UserType:    claims.UserType,
		Role:        claims.Role,
		CommunityID: claims.CommunityID,
	}

	if claims.IssuedAt != nil {
		info.IssuedAt = claims.IssuedAt.Time
	}

	if claims.ExpiresAt != nil {
		info.ExpiresAt = claims.ExpiresAt.Time
	}

	return info
}

// HasRole checks if claims have a specific role
func (c *Claims) HasRole(role string) bool {
	return c.Role == role || c.Role == "admin"
}

// IsCommunityMember checks if user is a member of a specific community
func (c *Claims) IsCommunityMember(communityID int) bool {
	return c.CommunityID != nil && *c.CommunityID == communityID
}

// CanAccessCommunity checks if user can access community data
func (c *Claims) CanAccessCommunity(communityID int, isPublic bool) bool {
	// Public communities are accessible to all authenticated users
	if isPublic {
		return true
	}
	
	// Private communities require membership or admin role
	return c.HasRole("admin") || c.IsCommunityMember(communityID)
}