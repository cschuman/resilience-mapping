// Security middleware for HTTP security headers
// Created: January 31, 2025
// Purpose: Implement security best practices to protect community data

package middleware

import (
	"github.com/gin-gonic/gin"
)

// SecurityHeaders returns a middleware that sets security-related HTTP headers
func SecurityHeaders() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Prevent MIME type sniffing
		c.Header("X-Content-Type-Options", "nosniff")
		
		// Enable XSS filtering
		c.Header("X-XSS-Protection", "1; mode=block")
		
		// Prevent clickjacking
		c.Header("X-Frame-Options", "DENY")
		
		// Strict Transport Security (HTTPS only in production)
		if gin.Mode() == gin.ReleaseMode {
			c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload")
		}
		
		// Referrer Policy - protect community privacy
		c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
		
		// Content Security Policy - basic policy for API responses
		c.Header("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'")
		
		// Permissions Policy - restrict access to sensitive features
		c.Header("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
		
		// Server header - don't reveal server information
		c.Header("Server", "Health Resilience Mapping API")
		
		// Remove powered-by header if present
		c.Header("X-Powered-By", "")
		
		// Community data protection reminder in development
		if gin.Mode() == gin.DebugMode {
			c.Header("X-Community-Protection", "This API serves real community data with dignity and respect")
		}
		
		c.Next()
	}
}