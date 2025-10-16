// Community-first middleware
// Created: January 31, 2025
// Purpose: Remind developers about community-first principles during development

package middleware

import (
	"math/rand"
	"time"

	"github.com/gin-gonic/gin"
)

// CommunityFirst returns a middleware that adds community-first reminders (development only)
func CommunityFirst() gin.HandlerFunc {
	// Community-focused messages to remind developers
	messages := []string{
		"Remember: This API serves real communities with real families",
		"Every endpoint should preserve community dignity",
		"Ask: Would this help Maria find resources for her clients?",
		"Community approval required before shipping any feature",
		"Building for 1,000+ communities with love and respect",
		"No deficit language - communities are resilient, not struggling",
		"Accessibility is not optional - everyone deserves access",
		"Community data belongs to communities, we are stewards",
		"Beautiful design is a form of respect for communities",
		"Test with actual community members, not just personas",
		"Performance matters - many communities have slow internet",
		"Privacy first - protect community members always",
		"Think mobile-first - many users only have phones",
		"Every feature should empower communities, not extract from them",
	}
	
	// Seed random number generator
	rand.Seed(time.Now().UnixNano())
	
	return func(c *gin.Context) {
		// Only run in development mode
		if gin.Mode() != gin.DebugMode {
			c.Next()
			return
		}
		
		// Add community reminder header (10% chance to avoid spam)
		if rand.Intn(10) == 0 {
			message := messages[rand.Intn(len(messages))]
			c.Header("X-Community-Reminder", message)
		}
		
		// Add community stats header
		c.Header("X-Communities-Served", "1059 resilient communities mapped")
		c.Header("X-Our-Mission", "Technology that serves communities with dignity")
		
		c.Next()
	}
}

// CommunityContext adds community-related context to requests
func CommunityContext() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Add community context to request
		c.Set("communities_served", 1059)
		c.Set("mission", "dignity_first_technology")
		c.Set("built_for", "Maria, Dr. James, Sarah, Keisha, Miguel")
		
		c.Next()
	}
}

// CommunityMetrics tracks community-focused metrics
func CommunityMetrics() gin.HandlerFunc {
	return func(c *gin.Context) {
		startTime := time.Now()
		
		c.Next()
		
		// Log community-focused metrics
		duration := time.Since(startTime)
		path := c.Request.URL.Path
		
		// Log slow requests (community members might have slow internet)
		if duration > 3*time.Second {
			// In real implementation, log to monitoring system
			c.Header("X-Performance-Warning", "Request took longer than 3s - consider optimization for community members")
		}
		
		// Add performance header for monitoring
		c.Header("X-Response-Time-Ms", duration.Milliseconds())
		
		// Track community-relevant paths
		if isCommunityPath(path) {
			c.Header("X-Community-Path", "true")
		}
	}
}

// isCommunityPath determines if a path is community-relevant
func isCommunityPath(path string) bool {
	communityPaths := []string{
		"/communities",
		"/stories", 
		"/search",
		"/contact",
		"/resources",
	}
	
	for _, cp := range communityPaths {
		if len(path) >= len(cp) && path[:len(cp)] == cp {
			return true
		}
	}
	
	return false
}