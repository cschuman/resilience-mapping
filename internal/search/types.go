// Search types and data structures
// Created: January 31, 2025
// Purpose: Type definitions for search functionality

package search

import (
	"encoding/json"
	"time"
)

// Search parameters

// CommunitySearchParams defines parameters for community search
type CommunitySearchParams struct {
	Query                string
	State                string
	County               string
	MinResilienceScore   float64
	MaxResilienceScore   float64
	UnexpectedGoodOnly   bool
	MinPopulation        int
	MaxPopulation        int
	Limit                int
	Offset               int
	SortBy               string
}

// StorySearchParams defines parameters for story search
type StorySearchParams struct {
	Query       string
	CommunityID int
	Category    string
	StoryType   string
	Tags        []string
	Limit       int
	Offset      int
	SortBy      string
}

// Search documents (for indexing)

// CommunitySearchDocument represents a community in the search index
type CommunitySearchDocument struct {
	ID              int       `json:"id"`
	TractID         string    `json:"tract_id"`
	State           string    `json:"state"`
	County          string    `json:"county"`
	Name            string    `json:"name"`
	Population      int       `json:"population"`
	ResilienceScore float64   `json:"resilience_score"`
	UnexpectedGood  bool      `json:"unexpected_good"`
	StoryCount      int       `json:"story_count"`
	PrivacyLevel    string    `json:"privacy_level"`
	LastUpdated     time.Time `json:"last_updated"`
	Score           float64   `json:"_score,omitempty"`
}

// StorySearchDocument represents a story in the search index
type StorySearchDocument struct {
	ID            int        `json:"id"`
	CommunityID   int        `json:"community_id"`
	Title         string     `json:"title"`
	Summary       string     `json:"summary"`
	Content       string     `json:"content"`
	StoryType     string     `json:"story_type"`
	Category      string     `json:"category"`
	Tags          []string   `json:"tags"`
	Views         int        `json:"views"`
	Likes         int        `json:"likes"`
	PublishedAt   *time.Time `json:"published_at"`
	LastUpdated   time.Time  `json:"last_updated"`
	CommunityName string     `json:"community_name"`
	Score         float64    `json:"_score,omitempty"`
}

// UserSearchDocument represents a user in the search index (public data only)
type UserSearchDocument struct {
	ID           int    `json:"id"`
	DisplayName  string `json:"display_name"`
	UserType     string `json:"user_type"`
	Organization string `json:"organization"`
	Bio          string `json:"bio"`
	PrivacyLevel string `json:"privacy_level"`
	Score        float64 `json:"_score,omitempty"`
}

// Search results

// CommunitySearchResults contains community search results
type CommunitySearchResults struct {
	Total       int64                      `json:"total"`
	Communities []CommunitySearchDocument  `json:"communities"`
	Took        int                        `json:"took"`
	Aggregations map[string]interface{}    `json:"aggregations,omitempty"`
}

// StorySearchResults contains story search results
type StorySearchResults struct {
	Total        int64                   `json:"total"`
	Stories      []StorySearchDocument   `json:"stories"`
	Took         int                     `json:"took"`
	Aggregations map[string]interface{}  `json:"aggregations,omitempty"`
}

// GlobalSearchResults contains results from searching across all indices
type GlobalSearchResults struct {
	Query       string                    `json:"query"`
	Total       int64                     `json:"total"`
	Communities []CommunitySearchDocument `json:"communities"`
	Stories     []StorySearchDocument     `json:"stories"`
	Users       []UserSearchDocument      `json:"users,omitempty"`
}

// SearchSuggestions contains autocomplete suggestions
type SearchSuggestions struct {
	Communities []string `json:"communities"`
	Stories     []string `json:"stories"`
	Tags        []string `json:"tags"`
}

// SearchFacets contains faceted search results
type SearchFacets struct {
	States         map[string]int64 `json:"states"`
	Categories     map[string]int64 `json:"categories"`
	StoryTypes     map[string]int64 `json:"story_types"`
	Tags           map[string]int64 `json:"tags"`
	ResilienceRanges map[string]int64 `json:"resilience_ranges"`
}

// Elasticsearch response structures

// ElasticsearchResponse represents the raw Elasticsearch response
type ElasticsearchResponse struct {
	Took     int                    `json:"took"`
	TimedOut bool                   `json:"timed_out"`
	Hits     ElasticsearchHits      `json:"hits"`
	Suggest  map[string]interface{} `json:"suggest,omitempty"`
}

// ElasticsearchHits represents the hits section of ES response
type ElasticsearchHits struct {
	Total ElasticsearchTotal `json:"total"`
	Hits  []ElasticsearchHit `json:"hits"`
}

// ElasticsearchTotal represents the total hits information
type ElasticsearchTotal struct {
	Value    int64  `json:"value"`
	Relation string `json:"relation"`
}

// ElasticsearchHit represents a single search hit
type ElasticsearchHit struct {
	Index  string          `json:"_index"`
	Type   string          `json:"_type"`
	ID     string          `json:"_id"`
	Score  float64         `json:"_score"`
	Source json.RawMessage `json:"_source"`
}

// Search analytics

// SearchAnalytics tracks search usage and performance
type SearchAnalytics struct {
	Query           string        `json:"query"`
	Index           string        `json:"index"`
	ResultCount     int64         `json:"result_count"`
	Duration        time.Duration `json:"duration"`
	UserID          int           `json:"user_id,omitempty"`
	UserType        string        `json:"user_type,omitempty"`
	IPAddress       string        `json:"ip_address,omitempty"`
	Timestamp       time.Time     `json:"timestamp"`
	ClickedResults  []int         `json:"clicked_results,omitempty"`
}

// Search configuration

// SearchConfig contains search-specific configuration
type SearchConfig struct {
	DefaultLimit        int               `json:"default_limit"`
	MaxLimit           int               `json:"max_limit"`
	EnableSuggestions  bool              `json:"enable_suggestions"`
	EnableAnalytics    bool              `json:"enable_analytics"`
	CacheEnabled       bool              `json:"cache_enabled"`
	CacheTTL           time.Duration     `json:"cache_ttl"`
	IndexSettings      map[string]interface{} `json:"index_settings"`
}

// Search filters

// SearchFilter represents a single search filter
type SearchFilter struct {
	Field    string      `json:"field"`
	Operator string      `json:"operator"` // eq, ne, gt, gte, lt, lte, in, nin
	Value    interface{} `json:"value"`
}

// SearchSort represents sorting criteria
type SearchSort struct {
	Field string `json:"field"`
	Order string `json:"order"` // asc, desc
}

// Advanced search parameters

// AdvancedSearchParams provides more complex search capabilities
type AdvancedSearchParams struct {
	Query         string         `json:"query"`
	Filters       []SearchFilter `json:"filters"`
	Sort          []SearchSort   `json:"sort"`
	Facets        []string       `json:"facets"`
	Limit         int            `json:"limit"`
	Offset        int            `json:"offset"`
	HighlightFields []string     `json:"highlight_fields"`
	IncludeAggregations bool     `json:"include_aggregations"`
}

// Bulk operations

// BulkIndexRequest represents a bulk indexing request
type BulkIndexRequest struct {
	Index     string      `json:"index"`
	Documents []BulkDocument `json:"documents"`
}

// BulkDocument represents a document for bulk operations
type BulkDocument struct {
	ID     string      `json:"id"`
	Action string      `json:"action"` // index, update, delete
	Source interface{} `json:"source"`
}

// BulkIndexResponse represents the response from bulk operations
type BulkIndexResponse struct {
	Took    int                    `json:"took"`
	Errors  bool                   `json:"errors"`
	Items   []BulkResponseItem     `json:"items"`
}

// BulkResponseItem represents a single item in bulk response
type BulkResponseItem struct {
	Index  BulkItemResult `json:"index,omitempty"`
	Update BulkItemResult `json:"update,omitempty"`
	Delete BulkItemResult `json:"delete,omitempty"`
}

// BulkItemResult represents the result of a single bulk item
type BulkItemResult struct {
	ID     string `json:"_id"`
	Status int    `json:"status"`
	Error  string `json:"error,omitempty"`
}

// Search health and monitoring

// SearchHealth represents the health status of search functionality
type SearchHealth struct {
	Status          string            `json:"status"`
	ClusterStatus   string            `json:"cluster_status"`
	ActiveShards    int               `json:"active_shards"`
	NumberOfNodes   int               `json:"number_of_nodes"`
	Indices         map[string]IndexHealth `json:"indices"`
	LastChecked     time.Time         `json:"last_checked"`
}

// IndexHealth represents the health of a specific index
type IndexHealth struct {
	Status       string `json:"status"`
	DocumentCount int64  `json:"document_count"`
	StoreSize    string `json:"store_size"`
	LastUpdated  time.Time `json:"last_updated"`
}

// Community-specific search features

// CommunitySearchContext provides context for community-aware searches
type CommunitySearchContext struct {
	UserCommunityID *int   `json:"user_community_id,omitempty"`
	UserRole        string `json:"user_role"`
	UserType        string `json:"user_type"`
	PrivacyFilter   string `json:"privacy_filter"`
	IncludePrivate  bool   `json:"include_private"`
}

// ResilienceSearchParams provides search parameters specific to resilience data
type ResilienceSearchParams struct {
	MinResilienceScore    float64 `json:"min_resilience_score"`
	MaxResilienceScore    float64 `json:"max_resilience_score"`
	UnexpectedGoodOnly    bool    `json:"unexpected_good_only"`
	HealthOutcomeMin      float64 `json:"health_outcome_min"`
	HealthOutcomeMax      float64 `json:"health_outcome_max"`
	FoodAccessMin         float64 `json:"food_access_min"`
	FoodAccessMax         float64 `json:"food_access_max"`
	PopulationMin         int     `json:"population_min"`
	PopulationMax         int     `json:"population_max"`
	StoryCountMin         int     `json:"story_count_min"`
}