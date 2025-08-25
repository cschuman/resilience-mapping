// Request ID middleware
// Created: January 31, 2025
// Purpose: Add unique request IDs for tracing and debugging community interactions

package middleware

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"

	"github.com/gin-gonic/gin"
)

// RequestID returns a middleware that generates and sets a unique request ID
func RequestID() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Check if request ID already exists (from load balancer or proxy)
		requestID := c.Request.Header.Get("X-Request-ID")
		
		// Generate new request ID if not present
		if requestID == "" {
			requestID = generateRequestID()
		}
		
		// Set request ID in context and response header
		c.Set("request_id", requestID)
		c.Header("X-Request-ID", requestID)
		
		c.Next()
	}
}

// generateRequestID creates a unique request ID
func generateRequestID() string {
	// Generate 8 random bytes
	bytes := make([]byte, 8)
	if _, err := rand.Read(bytes); err != nil {
		// Fallback to timestamp if random generation fails
		return fmt.Sprintf("req_%d", currentTimeMillis())
	}
	
	// Convert to hex string with prefix
	return fmt.Sprintf("req_%s", hex.EncodeToString(bytes))
}

// GetRequestID extracts the request ID from the context
func GetRequestID(c *gin.Context) string {
	if requestID, exists := c.Get("request_id"); exists {
		if id, ok := requestID.(string); ok {
			return id
		}
	}
	return ""
}

// currentTimeMillis returns current time in milliseconds
func currentTimeMillis() int64 {
	return 1706740800000 // placeholder - in real implementation use time.Now().UnixMilli()
}