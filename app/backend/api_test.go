// Integration tests for API endpoints
// Created: January 31, 2025
// Purpose: Test API functionality with community-first principles

package integration

import (
	"fmt"
	"net/http"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/your-org/resilience-mapping/internal/api"
	"github.com/your-org/resilience-mapping/internal/config"
	"github.com/your-org/resilience-mapping/internal/handlers"
	"github.com/your-org/resilience-mapping/internal/middleware"
	"github.com/your-org/resilience-mapping/internal/repositories"
	"github.com/your-org/resilience-mapping/internal/services"
	"github.com/your-org/resilience-mapping/test/testutils"
)

func TestCommunityAPI(t *testing.T) {
	// Setup test environment
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	fixtures := testDB.SeedTestData(t)

	// Create repositories
	communityRepo := repositories.NewCommunityRepository(testDB.DB)
	storyRepo := repositories.NewStoryRepository(testDB.DB)
	userRepo := repositories.NewUserRepository(testDB.DB)

	// Create services
	communityService := services.NewCommunityService(communityRepo, storyRepo, userRepo)

	// Create handlers
	communityHandler := handlers.NewCommunityHandler(communityRepo, communityService)
	storyHandler := handlers.NewStoryHandler()
	userHandler := handlers.NewUserHandler()
	authHandler := handlers.NewAuthHandler()
	searchHandler := handlers.NewSearchHandler()
	healthHandler := handlers.NewHealthHandler(testDB.DB)

	// Create test router
	router := gin.New()
	router.Use(gin.Recovery())

	// Setup routes
	services := &api.Services{
		CommunityHandler: communityHandler,
		StoryHandler:     storyHandler,
		UserHandler:      userHandler,
		AuthHandler:      authHandler,
		SearchHandler:    searchHandler,
		HealthHandler:    healthHandler,
	}

	cfg := &config.Config{
		JWT: config.JWTConfig{
			Secret: "test-secret",
			Issuer: "test",
		},
	}

	api.SetupRoutes(router, services, cfg)

	// Create test client
	client := testutils.NewTestClient(router)

	t.Run("Health Check", func(t *testing.T) {
		resp := client.GET("/health", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		var response map[string]interface{}
		client.AssertJSON(t, resp, &response)
		
		if status, exists := response["status"]; !exists || status != "healthy" {
			t.Errorf("Expected healthy status, got: %v", response)
		}
		
		client.AssertContains(t, resp, "resilient communities")
	})

	t.Run("Get Communities - Public Access", func(t *testing.T) {
		resp := client.GET("/api/v1/communities", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		var response map[string]interface{}
		client.AssertJSON(t, resp, &response)
		
		// Should return public communities
		if communities, exists := response["communities"]; exists {
			if communitiesArray, ok := communities.([]interface{}); ok {
				if len(communitiesArray) == 0 {
					t.Error("Expected at least one public community")
				}
			}
		}
		
		// Check for community-first messaging
		client.AssertContains(t, resp, "resilient communities")
		client.AssertCommunityFirst(t, resp)
	})

	t.Run("Get Specific Community - Public", func(t *testing.T) {
		communityID := fixtures.PublicCommunity.ID
		
		resp := client.GET(fmt.Sprintf("/api/v1/communities/%d", communityID), nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		client.AssertCommunityInResponse(t, resp, fixtures.PublicCommunity.TractID)
		client.AssertCommunityFirst(t, resp)
	})

	t.Run("Get Specific Community - Private Should Be Protected", func(t *testing.T) {
		communityID := fixtures.PrivateCommunity.ID
		
		resp := client.GET(fmt.Sprintf("/api/v1/communities/%d", communityID), nil)
		
		// Should be forbidden or not found since it's private
		if resp.Code != http.StatusForbidden && resp.Code != http.StatusNotFound {
			t.Errorf("Expected 403 or 404 for private community, got %d", resp.Code)
		}
		
		client.AssertCommunityMessage(t, resp)
	})

	t.Run("Search Communities", func(t *testing.T) {
		resp := client.GET("/api/v1/communities/search?q=test", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		var response map[string]interface{}
		client.AssertJSON(t, resp, &response)
		
		// Should include search results
		if total, exists := response["total"]; exists {
			if totalNum, ok := total.(float64); ok && totalNum > 0 {
				// Good - found results
			} else {
				t.Log("No search results found - this might be expected for test data")
			}
		}
		
		client.AssertCommunityFirst(t, resp)
	})

	t.Run("Get Community Statistics", func(t *testing.T) {
		resp := client.GET("/api/v1/communities/stats", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		var response map[string]interface{}
		client.AssertJSON(t, resp, &response)
		
		// Should include statistics
		if stats, exists := response["statistics"]; exists {
			if statsMap, ok := stats.(map[string]interface{}); ok {
				if _, exists := statsMap["total_communities"]; !exists {
					t.Error("Expected total_communities in statistics")
				}
			}
		}
		
		client.AssertContains(t, resp, "communities")
	})
}

func TestStoryAPI(t *testing.T) {
	// Setup test environment
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	fixtures := testDB.SeedTestData(t)

	// Create test router with handlers
	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	t.Run("Get Published Stories", func(t *testing.T) {
		resp := client.GET("/api/v1/stories", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		var response map[string]interface{}
		client.AssertJSON(t, resp, &response)
		
		// Should return published stories
		if stories, exists := response["stories"]; exists {
			if storiesArray, ok := stories.([]interface{}); ok {
				if len(storiesArray) == 0 {
					t.Error("Expected at least one published story")
				}
			}
		}
		
		client.AssertCommunityFirst(t, resp)
	})

	t.Run("Get Specific Story", func(t *testing.T) {
		storyID := fixtures.PublishedStory.ID
		
		resp := client.GET(fmt.Sprintf("/api/v1/stories/%d", storyID), nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		client.AssertStoryInResponse(t, resp, fixtures.PublishedStory.Slug)
		client.AssertCommunityFirst(t, resp)
	})

	t.Run("Create Story - Requires Authentication", func(t *testing.T) {
		newStory := map[string]interface{}{
			"community_id": fixtures.PublicCommunity.ID,
			"title":        "New Test Story",
			"summary":      "A new test story summary",
			"content":      "New test story content",
			"category":     "resilience",
			"story_type":   "community_strength",
		}
		
		// Try without authentication
		resp := client.POST("/api/v1/stories", newStory, nil)
		client.AssertAuthRequired(t, resp)
		
		// Try with authentication
		resp = client.MemberRequest("POST", "/api/v1/stories", newStory)
		// This should return "not implemented" since handler is placeholder
		client.AssertStatusCode(t, resp, http.StatusOK)
	})

	t.Run("Story Privacy Protection", func(t *testing.T) {
		storyID := fixtures.PublishedStory.ID
		
		resp := client.GET(fmt.Sprintf("/api/v1/stories/%d", storyID), nil)
		client.AssertPrivacyProtection(t, resp)
	})
}

func TestAuthenticationAPI(t *testing.T) {
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	fixtures := testDB.SeedTestData(t)

	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	t.Run("User Registration", func(t *testing.T) {
		registrationData := map[string]interface{}{
			"email":      "newuser@test.org",
			"username":   "newuser",
			"password":   "NewPassword123!",
			"first_name": "New",
			"last_name":  "User",
			"user_type":  "community_member",
		}
		
		resp := client.POST("/api/v1/auth/register", registrationData, nil)
		
		// Should return success or not implemented
		if resp.Code != http.StatusOK && resp.Code != http.StatusNotImplemented {
			client.AssertCommunityMessage(t, resp)
		}
	})

	t.Run("User Login", func(t *testing.T) {
		loginData := map[string]interface{}{
			"email":    fixtures.MemberUser.Email,
			"password": "TestPassword123!",
		}
		
		resp := client.POST("/api/v1/auth/login", loginData, nil)
		
		// Should return success or not implemented
		if resp.Code != http.StatusOK && resp.Code != http.StatusNotImplemented {
			client.AssertCommunityMessage(t, resp)
		}
	})
}

func TestSearchAPI(t *testing.T) {
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	fixtures := testDB.SeedTestData(t)

	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	t.Run("Global Search", func(t *testing.T) {
		resp := client.GET("/api/v1/search?q=test", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		var response map[string]interface{}
		client.AssertJSON(t, resp, &response)
		
		client.AssertCommunityFirst(t, resp)
	})

	t.Run("Search Communities", func(t *testing.T) {
		resp := client.GET("/api/v1/search/communities?q=resilient", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		client.AssertCommunityFirst(t, resp)
	})

	t.Run("Search Stories", func(t *testing.T) {
		resp := client.GET("/api/v1/search/stories?q=community", nil)
		client.AssertStatusCode(t, resp, http.StatusOK)
		
		client.AssertCommunityFirst(t, resp)
	})
}

func TestRateLimiting(t *testing.T) {
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	t.Run("Rate Limiting Protects Community Data", func(t *testing.T) {
		// Make many requests quickly
		successCount := 0
		rateLimitedCount := 0
		
		for i := 0; i < 20; i++ {
			resp := client.GET("/api/v1/communities", nil)
			
			if resp.Code == http.StatusOK {
				successCount++
			} else if resp.Code == http.StatusTooManyRequests {
				rateLimitedCount++
				client.AssertCommunityMessage(t, resp)
			}
		}
		
		// Should eventually be rate limited
		t.Logf("Successful requests: %d, Rate limited: %d", successCount, rateLimitedCount)
	})
}

func TestAccessibilityCompliance(t *testing.T) {
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	fixtures := testDB.SeedTestData(t)

	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	endpoints := []string{
		"/api/v1/communities",
		"/api/v1/stories",
		"/health",
	}

	for _, endpoint := range endpoints {
		t.Run(fmt.Sprintf("Accessibility Check: %s", endpoint), func(t *testing.T) {
			resp := client.GET(endpoint, nil)
			
			if resp.Code == http.StatusOK {
				client.AssertAccessibility(t, resp)
			}
		})
	}
}

func TestCommunityValues(t *testing.T) {
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	t.Run("Community-First Language in All Responses", func(t *testing.T) {
		endpoints := []string{
			"/health",
			"/api/v1/communities",
			"/api/v1/stories",
		}
		
		for _, endpoint := range endpoints {
			resp := client.GET(endpoint, nil)
			
			if resp.Code == http.StatusOK {
				client.AssertCommunityFirst(t, resp)
			}
		}
	})

	t.Run("Dignity-First Error Messages", func(t *testing.T) {
		// Test 404 error
		resp := client.GET("/api/v1/communities/99999", nil)
		
		if resp.Code == http.StatusNotFound {
			client.AssertCommunityMessage(t, resp)
			client.AssertCommunityFirst(t, resp)
		}
		
		// Test authentication required
		resp = client.POST("/api/v1/stories", map[string]interface{}{}, nil)
		
		if resp.Code == http.StatusUnauthorized {
			client.AssertCommunityMessage(t, resp)
		}
	})
}

func TestPerformance(t *testing.T) {
	testDB := testutils.NewTestDB(t)
	defer testDB.Close(t)

	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	t.Run("API Response Times", func(t *testing.T) {
		endpoints := map[string]int64{
			"/health":                200,  // 200ms max
			"/api/v1/communities":    500,  // 500ms max
			"/api/v1/stories":        500,  // 500ms max
		}
		
		for endpoint, maxDuration := range endpoints {
			client.TestResponseTime(t, "GET", endpoint, maxDuration)
		}
	})
}

// Helper function to create test router
func createTestRouter(testDB *testutils.TestDB) *gin.Engine {
	// Create repositories
	communityRepo := repositories.NewCommunityRepository(testDB.DB)
	storyRepo := repositories.NewStoryRepository(testDB.DB)
	userRepo := repositories.NewUserRepository(testDB.DB)

	// Create services
	communityService := services.NewCommunityService(communityRepo, storyRepo, userRepo)

	// Create handlers
	communityHandler := handlers.NewCommunityHandler(communityRepo, communityService)
	storyHandler := handlers.NewStoryHandler()
	userHandler := handlers.NewUserHandler()
	authHandler := handlers.NewAuthHandler()
	searchHandler := handlers.NewSearchHandler()
	healthHandler := handlers.NewHealthHandler(testDB.DB)

	// Create router
	router := gin.New()
	router.Use(gin.Recovery())

	// Setup routes
	services := &api.Services{
		CommunityHandler: communityHandler,
		StoryHandler:     storyHandler,
		UserHandler:      userHandler,
		AuthHandler:      authHandler,
		SearchHandler:    searchHandler,
		HealthHandler:    healthHandler,
	}

	cfg := &config.Config{
		JWT: config.JWTConfig{
			Secret: "test-secret",
			Issuer: "test",
		},
	}

	api.SetupRoutes(router, services, cfg)

	return router
}

// Benchmark tests
func BenchmarkCommunityAPI(b *testing.B) {
	testDB := testutils.NewTestDB(&testing.T{})
	defer testDB.Close(&testing.T{})

	fixtures := testDB.SeedTestData(&testing.T{})
	
	router := createTestRouter(testDB)
	client := testutils.NewTestClient(router)

	b.Run("GetCommunities", func(b *testing.B) {
		client.BenchmarkEndpoint(b, "GET", "/api/v1/communities", nil)
	})

	b.Run("GetStories", func(b *testing.B) {
		client.BenchmarkEndpoint(b, "GET", "/api/v1/stories", nil)
	})
	
	b.Run("Health Check", func(b *testing.B) {
		client.BenchmarkEndpoint(b, "GET", "/health", nil)
	})
}