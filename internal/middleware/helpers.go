// Helper functions for middleware
// Created: January 31, 2025
// Purpose: Shared utilities for middleware functions

package middleware

import (
	"strings"
	"time"
)

// contains checks if a string contains a substring
func contains(s, substr string) bool {
	return strings.Contains(strings.ToLower(s), strings.ToLower(substr))
}

// currentTimeMillis returns current time in milliseconds
func currentTimeMillis() int64 {
	return time.Now().UnixMilli()
}