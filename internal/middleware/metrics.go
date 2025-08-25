// Metrics middleware for monitoring and observability
// Created: January 31, 2025
// Purpose: Track API usage to ensure community needs are met

package middleware

import (
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	// HTTP request metrics
	httpRequestsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "resilience_api_http_requests_total",
			Help: "Total number of HTTP requests processed",
		},
		[]string{"method", "path", "status_code", "community_focused"},
	)
	
	httpRequestDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "resilience_api_http_request_duration_seconds",
			Help:    "HTTP request duration in seconds",
			Buckets: []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10},
		},
		[]string{"method", "path", "status_code"},
	)
	
	// Community-focused metrics
	communitySearches = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "resilience_api_community_searches_total",
			Help: "Total number of community searches performed",
		},
		[]string{"search_type"},
	)
	
	communityStoryViews = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "resilience_api_story_views_total", 
			Help: "Total number of community story views",
		},
		[]string{"community_id", "story_type"},
	)
	
	dataDownloads = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "resilience_api_data_downloads_total",
			Help: "Total number of data downloads",
		},
		[]string{"data_type", "user_type"},
	)
	
	communityContacts = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "resilience_api_community_contacts_total",
			Help: "Total number of community contact requests",
		},
		[]string{"contact_type"},
	)
	
	// Performance metrics
	slowRequests = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "resilience_api_slow_requests_total",
			Help: "Requests that took longer than 3 seconds (community internet consideration)",
		},
		[]string{"path", "duration_bucket"},
	)
	
	// Error metrics
	apiErrors = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "resilience_api_errors_total",
			Help: "Total number of API errors",
		},
		[]string{"error_type", "path", "status_code"},
	)
)

// Metrics returns a middleware that collects Prometheus metrics
func Metrics() gin.HandlerFunc {
	return func(c *gin.Context) {
		startTime := time.Now()
		path := c.Request.URL.Path
		method := c.Request.Method
		
		c.Next()
		
		duration := time.Since(startTime)
		statusCode := c.Writer.Status()
		statusCodeStr := strconv.Itoa(statusCode)
		
		// Normalize path for metrics (remove dynamic segments)
		normalizedPath := normalizePath(path)
		
		// Track basic HTTP metrics
		isCommunityFocused := isCommunityPath(path)
		httpRequestsTotal.WithLabelValues(
			method, 
			normalizedPath, 
			statusCodeStr,
			strconv.FormatBool(isCommunityFocused),
		).Inc()
		
		httpRequestDuration.WithLabelValues(
			method,
			normalizedPath, 
			statusCodeStr,
		).Observe(duration.Seconds())
		
		// Track slow requests (important for community members with slow internet)
		if duration > 3*time.Second {
			bucket := getPerformanceBucket(duration)
			slowRequests.WithLabelValues(normalizedPath, bucket).Inc()
		}
		
		// Track errors
		if statusCode >= 400 {
			errorType := getErrorType(statusCode)
			apiErrors.WithLabelValues(errorType, normalizedPath, statusCodeStr).Inc()
		}
		
		// Track community-specific metrics
		trackCommunityMetrics(c, path, method)
	}
}

// normalizePath removes dynamic segments from paths for consistent metrics
func normalizePath(path string) string {
	// Common path normalizations
	normalizations := map[string]string{
		"/communities/": "/communities/:id",
		"/stories/":     "/stories/:id",
		"/research/":    "/research/:type",
		"/policy/":      "/policy/:type",
		"/users/":       "/users/:id",
	}
	
	// Check for patterns
	for pattern, normalized := range normalizations {
		if len(path) >= len(pattern) && path[:len(pattern)] == pattern {
			return normalized
		}
	}
	
	return path
}

// getPerformanceBucket categorizes request duration for performance tracking
func getPerformanceBucket(duration time.Duration) string {
	switch {
	case duration < 5*time.Second:
		return "slow"
	case duration < 10*time.Second:
		return "very_slow"
	default:
		return "extremely_slow"
	}
}

// getErrorType categorizes HTTP status codes
func getErrorType(statusCode int) string {
	switch {
	case statusCode >= 500:
		return "server_error"
	case statusCode == 429:
		return "rate_limit"
	case statusCode == 404:
		return "not_found"
	case statusCode == 403:
		return "forbidden"
	case statusCode == 401:
		return "unauthorized"
	case statusCode >= 400:
		return "client_error"
	default:
		return "unknown"
	}
}

// trackCommunityMetrics tracks metrics specific to community interactions
func trackCommunityMetrics(c *gin.Context, path, method string) {
	// Track searches
	if path == "/search" || path == "/api/v1/search" {
		searchType := c.Query("type")
		if searchType == "" {
			searchType = "general"
		}
		communitySearches.WithLabelValues(searchType).Inc()
	}
	
	// Track story views
	if method == "GET" && contains(path, "/stories/") {
		communityID := c.Param("community_id")
		if communityID == "" {
			communityID = "unknown"
		}
		storyType := c.Query("type")
		if storyType == "" {
			storyType = "general"
		}
		communityStoryViews.WithLabelValues(communityID, storyType).Inc()
	}
	
	// Track data downloads
	if contains(path, "/download") {
		dataType := c.Query("type")
		if dataType == "" {
			dataType = "general"
		}
		userType := getUserType(c)
		dataDownloads.WithLabelValues(dataType, userType).Inc()
	}
	
	// Track community contacts
	if method == "POST" && contains(path, "/contact") {
		contactType := c.PostForm("type")
		if contactType == "" {
			contactType = "general"
		}
		communityContacts.WithLabelValues(contactType).Inc()
	}
}

// getUserType attempts to determine user type from request context
func getUserType(c *gin.Context) string {
	// Check for user type in JWT token or headers
	userType := c.GetHeader("X-User-Type")
	if userType != "" {
		return userType
	}
	
	// Check for user agent patterns
	userAgent := c.GetHeader("User-Agent")
	if contains(userAgent, "research") || contains(userAgent, "academic") {
		return "researcher"
	}
	
	if contains(userAgent, "mobile") {
		return "mobile_user"
	}
	
	return "general"
}

// Community impact tracking
func TrackCommunityImpact() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Add community impact headers
		c.Header("X-Communities-Impacted", "1059")
		c.Header("X-Stories-Shared", "500+")
		c.Header("X-Researchers-Served", "100+")
		c.Header("X-Policies-Influenced", "25+")
		
		c.Next()
	}
}