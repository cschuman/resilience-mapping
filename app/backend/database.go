// Database initialization and connection management
// Created: January 31, 2025
// Purpose: Secure, reliable database connections for community data

package database

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"github.com/your-org/resilience-mapping/internal/config"
	"github.com/your-org/resilience-mapping/internal/models"
)

// Database wraps GORM DB with additional functionality
type Database struct {
	*gorm.DB
	config *config.DatabaseConfig
}

// NewDatabase creates a new database connection
func NewDatabase(cfg *config.DatabaseConfig) (*Database, error) {
	// Build connection string
	dsn := buildDSN(cfg)
	
	// Configure GORM
	gormConfig := &gorm.Config{
		Logger: getLogger(cfg.LogLevel),
		NowFunc: func() time.Time {
			return time.Now().UTC()
		},
	}
	
	// Open database connection
	db, err := gorm.Open(postgres.Open(dsn), gormConfig)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to database: %w", err)
	}
	
	// Get underlying SQL DB for configuration
	sqlDB, err := db.DB()
	if err != nil {
		return nil, fmt.Errorf("failed to get SQL DB: %w", err)
	}
	
	// Configure connection pool
	sqlDB.SetMaxOpenConns(cfg.MaxOpenConns)
	sqlDB.SetMaxIdleConns(cfg.MaxIdleConns)
	sqlDB.SetConnMaxLifetime(cfg.ConnMaxLifetime)
	sqlDB.SetConnMaxIdleTime(cfg.ConnMaxIdleTime)
	
	// Test connection
	if err := sqlDB.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}
	
	database := &Database{
		DB:     db,
		config: cfg,
	}
	
	log.Printf("🗄️ Database connected successfully")
	log.Printf("📊 Connection pool: %d max open, %d max idle", cfg.MaxOpenConns, cfg.MaxIdleConns)
	
	return database, nil
}

// Migrate runs database migrations
func (d *Database) Migrate() error {
	log.Printf("🔄 Running database migrations...")
	
	// Enable PostGIS extension
	if err := d.enablePostGIS(); err != nil {
		return fmt.Errorf("failed to enable PostGIS: %w", err)
	}
	
	// Auto-migrate models
	err := d.AutoMigrate(
		&models.User{},
		&models.Community{},
		&models.Story{},
		&models.Comment{},
	)
	if err != nil {
		return fmt.Errorf("failed to run migrations: %w", err)
	}
	
	// Create indexes for performance
	if err := d.createIndexes(); err != nil {
		return fmt.Errorf("failed to create indexes: %w", err)
	}
	
	log.Printf("✅ Database migrations completed successfully")
	return nil
}

// Close closes the database connection
func (d *Database) Close() error {
	sqlDB, err := d.DB.DB()
	if err != nil {
		return err
	}
	
	log.Printf("🔒 Closing database connection...")
	return sqlDB.Close()
}

// Health checks database health
func (d *Database) Health() error {
	sqlDB, err := d.DB.DB()
	if err != nil {
		return fmt.Errorf("failed to get SQL DB: %w", err)
	}
	
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	return sqlDB.PingContext(ctx)
}

// GetStats returns database connection statistics
func (d *Database) GetStats() map[string]interface{} {
	sqlDB, err := d.DB.DB()
	if err != nil {
		return map[string]interface{}{
			"error": err.Error(),
		}
	}
	
	stats := sqlDB.Stats()
	return map[string]interface{}{
		"open_connections": stats.OpenConnections,
		"in_use":          stats.InUse,
		"idle":            stats.Idle,
		"wait_count":      stats.WaitCount,
		"wait_duration":   stats.WaitDuration,
		"max_idle_closed": stats.MaxIdleClosed,
		"max_lifetime_closed": stats.MaxLifetimeClosed,
	}
}

// Helper functions

func buildDSN(cfg *config.DatabaseConfig) string {
	if cfg.URL != "" {
		return cfg.URL
	}
	
	return fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
		cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.Name, cfg.SSLMode,
	)
}

func getLogger(level string) logger.Interface {
	var logLevel logger.LogLevel
	
	switch level {
	case "silent":
		logLevel = logger.Silent
	case "error":
		logLevel = logger.Error
	case "warn":
		logLevel = logger.Warn
	case "info":
		logLevel = logger.Info
	default:
		logLevel = logger.Info
	}
	
	return logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags),
		logger.Config{
			SlowThreshold:             200 * time.Millisecond,
			LogLevel:                  logLevel,
			IgnoreRecordNotFoundError: true,
			Colorful:                  true,
		},
	)
}

func (d *Database) enablePostGIS() error {
	// Check if PostGIS extension exists
	var exists bool
	err := d.Raw("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'postgis')").Scan(&exists).Error
	if err != nil {
		return err
	}
	
	if !exists {
		log.Printf("🗺️ Enabling PostGIS extension...")
		if err := d.Exec("CREATE EXTENSION IF NOT EXISTS postgis").Error; err != nil {
			return fmt.Errorf("failed to create PostGIS extension: %w", err)
		}
		log.Printf("✅ PostGIS extension enabled")
	} else {
		log.Printf("✅ PostGIS extension already enabled")
	}
	
	return nil
}

func (d *Database) createIndexes() error {
	indexes := []struct {
		table string
		index string
		sql   string
	}{
		{
			table: "communities",
			index: "idx_communities_geom",
			sql:   "CREATE INDEX IF NOT EXISTS idx_communities_geom ON communities USING GIST (geometry)",
		},
		{
			table: "communities",
			index: "idx_communities_centroid",
			sql:   "CREATE INDEX IF NOT EXISTS idx_communities_centroid ON communities USING GIST (centroid)",
		},
		{
			table: "communities",
			index: "idx_communities_resilience_score",
			sql:   "CREATE INDEX IF NOT EXISTS idx_communities_resilience_score ON communities (resilience_score DESC)",
		},
		{
			table: "communities",
			index: "idx_communities_state_county",
			sql:   "CREATE INDEX IF NOT EXISTS idx_communities_state_county ON communities (state, county)",
		},
		{
			table: "stories",
			index: "idx_stories_community_status",
			sql:   "CREATE INDEX IF NOT EXISTS idx_stories_community_status ON stories (community_id, status)",
		},
		{
			table: "stories",
			index: "idx_stories_published_at",
			sql:   "CREATE INDEX IF NOT EXISTS idx_stories_published_at ON stories (published_at DESC) WHERE published_at IS NOT NULL",
		},
		{
			table: "users",
			index: "idx_users_community_id",
			sql:   "CREATE INDEX IF NOT EXISTS idx_users_community_id ON users (community_id) WHERE community_id IS NOT NULL",
		},
	}
	
	log.Printf("🔍 Creating performance indexes...")
	
	for _, idx := range indexes {
		if err := d.Exec(idx.sql).Error; err != nil {
			log.Printf("⚠️ Warning: Failed to create index %s: %v", idx.index, err)
			// Continue with other indexes rather than failing completely
		} else {
			log.Printf("✅ Created index: %s", idx.index)
		}
	}
	
	return nil
}

// Transaction helpers

// WithTransaction executes function within a database transaction
func (d *Database) WithTransaction(fn func(*gorm.DB) error) error {
	tx := d.Begin()
	if tx.Error != nil {
		return tx.Error
	}
	
	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
			panic(r)
		}
	}()
	
	if err := fn(tx); err != nil {
		tx.Rollback()
		return err
	}
	
	return tx.Commit().Error
}

// Seed creates initial data for development
func (d *Database) Seed() error {
	log.Printf("🌱 Seeding database with community-first sample data...")
	
	// Create sample admin user
	adminUser := &models.User{
		Email:        "admin@resilience-mapping.org",
		Username:     "admin",
		FirstName:    "System",
		LastName:     "Administrator",
		UserType:     "admin",
		Role:         "admin",
		Status:       "active",
		IsVerified:   true,
		EmailVerified: true,
		ConsentGiven: true,
		TermsAccepted: true,
		PrivacyAccepted: true,
	}
	adminUser.SetPassword("AdminPassword123!")
	
	if err := d.FirstOrCreate(adminUser, models.User{Email: adminUser.Email}).Error; err != nil {
		return fmt.Errorf("failed to create admin user: %w", err)
	}
	
	log.Printf("✅ Database seeded with sample data")
	log.Printf("🔐 Admin user created: admin@resilience-mapping.org")
	log.Printf("🏘️ Ready to serve resilient communities")
	
	return nil
}