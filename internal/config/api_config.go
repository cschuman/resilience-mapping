// Package config handles API server configuration
// Created: January 31, 2025
// Purpose: Centralized configuration management for the API server

package config

import (
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/spf13/viper"
)

// APIConfig holds all configuration values for the API server
type APIConfig struct {
	App           AppConfig           `mapstructure:"app"`
	Database      DatabaseConfig      `mapstructure:"database"`
	Redis         RedisConfig         `mapstructure:"redis"`
	Elasticsearch ElasticsearchConfig `mapstructure:"elasticsearch"`
	SMTP          SMTPConfig          `mapstructure:"smtp"`
	JWT           JWTConfig           `mapstructure:"jwt"`
	CORS          CORSConfig          `mapstructure:"cors"`
	RateLimit     RateLimitConfig     `mapstructure:"rate_limit"`
	Storage       StorageConfig       `mapstructure:"storage"`
	Metrics       MetricsConfig       `mapstructure:"metrics"`
	Logging       LoggingConfig       `mapstructure:"logging"`
}

// AppConfig contains general application settings
type AppConfig struct {
	Environment string `mapstructure:"environment" default:"development"`
	Port        int    `mapstructure:"port" default:"8080"`
	Debug       bool   `mapstructure:"debug" default:"false"`
	Name        string `mapstructure:"name" default:"Health Resilience Mapping API"`
	Version     string `mapstructure:"version" default:"1.0.0"`
}

// DatabaseConfig contains database connection settings
type DatabaseConfig struct {
	URL      string `mapstructure:"url"`
	Host     string `mapstructure:"host" default:"localhost"`
	Port     int    `mapstructure:"port" default:"5432"`
	Name     string `mapstructure:"name" default:"resilience_dev"`
	User     string `mapstructure:"user" default:"resilience"`
	Password string `mapstructure:"password"`
	SSLMode  string `mapstructure:"ssl_mode" default:"disable"`
	
	// Connection pool settings
	MaxOpenConns    int           `mapstructure:"max_open_conns" default:"25"`
	MaxIdleConns    int           `mapstructure:"max_idle_conns" default:"5"`
	ConnMaxLifetime time.Duration `mapstructure:"conn_max_lifetime" default:"1h"`
	ConnMaxIdleTime time.Duration `mapstructure:"conn_max_idle_time" default:"30m"`
}

// RedisConfig contains Redis connection settings
type RedisConfig struct {
	URL      string `mapstructure:"url"`
	Host     string `mapstructure:"host" default:"localhost"`
	Port     int    `mapstructure:"port" default:"6379"`
	Password string `mapstructure:"password"`
	Database int    `mapstructure:"database" default:"0"`
	
	// Connection pool settings
	PoolSize           int           `mapstructure:"pool_size" default:"10"`
	MinIdleConns       int           `mapstructure:"min_idle_conns" default:"2"`
	MaxConnAge         time.Duration `mapstructure:"max_conn_age" default:"1h"`
	PoolTimeout        time.Duration `mapstructure:"pool_timeout" default:"30s"`
	IdleTimeout        time.Duration `mapstructure:"idle_timeout" default:"5m"`
	IdleCheckFrequency time.Duration `mapstructure:"idle_check_frequency" default:"1m"`
}

// ElasticsearchConfig contains Elasticsearch connection settings
type ElasticsearchConfig struct {
	URL      string `mapstructure:"url" default:"http://localhost:9200"`
	Host     string `mapstructure:"host" default:"localhost"`
	Port     int    `mapstructure:"port" default:"9200"`
	Username string `mapstructure:"username"`
	Password string `mapstructure:"password"`
	
	// Index settings
	CommunitiesIndex string `mapstructure:"communities_index" default:"communities"`
	StoriesIndex     string `mapstructure:"stories_index" default:"stories"`
	SearchIndex      string `mapstructure:"search_index" default:"search_queries"`
}

// SMTPConfig contains email server settings
type SMTPConfig struct {
	Host     string `mapstructure:"host" default:"localhost"`
	Port     int    `mapstructure:"port" default:"1025"`
	User     string `mapstructure:"user"`
	Password string `mapstructure:"password"`
	From     string `mapstructure:"from" default:"noreply@resilience-mapping.org"`
	
	// Template settings
	TemplateDir string `mapstructure:"template_dir" default:"templates/email"`
	
	// Development settings
	UseTLS       bool `mapstructure:"use_tls" default:"false"`
	InsecureTLS  bool `mapstructure:"insecure_tls" default:"true"`
}

// JWTConfig contains JWT token settings
type JWTConfig struct {
	Secret     string        `mapstructure:"secret"`
	Expiry     time.Duration `mapstructure:"expiry" default:"24h"`
	Issuer     string        `mapstructure:"issuer" default:"resilience-mapping-api"`
	Algorithm  string        `mapstructure:"algorithm" default:"HS256"`
}

// CORSConfig contains CORS settings
type CORSConfig struct {
	AllowedOrigins   []string `mapstructure:"allowed_origins"`
	AllowedMethods   []string `mapstructure:"allowed_methods"`
	AllowedHeaders   []string `mapstructure:"allowed_headers"`
	AllowCredentials bool     `mapstructure:"allow_credentials" default:"true"`
}

// RateLimitConfig contains rate limiting settings
type RateLimitConfig struct {
	RequestsPerMinute int           `mapstructure:"requests_per_minute" default:"60"`
	BurstSize         int           `mapstructure:"burst_size" default:"10"`
	CleanupInterval   time.Duration `mapstructure:"cleanup_interval" default:"1m"`
	
	// Different limits for different endpoints
	SearchLimit    int `mapstructure:"search_limit" default:"100"`
	DownloadLimit  int `mapstructure:"download_limit" default:"10"`
	ContactLimit   int `mapstructure:"contact_limit" default:"5"`
}

// StorageConfig contains file storage settings
type StorageConfig struct {
	Type     string `mapstructure:"type" default:"local"`
	Path     string `mapstructure:"path" default:"./storage"`
	
	// AWS S3 settings
	AWSRegion          string `mapstructure:"aws_region"`
	AWSAccessKeyID     string `mapstructure:"aws_access_key_id"`
	AWSSecretAccessKey string `mapstructure:"aws_secret_access_key"`
	S3BucketName       string `mapstructure:"s3_bucket_name"`
	S3Endpoint         string `mapstructure:"s3_endpoint"`
	
	// Upload limits
	MaxFileSize   int64 `mapstructure:"max_file_size" default:"10485760"` // 10MB
	AllowedTypes  []string `mapstructure:"allowed_types"`
}

// MetricsConfig contains monitoring and metrics settings
type MetricsConfig struct {
	Enabled bool   `mapstructure:"enabled" default:"true"`
	Port    int    `mapstructure:"port" default:"9090"`
	Path    string `mapstructure:"path" default:"/metrics"`
	
	// External monitoring
	SentryDSN string `mapstructure:"sentry_dsn"`
}

// LoggingConfig contains logging settings
type LoggingConfig struct {
	Level      string `mapstructure:"level" default:"info"`
	Format     string `mapstructure:"format" default:"json"`
	Output     string `mapstructure:"output" default:"stdout"`
	
	// File logging
	FilePath   string `mapstructure:"file_path"`
	MaxSize    int    `mapstructure:"max_size" default:"100"`    // MB
	MaxBackups int    `mapstructure:"max_backups" default:"3"`
	MaxAge     int    `mapstructure:"max_age" default:"28"`      // days
	Compress   bool   `mapstructure:"compress" default:"true"`
}

// Load reads API server configuration from environment variables and config files
func Load() (*APIConfig, error) {
	cfg := &APIConfig{}
	
	// Create new viper instance for API config
	v := viper.New()
	
	// Set default values
	setAPIDefaults(v)
	
	// Read from config file if it exists
	v.SetConfigName("api")
	v.SetConfigType("yaml")
	v.AddConfigPath("./config")
	v.AddConfigPath(".")
	
	// Read config file (optional)
	if err := v.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
			return nil, fmt.Errorf("failed to read config file: %w", err)
		}
	}
	
	// Override with environment variables
	v.AutomaticEnv()
	v.SetEnvKeyReplacer(strings.NewReplacer(".", "_", "-", "_"))
	
	// Bind specific environment variables
	bindAPIEnvironmentVariables(v)
	
	// Unmarshal configuration
	if err := v.Unmarshal(cfg); err != nil {
		return nil, fmt.Errorf("failed to unmarshal config: %w", err)
	}
	
	// Set environment-specific defaults
	setAPIEnvironmentDefaults(cfg)
	
	// Validate configuration
	if err := validateAPIConfig(cfg); err != nil {
		return nil, fmt.Errorf("configuration validation failed: %w", err)
	}
	
	return cfg, nil
}

// setAPIDefaults sets default configuration values
func setAPIDefaults(v *viper.Viper) {
	// App defaults
	v.SetDefault("app.environment", "development")
	v.SetDefault("app.port", 8080)
	v.SetDefault("app.debug", false)
	v.SetDefault("app.name", "Health Resilience Mapping API")
	v.SetDefault("app.version", "1.0.0")
	
	// Database defaults
	v.SetDefault("database.host", "localhost")
	v.SetDefault("database.port", 5432)
	v.SetDefault("database.name", "resilience_dev")
	v.SetDefault("database.user", "resilience")
	v.SetDefault("database.ssl_mode", "disable")
	v.SetDefault("database.max_open_conns", 25)
	v.SetDefault("database.max_idle_conns", 5)
	v.SetDefault("database.conn_max_lifetime", "1h")
	v.SetDefault("database.conn_max_idle_time", "30m")
	
	// Redis defaults
	v.SetDefault("redis.host", "localhost")
	v.SetDefault("redis.port", 6379)
	v.SetDefault("redis.database", 0)
	v.SetDefault("redis.pool_size", 10)
	v.SetDefault("redis.min_idle_conns", 2)
	
	// Elasticsearch defaults
	v.SetDefault("elasticsearch.url", "http://localhost:9200")
	v.SetDefault("elasticsearch.host", "localhost")
	v.SetDefault("elasticsearch.port", 9200)
	v.SetDefault("elasticsearch.communities_index", "communities")
	v.SetDefault("elasticsearch.stories_index", "stories")
	v.SetDefault("elasticsearch.search_index", "search_queries")
	
	// SMTP defaults
	v.SetDefault("smtp.host", "localhost")
	v.SetDefault("smtp.port", 1025)
	v.SetDefault("smtp.from", "noreply@resilience-mapping.org")
	v.SetDefault("smtp.use_tls", false)
	v.SetDefault("smtp.insecure_tls", true)
	
	// JWT defaults
	v.SetDefault("jwt.expiry", "24h")
	v.SetDefault("jwt.issuer", "resilience-mapping-api")
	v.SetDefault("jwt.algorithm", "HS256")
	
	// CORS defaults
	v.SetDefault("cors.allowed_methods", []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"})
	v.SetDefault("cors.allowed_headers", []string{"Origin", "Content-Type", "Accept", "Authorization", "X-Requested-With"})
	v.SetDefault("cors.allow_credentials", true)
	
	// Rate limiting defaults
	v.SetDefault("rate_limit.requests_per_minute", 60)
	v.SetDefault("rate_limit.burst_size", 10)
	v.SetDefault("rate_limit.search_limit", 100)
	v.SetDefault("rate_limit.download_limit", 10)
	v.SetDefault("rate_limit.contact_limit", 5)
	
	// Storage defaults
	v.SetDefault("storage.type", "local")
	v.SetDefault("storage.path", "./storage")
	v.SetDefault("storage.max_file_size", 10485760) // 10MB
	v.SetDefault("storage.allowed_types", []string{"image/jpeg", "image/png", "application/pdf"})
	
	// Metrics defaults
	v.SetDefault("metrics.enabled", true)
	v.SetDefault("metrics.port", 9090)
	v.SetDefault("metrics.path", "/metrics")
	
	// Logging defaults
	v.SetDefault("logging.level", "info")
	v.SetDefault("logging.format", "json")
	v.SetDefault("logging.output", "stdout")
}

// bindAPIEnvironmentVariables binds specific environment variables
func bindAPIEnvironmentVariables(v *viper.Viper) {
	// Database
	v.BindEnv("database.url", "DATABASE_URL")
	v.BindEnv("database.host", "DB_HOST")
	v.BindEnv("database.port", "DB_PORT")
	v.BindEnv("database.name", "DB_NAME")
	v.BindEnv("database.user", "DB_USER")
	v.BindEnv("database.password", "DB_PASSWORD")
	v.BindEnv("database.ssl_mode", "DB_SSL_MODE")
	
	// Redis
	v.BindEnv("redis.url", "REDIS_URL")
	v.BindEnv("redis.host", "REDIS_HOST")
	v.BindEnv("redis.port", "REDIS_PORT")
	v.BindEnv("redis.password", "REDIS_PASSWORD")
	v.BindEnv("redis.database", "REDIS_DB")
	
	// Elasticsearch
	v.BindEnv("elasticsearch.url", "ELASTICSEARCH_URL")
	v.BindEnv("elasticsearch.host", "ELASTICSEARCH_HOST")
	v.BindEnv("elasticsearch.port", "ELASTICSEARCH_PORT")
	v.BindEnv("elasticsearch.username", "ELASTICSEARCH_USERNAME")
	v.BindEnv("elasticsearch.password", "ELASTICSEARCH_PASSWORD")
	
	// SMTP
	v.BindEnv("smtp.host", "SMTP_HOST")
	v.BindEnv("smtp.port", "SMTP_PORT")
	v.BindEnv("smtp.user", "SMTP_USER")
	v.BindEnv("smtp.password", "SMTP_PASSWORD")
	v.BindEnv("smtp.from", "SMTP_FROM")
	
	// Application
	v.BindEnv("app.environment", "APP_ENV")
	v.BindEnv("app.port", "APP_PORT")
	v.BindEnv("app.debug", "APP_DEBUG")
	
	// JWT
	v.BindEnv("jwt.secret", "JWT_SECRET")
	v.BindEnv("jwt.expiry", "JWT_EXPIRY")
	
	// CORS
	v.BindEnv("cors.allowed_origins", "CORS_ALLOWED_ORIGINS")
	
	// Rate limiting
	v.BindEnv("rate_limit.requests_per_minute", "RATE_LIMIT_REQUESTS_PER_MINUTE")
	
	// Storage
	v.BindEnv("storage.type", "STORAGE_TYPE")
	v.BindEnv("storage.aws_region", "AWS_REGION")
	v.BindEnv("storage.aws_access_key_id", "AWS_ACCESS_KEY_ID")
	v.BindEnv("storage.aws_secret_access_key", "AWS_SECRET_ACCESS_KEY")
	v.BindEnv("storage.s3_bucket_name", "S3_BUCKET_NAME")
	
	// Metrics
	v.BindEnv("metrics.enabled", "ENABLE_METRICS")
	v.BindEnv("metrics.sentry_dsn", "SENTRY_DSN")
	
	// Logging
	v.BindEnv("logging.level", "LOG_LEVEL")
}

// setAPIEnvironmentDefaults sets environment-specific default values
func setAPIEnvironmentDefaults(cfg *APIConfig) {
	// Production-specific defaults
	if cfg.App.Environment == "production" {
		if cfg.Database.SSLMode == "disable" {
			cfg.Database.SSLMode = "require"
		}
		if cfg.SMTP.UseTLS == false {
			cfg.SMTP.UseTLS = true
		}
		if cfg.SMTP.InsecureTLS == true {
			cfg.SMTP.InsecureTLS = false
		}
	}
	
	// Development-specific defaults
	if cfg.App.Environment == "development" {
		// Allow all origins in development
		if len(cfg.CORS.AllowedOrigins) == 0 {
			cfg.CORS.AllowedOrigins = []string{
				"http://localhost:3000",
				"http://localhost:3001", 
				"http://localhost:3002",
			}
		}
		
		// Higher rate limits in development
		if cfg.RateLimit.RequestsPerMinute == 60 {
			cfg.RateLimit.RequestsPerMinute = 1000
		}
	}
	
	// Parse CORS origins from environment variable
	if originsEnv := os.Getenv("CORS_ALLOWED_ORIGINS"); originsEnv != "" {
		cfg.CORS.AllowedOrigins = strings.Split(originsEnv, ",")
	}
}

// validateAPIConfig validates the configuration
func validateAPIConfig(cfg *APIConfig) error {
	// Validate required fields
	if cfg.JWT.Secret == "" && cfg.App.Environment == "production" {
		return fmt.Errorf("JWT secret is required in production")
	}
	
	if cfg.Database.Password == "" && cfg.App.Environment == "production" {
		return fmt.Errorf("database password is required in production")
	}
	
	// Validate port ranges
	if cfg.App.Port < 1 || cfg.App.Port > 65535 {
		return fmt.Errorf("app port must be between 1 and 65535")
	}
	
	if cfg.Database.Port < 1 || cfg.Database.Port > 65535 {
		return fmt.Errorf("database port must be between 1 and 65535")
	}
	
	// Validate environment
	validEnvs := []string{"development", "staging", "production"}
	validEnv := false
	for _, env := range validEnvs {
		if cfg.App.Environment == env {
			validEnv = true
			break
		}
	}
	if !validEnv {
		return fmt.Errorf("environment must be one of: %s", strings.Join(validEnvs, ", "))
	}
	
	// Validate storage configuration
	if cfg.Storage.Type == "s3" {
		if cfg.Storage.AWSRegion == "" {
			return fmt.Errorf("AWS region is required for S3 storage")
		}
		if cfg.Storage.S3BucketName == "" {
			return fmt.Errorf("S3 bucket name is required for S3 storage")
		}
	}
	
	return nil
}

// GetDatabaseURL returns the database connection URL
func (cfg *APIConfig) GetDatabaseURL() string {
	if cfg.Database.URL != "" {
		return cfg.Database.URL
	}
	
	return fmt.Sprintf("postgres://%s:%s@%s:%d/%s?sslmode=%s",
		cfg.Database.User,
		cfg.Database.Password,
		cfg.Database.Host,
		cfg.Database.Port,
		cfg.Database.Name,
		cfg.Database.SSLMode,
	)
}

// GetRedisURL returns the Redis connection URL
func (cfg *APIConfig) GetRedisURL() string {
	if cfg.Redis.URL != "" {
		return cfg.Redis.URL
	}
	
	if cfg.Redis.Password != "" {
		return fmt.Sprintf("redis://:%s@%s:%d/%d",
			cfg.Redis.Password,
			cfg.Redis.Host,
			cfg.Redis.Port,
			cfg.Redis.Database,
		)
	}
	
	return fmt.Sprintf("redis://%s:%d/%d",
		cfg.Redis.Host,
		cfg.Redis.Port,
		cfg.Redis.Database,
	)
}

// GetElasticsearchURL returns the Elasticsearch connection URL
func (cfg *APIConfig) GetElasticsearchURL() string {
	if cfg.Elasticsearch.URL != "" {
		return cfg.Elasticsearch.URL
	}
	
	if cfg.Elasticsearch.Username != "" && cfg.Elasticsearch.Password != "" {
		return fmt.Sprintf("http://%s:%s@%s:%d",
			cfg.Elasticsearch.Username,
			cfg.Elasticsearch.Password,
			cfg.Elasticsearch.Host,
			cfg.Elasticsearch.Port,
		)
	}
	
	return fmt.Sprintf("http://%s:%d",
		cfg.Elasticsearch.Host,
		cfg.Elasticsearch.Port,
	)
}

// IsDevelopment returns true if running in development environment
func (cfg *APIConfig) IsDevelopment() bool {
	return cfg.App.Environment == "development"
}

// IsProduction returns true if running in production environment
func (cfg *APIConfig) IsProduction() bool {
	return cfg.App.Environment == "production"
}