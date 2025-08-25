// API routes configuration
// Created: January 31, 2025
// Purpose: Define all API endpoints with community-first approach

package api

import (
	"github.com/gin-gonic/gin"
	"github.com/your-org/resilience-mapping/internal/handlers"
	"github.com/your-org/resilience-mapping/internal/middleware"
	"github.com/your-org/resilience-mapping/internal/config"
)

// Services contains all service dependencies
type Services struct {
	CommunityHandler *handlers.CommunityHandler
	StoryHandler     *handlers.StoryHandler
	UserHandler      *handlers.UserHandler
	AuthHandler      *handlers.AuthHandler
	SearchHandler    *handlers.SearchHandler
	HealthHandler    *handlers.HealthHandler
}

// SetupRoutes configures all API routes
func SetupRoutes(router *gin.Engine, services *Services, cfg *config.Config) {
	// Health check endpoints (no auth required)
	router.GET("/health", services.HealthHandler.Health)
	router.GET("/ready", services.HealthHandler.Ready)
	
	// Public API routes (no auth required)
	v1 := router.Group("/api/v1")
	{
		// Community endpoints - public access
		communities := v1.Group("/communities")
		{
			communities.GET("", services.CommunityHandler.List)
			communities.GET("/:id", services.CommunityHandler.GetByID)
			communities.GET("/:id/stories", services.CommunityHandler.GetStories)
			communities.GET("/search", services.CommunityHandler.Search)
			communities.GET("/nearby", services.CommunityHandler.GetNearby)
			communities.GET("/resilient", services.CommunityHandler.GetResilient)
			communities.GET("/stats", services.CommunityHandler.GetStatistics)
		}
		
		// Story endpoints - public read access
		stories := v1.Group("/stories")
		{
			stories.GET("", services.StoryHandler.List)
			stories.GET("/:id", services.StoryHandler.GetByID)
			stories.GET("/slug/:slug", services.StoryHandler.GetBySlug)
			stories.GET("/featured", services.StoryHandler.GetFeatured)
			stories.GET("/popular", services.StoryHandler.GetPopular)
			stories.GET("/categories", services.StoryHandler.GetCategories)
			stories.GET("/tags", services.StoryHandler.GetTags)
			stories.POST("/:id/view", services.StoryHandler.IncrementViews)
			stories.POST("/:id/share", services.StoryHandler.IncrementShares)
		}
		
		// Search endpoints
		search := v1.Group("/search")
		{
			search.GET("", services.SearchHandler.GlobalSearch)
			search.GET("/communities", services.SearchHandler.SearchCommunities)
			search.GET("/stories", services.SearchHandler.SearchStories)
			search.GET("/suggest", services.SearchHandler.SearchSuggestions)
		}
		
		// Authentication endpoints
		auth := v1.Group("/auth")
		{
			auth.POST("/register", services.AuthHandler.Register)
			auth.POST("/login", services.AuthHandler.Login)
			auth.POST("/refresh", services.AuthHandler.RefreshToken)
			auth.POST("/forgot-password", services.AuthHandler.ForgotPassword)
			auth.POST("/reset-password", services.AuthHandler.ResetPassword)
			auth.POST("/verify-email", services.AuthHandler.VerifyEmail)
		}
		
		// Public user profiles
		users := v1.Group("/users")
		{
			users.GET("/:id/public", services.UserHandler.GetPublicProfile)
			users.GET("/:id/stories", services.UserHandler.GetUserStories)
		}
	}
	
	// Protected API routes (authentication required)
	protected := v1.Group("")
	protected.Use(middleware.RequireAuth())
	{
		// User management
		user := protected.Group("/user")
		{
			user.GET("/profile", services.UserHandler.GetProfile)
			user.PUT("/profile", services.UserHandler.UpdateProfile)
			user.PUT("/password", services.UserHandler.ChangePassword)
			user.PUT("/preferences", services.UserHandler.UpdatePreferences)
			user.PUT("/notifications", services.UserHandler.UpdateNotifications)
			user.GET("/stories", services.UserHandler.GetMyStories)
			user.GET("/drafts", services.UserHandler.GetMyDrafts)
			user.DELETE("/account", services.UserHandler.DeleteAccount)
		}
		
		// Story creation and management
		storyMgmt := protected.Group("/stories")
		{
			storyMgmt.POST("", services.StoryHandler.Create)
			storyMgmt.PUT("/:id", services.StoryHandler.Update)
			storyMgmt.POST("/:id/publish", services.StoryHandler.Publish)
			storyMgmt.POST("/:id/like", services.StoryHandler.LikeStory)
			storyMgmt.DELETE("/:id", services.StoryHandler.Delete)
			storyMgmt.POST("/:id/comments", services.StoryHandler.AddComment)
			storyMgmt.GET("/:id/comments", services.StoryHandler.GetComments)
		}
		
		// Community interaction (for community members)
		communityInteraction := protected.Group("/communities")
		{
			communityInteraction.POST("/:id/contact", services.CommunityHandler.ContactCommunity)
			communityInteraction.POST("/:id/join", services.CommunityHandler.JoinCommunity)
			communityInteraction.POST("/:id/approve-story", services.CommunityHandler.ApproveStory)
		}
		
		// Research access (for verified researchers)
		research := protected.Group("/research")
		research.Use(middleware.RequireRole("researcher"))
		{
			research.GET("/data/communities", services.CommunityHandler.GetResearchData)
			research.GET("/data/stories", services.StoryHandler.GetResearchData)
			research.GET("/export/csv", services.CommunityHandler.ExportCSV)
			research.GET("/export/json", services.CommunityHandler.ExportJSON)
			research.GET("/analytics", services.CommunityHandler.GetAnalytics)
		}
		
		// Policy maker access
		policy := protected.Group("/policy")
		policy.Use(middleware.RequireRole("policymaker"))
		{
			policy.GET("/briefings", services.StoryHandler.GetPolicyBriefings)
			policy.GET("/impact-reports", services.CommunityHandler.GetImpactReports)
			policy.GET("/recommendations", services.CommunityHandler.GetPolicyRecommendations)
		}
	}
	
	// Admin routes (admin role required)
	admin := v1.Group("/admin")
	admin.Use(middleware.RequireAuth(), middleware.RequireRole("admin"))
	{
		// User management
		adminUsers := admin.Group("/users")
		{
			adminUsers.GET("", services.UserHandler.ListUsers)
			adminUsers.GET("/:id", services.UserHandler.GetUser)
			adminUsers.PUT("/:id/status", services.UserHandler.UpdateUserStatus)
			adminUsers.POST("/:id/verify", services.UserHandler.VerifyUser)
			adminUsers.DELETE("/:id", services.UserHandler.DeleteUser)
			adminUsers.GET("/stats", services.UserHandler.GetUserStats)
		}
		
		// Story moderation
		adminStories := admin.Group("/stories")
		{
			adminStories.GET("/pending", services.StoryHandler.GetPendingStories)
			adminStories.POST("/:id/approve", services.StoryHandler.ApproveStory)
			adminStories.POST("/:id/reject", services.StoryHandler.RejectStory)
			adminStories.POST("/:id/feature", services.StoryHandler.FeatureStory)
			adminStories.DELETE("/:id/force", services.StoryHandler.ForceDeleteStory)
		}
		
		// Community management
		adminCommunities := admin.Group("/communities")
		{
			adminCommunities.POST("", services.CommunityHandler.CreateCommunity)
			adminCommunities.PUT("/:id", services.CommunityHandler.UpdateCommunity)
			adminCommunities.POST("/:id/approve", services.CommunityHandler.ApproveCommunity)
			adminCommunities.DELETE("/:id", services.CommunityHandler.DeleteCommunity)
			adminCommunities.POST("/bulk-import", services.CommunityHandler.BulkImport)
		}
		
		// System monitoring
		adminSystem := admin.Group("/system")
		{
			adminSystem.GET("/metrics", services.HealthHandler.GetMetrics)
			adminSystem.GET("/logs", services.HealthHandler.GetLogs)
			adminSystem.POST("/backup", services.HealthHandler.CreateBackup)
			adminSystem.GET("/status", services.HealthHandler.GetSystemStatus)
		}
	}
	
	// Webhook endpoints for external integrations
	webhooks := v1.Group("/webhooks")
	webhooks.Use(middleware.ValidateWebhook())
	{
		webhooks.POST("/github", services.HealthHandler.GitHubWebhook)
		webhooks.POST("/community-feedback", services.CommunityHandler.CommunityFeedbackWebhook)
	}
	
	// Special routes for different site types
	
	// Stories site specific endpoints
	storiesSite := router.Group("/stories-api")
	{
		storiesSite.GET("/featured", services.StoryHandler.GetFeaturedForSite)
		storiesSite.GET("/latest", services.StoryHandler.GetLatestForSite)
		storiesSite.GET("/by-community/:id", services.StoryHandler.GetByCommunityForSite)
	}
	
	// Research site specific endpoints  
	researchSite := router.Group("/research-api")
	researchSite.Use(middleware.RequireAuth(), middleware.RequireRole("researcher"))
	{
		researchSite.GET("/datasets", services.CommunityHandler.GetResearchDatasets)
		researchSite.GET("/methodologies", services.CommunityHandler.GetMethodologies)
		researchSite.GET("/publications", services.CommunityHandler.GetPublications)
	}
	
	// Policy site specific endpoints
	policySite := router.Group("/policy-api")
	policySite.Use(middleware.RequireAuth(), middleware.RequireRole("policymaker"))
	{
		policySite.GET("/briefs", services.StoryHandler.GetPolicyBriefs)
		policySite.GET("/interventions", services.CommunityHandler.GetInterventions)
		policySite.GET("/outcomes", services.CommunityHandler.GetOutcomes)
	}
}