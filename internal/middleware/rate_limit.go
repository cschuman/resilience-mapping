// Rate limiting middleware
// Created: January 31, 2025  
// Purpose: Protect API from abuse while allowing legitimate community access

package middleware

import (
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/example/resilience-mapping-go/internal/config"
)

// RateLimiter implements a token bucket rate limiter
type RateLimiter struct {
	visitors map[string]*visitor
	mutex    sync.RWMutex
	rate     int           // requests per minute
	burst    int           // burst size
	cleanup  time.Duration // cleanup interval
}

// visitor represents a client with their own token bucket
type visitor struct {
	limiter  *TokenBucket
	lastSeen time.Time
}

// TokenBucket implements a token bucket algorithm
type TokenBucket struct {
	tokens    int
	capacity  int
	rate      int
	lastRefill time.Time
	mutex     sync.Mutex
}

// NewTokenBucket creates a new token bucket
func NewTokenBucket(capacity, rate int) *TokenBucket {
	return &TokenBucket{
		tokens:     capacity,
		capacity:   capacity,
		rate:       rate,
		lastRefill: time.Now(),
	}
}

// Allow checks if a request is allowed and consumes a token
func (tb *TokenBucket) Allow() bool {
	tb.mutex.Lock()
	defer tb.mutex.Unlock()
	
	now := time.Now()
	elapsed := now.Sub(tb.lastRefill)
	
	// Refill tokens based on elapsed time
	tokensToAdd := int(elapsed.Minutes() * float64(tb.rate))
	if tokensToAdd > 0 {
		tb.tokens = min(tb.capacity, tb.tokens+tokensToAdd)
		tb.lastRefill = now
	}
	
	// Check if we have tokens available
	if tb.tokens > 0 {
		tb.tokens--
		return true
	}
	
	return false
}

// RateLimit returns a rate limiting middleware
func RateLimit(cfg config.RateLimitConfig) gin.HandlerFunc {
	limiter := &RateLimiter{
		visitors: make(map[string]*visitor),
		rate:     cfg.RequestsPerMinute,
		burst:    cfg.BurstSize,
		cleanup:  cfg.CleanupInterval,
	}
	
	// Start cleanup goroutine
	go limiter.cleanupVisitors()
	
	return func(c *gin.Context) {
		// Get client IP
		clientIP := getClientIP(c)
		
		// Get or create visitor
		v := limiter.getVisitor(clientIP)
		
		// Check if request is allowed
		if !v.limiter.Allow() {
			c.JSON(http.StatusTooManyRequests, gin.H{
				"error": "Rate limit exceeded",
				"message": "Too many requests. Please try again later.",
				"community_note": "We protect our community data by limiting request rates. Thank you for understanding.",
				"retry_after": 60,
			})
			c.Abort()
			return
		}
		
		// Add rate limit headers
		c.Header("X-RateLimit-Limit", fmt.Sprintf("%d", cfg.RequestsPerMinute))
		c.Header("X-RateLimit-Remaining", fmt.Sprintf("%d", v.limiter.tokens))
		c.Header("X-RateLimit-Reset", fmt.Sprintf("%d", time.Now().Add(time.Minute).Unix()))
		
		c.Next()
	}
}

// getVisitor gets or creates a visitor for the given IP
func (rl *RateLimiter) getVisitor(ip string) *visitor {
	rl.mutex.Lock()
	defer rl.mutex.Unlock()
	
	v, exists := rl.visitors[ip]
	if !exists {
		v = &visitor{
			limiter: NewTokenBucket(rl.burst, rl.rate),
		}
		rl.visitors[ip] = v
	}
	
	v.lastSeen = time.Now()
	return v
}

// cleanupVisitors removes old visitors to prevent memory leaks
func (rl *RateLimiter) cleanupVisitors() {
	ticker := time.NewTicker(rl.cleanup)
	defer ticker.Stop()
	
	for {
		select {
		case <-ticker.C:
			rl.mutex.Lock()
			for ip, v := range rl.visitors {
				// Remove visitors not seen for 10 minutes
				if time.Since(v.lastSeen) > 10*time.Minute {
					delete(rl.visitors, ip)
				}
			}
			rl.mutex.Unlock()
		}
	}
}

// getClientIP extracts the client IP from the request
func getClientIP(c *gin.Context) string {
	// Check for forwarded IP first (load balancers, proxies)
	forwarded := c.Request.Header.Get("X-Forwarded-For")
	if forwarded != "" {
		// Take the first IP in the list
		return forwarded[:min(len(forwarded), 15)]
	}
	
	// Check for real IP header
	realIP := c.Request.Header.Get("X-Real-IP")
	if realIP != "" {
		return realIP
	}
	
	// Fall back to remote address
	return c.ClientIP()
}

// PathBasedRateLimit returns a rate limiter that applies different limits based on path
func PathBasedRateLimit(cfg config.RateLimitConfig) gin.HandlerFunc {
	return func(c *gin.Context) {
		path := c.Request.URL.Path
		
		// Different limits for different endpoints
		var limit int
		switch {
		case contains(path, "/search"):
			limit = cfg.SearchLimit
		case contains(path, "/download"):
			limit = cfg.DownloadLimit
		case contains(path, "/contact"):
			limit = cfg.ContactLimit
		default:
			limit = cfg.RequestsPerMinute
		}
		
		// Create temporary config with path-specific limit
		pathCfg := cfg
		pathCfg.RequestsPerMinute = limit
		
		// Apply rate limiting with path-specific config
		RateLimit(pathCfg)(c)
	}
}

// Helper functions
func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func contains(s, substr string) bool {
	return len(s) >= len(substr) && s[:len(substr)] == substr
}