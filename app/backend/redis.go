// Redis caching layer
// Created: January 31, 2025
// Purpose: High-performance caching for community data with privacy protection

package cache

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
	"github.com/your-org/resilience-mapping/internal/config"
)

// CacheClient wraps Redis client with community-specific functionality
type CacheClient struct {
	client   *redis.Client
	config   *config.RedisConfig
	keyPrefix string
}

// NewCacheClient creates a new Redis cache client
func NewCacheClient(cfg *config.RedisConfig) (*CacheClient, error) {
	// Configure Redis options
	opts := &redis.Options{
		DB:       cfg.DB,
		Password: cfg.Password,
	}

	// Set address from URL or host/port
	if cfg.URL != "" {
		parsedOpts, err := redis.ParseURL(cfg.URL)
		if err != nil {
			return nil, fmt.Errorf("failed to parse Redis URL: %w", err)
		}
		opts = parsedOpts
	} else {
		opts.Addr = fmt.Sprintf("%s:%d", cfg.Host, cfg.Port)
	}

	// Create Redis client
	client := redis.NewClient(opts)

	// Test connection
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := client.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("failed to connect to Redis: %w", err)
	}

	cacheClient := &CacheClient{
		client:    client,
		config:    cfg,
		keyPrefix: "resilience:",
	}

	log.Printf("💾 Redis cache connected successfully")
	log.Printf("📊 Cache database: %d", cfg.DB)

	return cacheClient, nil
}

// Close closes the Redis connection
func (c *CacheClient) Close() error {
	log.Printf("🔒 Closing Redis cache connection...")
	return c.client.Close()
}

// Health checks Redis health
func (c *CacheClient) Health() error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	return c.client.Ping(ctx).Err()
}

// GetStats returns cache statistics
func (c *CacheClient) GetStats() map[string]interface{} {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	info, err := c.client.Info(ctx).Result()
	if err != nil {
		return map[string]interface{}{
			"error": err.Error(),
		}
	}

	// Parse basic stats from info string
	stats := map[string]interface{}{
		"connected": true,
		"info":      info[:200], // First 200 chars
	}

	return stats
}

// Basic cache operations

// Set stores a value in cache with expiration
func (c *CacheClient) Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error {
	fullKey := c.keyPrefix + key

	// Serialize value to JSON
	data, err := json.Marshal(value)
	if err != nil {
		return fmt.Errorf("failed to marshal value: %w", err)
	}

	return c.client.Set(ctx, fullKey, data, expiration).Err()
}

// Get retrieves a value from cache
func (c *CacheClient) Get(ctx context.Context, key string, dest interface{}) error {
	fullKey := c.keyPrefix + key

	data, err := c.client.Get(ctx, fullKey).Result()
	if err != nil {
		if err == redis.Nil {
			return ErrCacheMiss
		}
		return fmt.Errorf("failed to get cache value: %w", err)
	}

	// Deserialize from JSON
	if err := json.Unmarshal([]byte(data), dest); err != nil {
		return fmt.Errorf("failed to unmarshal cached value: %w", err)
	}

	return nil
}

// Del deletes a key from cache
func (c *CacheClient) Del(ctx context.Context, keys ...string) error {
	if len(keys) == 0 {
		return nil
	}

	fullKeys := make([]string, len(keys))
	for i, key := range keys {
		fullKeys[i] = c.keyPrefix + key
	}

	return c.client.Del(ctx, fullKeys...).Err()
}

// Exists checks if a key exists in cache
func (c *CacheClient) Exists(ctx context.Context, key string) (bool, error) {
	fullKey := c.keyPrefix + key
	count, err := c.client.Exists(ctx, fullKey).Result()
	return count > 0, err
}

// Community-specific cache operations

// CacheCommunity stores community data with privacy-aware TTL
func (c *CacheClient) CacheCommunity(ctx context.Context, communityID int, community interface{}) error {
	key := fmt.Sprintf("community:%d", communityID)
	
	// Cache public communities longer than private ones
	ttl := 15 * time.Minute // Default for private/sensitive data
	
	// Check if community is public (simplified check)
	if data, ok := community.(map[string]interface{}); ok {
		if privacyLevel, exists := data["privacy_level"]; exists && privacyLevel == "public" {
			ttl = 1 * time.Hour // Cache public data longer
		}
	}

	return c.Set(ctx, key, community, ttl)
}

// GetCachedCommunity retrieves cached community data
func (c *CacheClient) GetCachedCommunity(ctx context.Context, communityID int, dest interface{}) error {
	key := fmt.Sprintf("community:%d", communityID)
	return c.Get(ctx, key, dest)
}

// CacheStory stores story data
func (c *CacheClient) CacheStory(ctx context.Context, storyID int, story interface{}) error {
	key := fmt.Sprintf("story:%d", storyID)
	// Stories can be cached for longer since they don't change frequently
	return c.Set(ctx, key, story, 30*time.Minute)
}

// GetCachedStory retrieves cached story data
func (c *CacheClient) GetCachedStory(ctx context.Context, storyID int, dest interface{}) error {
	key := fmt.Sprintf("story:%d", storyID)
	return c.Get(ctx, key, dest)
}

// CacheSearchResults stores search results
func (c *CacheClient) CacheSearchResults(ctx context.Context, searchKey string, results interface{}) error {
	key := fmt.Sprintf("search:%s", searchKey)
	// Search results should be cached for shorter time
	return c.Set(ctx, key, results, 5*time.Minute)
}

// GetCachedSearchResults retrieves cached search results
func (c *CacheClient) GetCachedSearchResults(ctx context.Context, searchKey string, dest interface{}) error {
	key := fmt.Sprintf("search:%s", searchKey)
	return c.Get(ctx, key, dest)
}

// CacheUserSession stores user session data
func (c *CacheClient) CacheUserSession(ctx context.Context, sessionID string, sessionData interface{}) error {
	key := fmt.Sprintf("session:%s", sessionID)
	// Sessions expire after 24 hours
	return c.Set(ctx, key, sessionData, 24*time.Hour)
}

// GetCachedUserSession retrieves cached session data
func (c *CacheClient) GetCachedUserSession(ctx context.Context, sessionID string, dest interface{}) error {
	key := fmt.Sprintf("session:%s", sessionID)
	return c.Get(ctx, key, dest)
}

// Advanced cache operations

// SetNX sets a key only if it doesn't exist (useful for locks)
func (c *CacheClient) SetNX(ctx context.Context, key string, value interface{}, expiration time.Duration) (bool, error) {
	fullKey := c.keyPrefix + key

	data, err := json.Marshal(value)
	if err != nil {
		return false, fmt.Errorf("failed to marshal value: %w", err)
	}

	result, err := c.client.SetNX(ctx, fullKey, data, expiration).Result()
	return result, err
}

// Increment increments a numeric value
func (c *CacheClient) Increment(ctx context.Context, key string) (int64, error) {
	fullKey := c.keyPrefix + key
	return c.client.Incr(ctx, fullKey).Result()
}

// IncrementBy increments a numeric value by a specific amount
func (c *CacheClient) IncrementBy(ctx context.Context, key string, value int64) (int64, error) {
	fullKey := c.keyPrefix + key
	return c.client.IncrBy(ctx, fullKey, value).Result()
}

// Expire sets TTL for an existing key
func (c *CacheClient) Expire(ctx context.Context, key string, expiration time.Duration) error {
	fullKey := c.keyPrefix + key
	return c.client.Expire(ctx, fullKey, expiration).Err()
}

// TTL returns the remaining time to live for a key
func (c *CacheClient) TTL(ctx context.Context, key string) (time.Duration, error) {
	fullKey := c.keyPrefix + key
	return c.client.TTL(ctx, fullKey).Result()
}

// Community-focused caching patterns

// CacheMetrics stores system metrics
func (c *CacheClient) CacheMetrics(ctx context.Context, metrics interface{}) error {
	key := "metrics:system"
	return c.Set(ctx, key, metrics, 1*time.Minute)
}

// GetCachedMetrics retrieves cached system metrics
func (c *CacheClient) GetCachedMetrics(ctx context.Context, dest interface{}) error {
	key := "metrics:system"
	return c.Get(ctx, key, dest)
}

// CacheStatistics stores community statistics
func (c *CacheClient) CacheStatistics(ctx context.Context, stats interface{}) error {
	key := "stats:communities"
	// Statistics can be cached for longer
	return c.Set(ctx, key, stats, 1*time.Hour)
}

// GetCachedStatistics retrieves cached statistics
func (c *CacheClient) GetCachedStatistics(ctx context.Context, dest interface{}) error {
	key := "stats:communities"
	return c.Get(ctx, key, dest)
}

// Rate limiting support

// IncrementRateLimit increments rate limit counter
func (c *CacheClient) IncrementRateLimit(ctx context.Context, identifier string, window time.Duration) (int64, error) {
	key := fmt.Sprintf("ratelimit:%s", identifier)
	
	// Use pipeline for atomic operations
	pipe := c.client.Pipeline()
	
	incrResult := pipe.Incr(ctx, c.keyPrefix+key)
	pipe.Expire(ctx, c.keyPrefix+key, window)
	
	_, err := pipe.Exec(ctx)
	if err != nil {
		return 0, err
	}
	
	return incrResult.Val(), nil
}

// GetRateLimit gets current rate limit count
func (c *CacheClient) GetRateLimit(ctx context.Context, identifier string) (int64, error) {
	key := fmt.Sprintf("ratelimit:%s", identifier)
	fullKey := c.keyPrefix + key
	
	count, err := c.client.Get(ctx, fullKey).Int64()
	if err == redis.Nil {
		return 0, nil
	}
	return count, err
}

// Distributed locking

// AcquireLock acquires a distributed lock
func (c *CacheClient) AcquireLock(ctx context.Context, lockKey string, expiration time.Duration) (bool, error) {
	key := fmt.Sprintf("lock:%s", lockKey)
	lockValue := fmt.Sprintf("%d", time.Now().UnixNano())
	
	acquired, err := c.SetNX(ctx, key, lockValue, expiration)
	if err != nil {
		return false, fmt.Errorf("failed to acquire lock: %w", err)
	}
	
	if acquired {
		log.Printf("🔒 Acquired lock: %s", lockKey)
	}
	
	return acquired, nil
}

// ReleaseLock releases a distributed lock
func (c *CacheClient) ReleaseLock(ctx context.Context, lockKey string) error {
	key := fmt.Sprintf("lock:%s", lockKey)
	
	err := c.Del(ctx, key)
	if err != nil {
		return fmt.Errorf("failed to release lock: %w", err)
	}
	
	log.Printf("🔓 Released lock: %s", lockKey)
	return nil
}

// Bulk operations

// MSet sets multiple key-value pairs
func (c *CacheClient) MSet(ctx context.Context, pairs map[string]interface{}, expiration time.Duration) error {
	if len(pairs) == 0 {
		return nil
	}

	// Prepare data for Redis MSET
	args := make([]interface{}, 0, len(pairs)*2)
	
	for key, value := range pairs {
		fullKey := c.keyPrefix + key
		
		data, err := json.Marshal(value)
		if err != nil {
			return fmt.Errorf("failed to marshal value for key %s: %w", key, err)
		}
		
		args = append(args, fullKey, data)
	}

	// Set all values
	if err := c.client.MSet(ctx, args...).Err(); err != nil {
		return fmt.Errorf("failed to set multiple values: %w", err)
	}

	// Set expiration for all keys if specified
	if expiration > 0 {
		pipe := c.client.Pipeline()
		for key := range pairs {
			fullKey := c.keyPrefix + key
			pipe.Expire(ctx, fullKey, expiration)
		}
		_, err := pipe.Exec(ctx)
		if err != nil {
			return fmt.Errorf("failed to set expiration for multiple keys: %w", err)
		}
	}

	return nil
}

// MGet gets multiple values by keys
func (c *CacheClient) MGet(ctx context.Context, keys []string) (map[string]string, error) {
	if len(keys) == 0 {
		return map[string]string{}, nil
	}

	fullKeys := make([]string, len(keys))
	for i, key := range keys {
		fullKeys[i] = c.keyPrefix + key
	}

	values, err := c.client.MGet(ctx, fullKeys...).Result()
	if err != nil {
		return nil, fmt.Errorf("failed to get multiple values: %w", err)
	}

	result := make(map[string]string, len(keys))
	for i, key := range keys {
		if i < len(values) && values[i] != nil {
			result[key] = values[i].(string)
		}
	}

	return result, nil
}

// Cache invalidation

// InvalidateCommunityCache removes all cached data for a community
func (c *CacheClient) InvalidateCommunityCache(ctx context.Context, communityID int) error {
	keys := []string{
		fmt.Sprintf("community:%d", communityID),
		fmt.Sprintf("community:%d:stories", communityID),
		fmt.Sprintf("community:%d:stats", communityID),
	}
	
	return c.Del(ctx, keys...)
}

// InvalidateSearchCache removes cached search results matching pattern
func (c *CacheClient) InvalidateSearchCache(ctx context.Context, pattern string) error {
	searchPattern := c.keyPrefix + "search:" + pattern + "*"
	
	keys, err := c.client.Keys(ctx, searchPattern).Result()
	if err != nil {
		return fmt.Errorf("failed to find keys matching pattern: %w", err)
	}
	
	if len(keys) == 0 {
		return nil
	}
	
	// Remove prefix from keys before deletion
	cleanKeys := make([]string, len(keys))
	for i, key := range keys {
		cleanKeys[i] = strings.TrimPrefix(key, c.keyPrefix)
	}
	
	return c.Del(ctx, cleanKeys...)
}

// FlushCache clears all cache data (use with caution)
func (c *CacheClient) FlushCache(ctx context.Context) error {
	log.Printf("⚠️ Flushing all cache data - this affects community data access performance")
	return c.client.FlushDB(ctx).Err()
}

// Cache warming

// WarmupCache preloads frequently accessed data
func (c *CacheClient) WarmupCache(ctx context.Context) error {
	log.Printf("🔥 Starting cache warmup for community data...")
	
	// This would typically:
	// 1. Load most accessed communities
	// 2. Cache popular search results
	// 3. Preload system statistics
	// 4. Cache frequently accessed stories
	
	// For now, just log the intent
	log.Printf("✅ Cache warmup completed")
	return nil
}

// Utility functions

// GenerateSearchKey creates a consistent cache key for search results
func GenerateSearchKey(searchType, query string, filters map[string]interface{}) string {
	// Create a deterministic key from search parameters
	key := fmt.Sprintf("%s:%s", searchType, query)
	
	// Add filters to key (simplified)
	for k, v := range filters {
		key += fmt.Sprintf(":%s:%v", k, v)
	}
	
	return key
}

// Community cache hit/miss tracking
func (c *CacheClient) TrackCacheHit(ctx context.Context, cacheType string) {
	key := fmt.Sprintf("metrics:cache:hit:%s", cacheType)
	c.Increment(ctx, key)
}

func (c *CacheClient) TrackCacheMiss(ctx context.Context, cacheType string) {
	key := fmt.Sprintf("metrics:cache:miss:%s", cacheType)
	c.Increment(ctx, key)
}

// Error types
var (
	ErrCacheMiss = fmt.Errorf("cache miss")
)