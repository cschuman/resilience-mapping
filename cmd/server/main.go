// Health Resilience Mapping Platform - API Server
// Created: January 31, 2025
// Purpose: Main HTTP API server serving all three sites (stories, research, policy)

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/swaggo/gin-swagger"
	"github.com/swaggo/files"
	"github.com/example/resilience-mapping-go/internal/config"
	"github.com/example/resilience-mapping-go/internal/api"
	"github.com/example/resilience-mapping-go/internal/middleware"
	"github.com/example/resilience-mapping-go/internal/repositories"
	"github.com/example/resilience-mapping-go/internal/services"
	"github.com/example/resilience-mapping-go/internal/handlers"
	_ "github.com/example/resilience-mapping-go/docs" // Import generated docs
)

// @title Health Resilience Mapping API
// @version 1.0
// @description API for accessing community resilience data, stories, and policy insights
// @termsOfService https://resilience-mapping.org/terms
// @contact.name API Support
// @contact.url https://resilience-mapping.org/support
// @contact.email support@resilience-mapping.org
// @license.name MIT
// @license.url https://opensource.org/licenses/MIT
// @host api.resilience-mapping.org
// @BasePath /v1
// @schemes https http

func main() {
	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Set Gin mode based on environment
	if cfg.App.Environment == "production" {
		gin.SetMode(gin.ReleaseMode)
	} else {
		gin.SetMode(gin.DebugMode)
	}

	// Initialize database
	db, err := repositories.NewDatabase(cfg.Database)
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}
	defer db.Close()

	// Initialize cache
	cache, err := repositories.NewCache(cfg.Redis)
	if err != nil {
		log.Fatalf("Failed to initialize cache: %v", err)
	}
	defer cache.Close()

	// Initialize search engine
	search, err := repositories.NewSearch(cfg.Elasticsearch)
	if err != nil {
		log.Fatalf("Failed to initialize search engine: %v", err)
	}
	defer search.Close()

	// Initialize repositories (for now, use simple constructors)
	communityRepo := repositories.NewCommunityRepository(db)
	storyRepo := repositories.NewStoryRepository(db)
	userRepo := repositories.NewUserRepository(db)

	// Initialize services
	communityService := services.NewCommunityService(communityRepo, storyRepo, userRepo)

	// Initialize handlers
	communityHandler := handlers.NewCommunityHandler(communityRepo, communityService)
	storyHandler := handlers.NewStoryHandler()
	userHandler := handlers.NewUserHandler()
	authHandler := handlers.NewAuthHandler()
	searchHandler := handlers.NewSearchHandler()
	healthHandler := handlers.NewHealthHandler(db)

	// Create services struct for routes
	services := &api.Services{
		CommunityHandler: communityHandler,
		StoryHandler:     storyHandler,
		UserHandler:      userHandler,
		AuthHandler:      authHandler,
		SearchHandler:    searchHandler,
		HealthHandler:    healthHandler,
	}

	// Create Gin router
	router := gin.New()

	// Add middleware
	setupMiddleware(router, cfg)

	// Setup Swagger documentation endpoint
	router.GET("/docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	// Setup routes
	api.SetupRoutes(router, services, cfg)

	// Create HTTP server
	server := &http.Server{
		Addr:         fmt.Sprintf(":%d", cfg.App.Port),
		Handler:      router,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 30 * time.Second,
		IdleTimeout:  120 * time.Second,
	}

	// Start server in a goroutine
	go func() {
		log.Printf("🚀 Server starting on port %d", cfg.App.Port)
		log.Printf("📊 Environment: %s", cfg.App.Environment)
		log.Printf("🌍 API Documentation: http://localhost:%d/docs", cfg.App.Port)
		log.Printf("❤️  Building for 1,000+ communities with dignity")
		
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Failed to start server: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("🛑 Server shutting down...")

	// Give the server 30 seconds to shutdown gracefully
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("✅ Server shutdown complete")
}

// setupMiddleware configures all middleware for the Gin router
func setupMiddleware(router *gin.Engine, cfg *config.Config) {
	// Recovery middleware recovers from any panics and writes a 500 if there was one
	router.Use(gin.Recovery())

	// Custom logging middleware
	router.Use(middleware.Logger())

	// CORS middleware - allow cross-origin requests from our frontend sites
	router.Use(middleware.CORS(cfg.CORS))

	// Security headers middleware
	router.Use(middleware.SecurityHeaders())

	// Rate limiting middleware
	router.Use(middleware.RateLimit(cfg.RateLimit))

	// Request ID middleware - adds unique ID to each request
	router.Use(middleware.RequestID())

	// Community-first reminder middleware (development only)
	if cfg.App.Environment == "development" {
		router.Use(middleware.CommunityFirst())
	}

	// Metrics middleware (if enabled)
	if cfg.Metrics.Enabled {
		router.Use(middleware.Metrics())
	}
}