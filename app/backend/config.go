// Configuration management system
// Created: January 31, 2025
// Purpose: Centralized, secure configuration for community platform

package config

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
	"log"
	
	"github.com/joho/godotenv"
)

// Config holds all application configuration
type Config struct {
	App           AppConfig
	Database      DatabaseConfig
	Redis         RedisConfig
	Elasticsearch ElasticsearchConfig
	JWT           JWTConfig
	CORS          CORSConfig
	RateLimit     RateLimitConfig
	Metrics       MetricsConfig
	Email         EmailConfig
	Storage       StorageConfig
}

// AppConfig contains general application settings
type AppConfig struct {
	Name        string
	Version     string
	Environment string
	Port        int
	Debug       bool
}

// DatabaseConfig contains database connection settings
type DatabaseConfig struct {
	URL             string
	Host            string
	Port            int
	Name            string
	User            string
	Password        string
	SSLMode         string
	LogLevel        string
	MaxOpenConns    int
	MaxIdleConns    int
	ConnMaxLifetime time.Duration
	ConnMaxIdleTime time.Duration
}

// RedisConfig contains Redis connection settings
type RedisConfig struct {
	URL      string
	Host     string
	Port     int
	Password string
	DB       int
}

// ElasticsearchConfig contains Elasticsearch settings
type ElasticsearchConfig struct {
	URL      string
	Host     string
	Port     int
	Username string
	Password string
}

// JWTConfig contains JWT authentication settings
type JWTConfig struct {
	Secret     string
	Expiry     time.Duration
	RefreshExpiry time.Duration
	Issuer     string
}

// CORSConfig contains CORS settings
type CORSConfig struct {
	AllowedOrigins []string
	AllowedMethods []string
	AllowedHeaders []string
}

// RateLimitConfig contains rate limiting settings
type RateLimitConfig struct {
	RequestsPerMinute int
	BurstSize        int
}

// MetricsConfig contains monitoring settings
type MetricsConfig struct {
	Enabled bool
	Port    int
	Path    string
}

// EmailConfig contains email/SMTP settings
type EmailConfig struct {
	Host     string
	Port     int
	Username string
	Password string
	From     string
}

// StorageConfig contains file storage settings
type StorageConfig struct {
	Type string
	Path string
}

// Load loads configuration from environment variables and .env files
func Load() (*Config, error) {
	// Load .env file if it exists
	if err := godotenv.Load(); err != nil {
		log.Printf("📋 No .env file found, using environment variables")
	} else {
		log.Printf("📋 Configuration loaded from .env file")
	}
	
	config := &Config{
		App:           loadAppConfig(),
		Database:      loadDatabaseConfig(),
		Redis:         loadRedisConfig(),
		Elasticsearch: loadElasticsearchConfig(),
		JWT:           loadJWTConfig(),
		CORS:          loadCORSConfig(),
		RateLimit:     loadRateLimitConfig(),
		Metrics:       loadMetricsConfig(),
		Email:         loadEmailConfig(),
		Storage:       loadStorageConfig(),
	}
	
	// Validate critical configuration
	if err := config.Validate(); err != nil {
		return nil, fmt.Errorf("configuration validation failed: %w", err)
	}
	
	log.Printf("✅ Configuration loaded successfully")
	log.Printf("🌍 Environment: %s", config.App.Environment)
	log.Printf("🚀 Version: %s", config.App.Version)
	
	return config, nil
}

func loadAppConfig() AppConfig {
	return AppConfig{
		Name:        getEnvString("APP_NAME", "Health Resilience Mapping API"),
		Version:     getEnvString("APP_VERSION", "1.0.0"),
		Environment: getEnvString("APP_ENV", "development"),
		Port:        getEnvInt("APP_PORT", 8080),
		Debug:       getEnvBool("APP_DEBUG", true),
	}
}

func loadDatabaseConfig() DatabaseConfig {
	return DatabaseConfig{
		URL:             getEnvString("DATABASE_URL", ""),
		Host:            getEnvString("DB_HOST", "localhost"),
		Port:            getEnvInt("DB_PORT", 5432),
		Name:            getEnvString("DB_NAME", "resilience_dev"),
		User:            getEnvString("DB_USER", "resilience"),
		Password:        getEnvString("DB_PASSWORD", "resilience_dev_password_2025"),
		SSLMode:         getEnvString("DB_SSL_MODE", "disable"),
		LogLevel:        getEnvString("DB_LOG_LEVEL", "info"),
		MaxOpenConns:    getEnvInt("DB_MAX_OPEN_CONNS", 25),
		MaxIdleConns:    getEnvInt("DB_MAX_IDLE_CONNS", 5),
		ConnMaxLifetime: getEnvDuration("DB_CONN_MAX_LIFETIME", 5*time.Minute),
		ConnMaxIdleTime: getEnvDuration("DB_CONN_MAX_IDLE_TIME", 5*time.Minute),
	}
}

func loadRedisConfig() RedisConfig {
	return RedisConfig{
		URL:      getEnvString("REDIS_URL", ""),
		Host:     getEnvString("REDIS_HOST", "localhost"),
		Port:     getEnvInt("REDIS_PORT", 6379),
		Password: getEnvString("REDIS_PASSWORD", ""),
		DB:       getEnvInt("REDIS_DB", 0),
	}
}

func loadElasticsearchConfig() ElasticsearchConfig {
	return ElasticsearchConfig{
		URL:      getEnvString("ELASTICSEARCH_URL", "http://localhost:9200"),
		Host:     getEnvString("ELASTICSEARCH_HOST", "localhost"),
		Port:     getEnvInt("ELASTICSEARCH_PORT", 9200),
		Username: getEnvString("ELASTICSEARCH_USERNAME", ""),
		Password: getEnvString("ELASTICSEARCH_PASSWORD", ""),
	}
}

func loadJWTConfig() JWTConfig {
	return JWTConfig{
		Secret:        getEnvString("JWT_SECRET", "development-jwt-secret-change-in-production-2025"),
		Expiry:        getEnvDuration("JWT_EXPIRY", 24*time.Hour),
		RefreshExpiry: getEnvDuration("JWT_REFRESH_EXPIRY", 7*24*time.Hour),
		Issuer:        getEnvString("JWT_ISSUER", "resilience-mapping.org"),
	}
}

func loadCORSConfig() CORSConfig {
	origins := getEnvStringSlice("CORS_ALLOWED_ORIGINS", []string{
		"http://localhost:3000",
		"http://localhost:3001", 
		"http://localhost:3002",
	})
	
	return CORSConfig{
		AllowedOrigins: origins,
		AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders: []string{
			"Origin",
			"Content-Type",
			"Accept", 
			"Authorization",
			"X-Request-ID",
			"X-User-Type",
		},
	}
}

func loadRateLimitConfig() RateLimitConfig {
	return RateLimitConfig{
		RequestsPerMinute: getEnvInt("RATE_LIMIT_REQUESTS_PER_MINUTE", 1000),
		BurstSize:         getEnvInt("RATE_LIMIT_BURST_SIZE", 50),
	}
}

func loadMetricsConfig() MetricsConfig {
	return MetricsConfig{
		Enabled: getEnvBool("ENABLE_METRICS", true),
		Port:    getEnvInt("METRICS_PORT", 9090),
		Path:    getEnvString("METRICS_PATH", "/metrics"),
	}
}

func loadEmailConfig() EmailConfig {
	return EmailConfig{
		Host:     getEnvString("SMTP_HOST", "localhost"),
		Port:     getEnvInt("SMTP_PORT", 1025),
		Username: getEnvString("SMTP_USER", ""),
		Password: getEnvString("SMTP_PASSWORD", ""),
		From:     getEnvString("SMTP_FROM", "noreply@resilience-mapping.local"),
	}
}

func loadStorageConfig() StorageConfig {
	return StorageConfig{
		Type: getEnvString("STORAGE_TYPE", "local"),
		Path: getEnvString("STORAGE_PATH", "./storage"),
	}
}

// Validate checks if the configuration is valid
func (c *Config) Validate() error {
	// Validate critical settings
	if c.JWT.Secret == "" {
		return fmt.Errorf("JWT secret is required")
	}
	
	if c.App.Environment == "production" && c.JWT.Secret == "development-jwt-secret-change-in-production-2025" {
		return fmt.Errorf("production environment requires a secure JWT secret")
	}
	
	if c.Database.URL == "" {
		if c.Database.Host == "" || c.Database.Name == "" || c.Database.User == "" {
			return fmt.Errorf("database configuration is incomplete")
		}
	}
	
	if c.App.Port <= 0 || c.App.Port > 65535 {
		return fmt.Errorf("invalid port number: %d", c.App.Port)
	}
	
	// Validate community-specific settings
	if c.RateLimit.RequestsPerMinute <= 0 {
		return fmt.Errorf("rate limit must be positive")
	}
	
	return nil
}

// IsProduction returns true if running in production
func (c *Config) IsProduction() bool {
	return c.App.Environment == "production"
}

// IsDevelopment returns true if running in development
func (c *Config) IsDevelopment() bool {
	return c.App.Environment == "development"
}

// GetDatabaseDSN returns the database connection string
func (c *Config) GetDatabaseDSN() string {
	if c.Database.URL != "" {
		return c.Database.URL
	}
	
	return fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
		c.Database.Host,
		c.Database.Port,
		c.Database.User,
		c.Database.Password,
		c.Database.Name,
		c.Database.SSLMode,
	)
}

// Helper functions for reading environment variables

func getEnvString(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intValue, err := strconv.Atoi(value); err == nil {
			return intValue
		}
	}
	return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
	if value := os.Getenv(key); value != "" {
		if boolValue, err := strconv.ParseBool(value); err == nil {
			return boolValue
		}
	}
	return defaultValue
}

func getEnvDuration(key string, defaultValue time.Duration) time.Duration {
	if value := os.Getenv(key); value != "" {
		if duration, err := time.ParseDuration(value); err == nil {
			return duration
		}
	}
	return defaultValue
}

func getEnvStringSlice(key string, defaultValue []string) []string {
	if value := os.Getenv(key); value != "" {
		return strings.Split(value, ",")
	}
	return defaultValue
}