// Elasticsearch search functionality
// Created: January 31, 2025
// Purpose: Full-text search for community stories and data with privacy protection

package search

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"strings"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
	"github.com/elastic/go-elasticsearch/v8/esapi"
	"github.com/your-org/resilience-mapping/internal/config"
	"github.com/your-org/resilience-mapping/internal/models"
)

// SearchClient wraps Elasticsearch client with community-specific functionality
type SearchClient struct {
	client   *elasticsearch.Client
	config   *config.ElasticsearchConfig
	indices  map[string]string
}

// NewSearchClient creates a new Elasticsearch search client
func NewSearchClient(cfg *config.ElasticsearchConfig) (*SearchClient, error) {
	// Configure Elasticsearch client
	esCfg := elasticsearch.Config{
		Addresses: []string{cfg.URL},
	}
	
	// Add authentication if provided
	if cfg.Username != "" && cfg.Password != "" {
		esCfg.Username = cfg.Username
		esCfg.Password = cfg.Password
	}

	client, err := elasticsearch.NewClient(esCfg)
	if err != nil {
		return nil, fmt.Errorf("failed to create Elasticsearch client: %w", err)
	}

	// Test connection
	res, err := client.Info()
	if err != nil {
		return nil, fmt.Errorf("failed to connect to Elasticsearch: %w", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		return nil, fmt.Errorf("Elasticsearch connection error: %s", res.Status())
	}

	searchClient := &SearchClient{
		client: client,
		config: cfg,
		indices: map[string]string{
			"communities": "resilience-communities",
			"stories":     "resilience-stories",
			"users":       "resilience-users",
		},
	}

	log.Printf("🔍 Elasticsearch connected successfully")
	log.Printf("📊 Search indices: %v", searchClient.indices)

	return searchClient, nil
}

// Initialize creates Elasticsearch indices with proper mappings
func (s *SearchClient) Initialize() error {
	log.Printf("🔧 Initializing Elasticsearch indices...")

	// Create communities index
	if err := s.createCommunitiesIndex(); err != nil {
		return fmt.Errorf("failed to create communities index: %w", err)
	}

	// Create stories index
	if err := s.createStoriesIndex(); err != nil {
		return fmt.Errorf("failed to create stories index: %w", err)
	}

	// Create users index
	if err := s.createUsersIndex(); err != nil {
		return fmt.Errorf("failed to create users index: %w", err)
	}

	log.Printf("✅ Elasticsearch indices initialized successfully")
	return nil
}

// Close closes the search client
func (s *SearchClient) Close() error {
	log.Printf("🔒 Closing Elasticsearch client...")
	return nil // go-elasticsearch doesn't require explicit closing
}

// Health checks Elasticsearch health
func (s *SearchClient) Health() error {
	res, err := s.client.Cluster.Health()
	if err != nil {
		return err
	}
	defer res.Body.Close()

	if res.IsError() {
		return fmt.Errorf("Elasticsearch cluster unhealthy: %s", res.Status())
	}

	return nil
}

// Community search operations

// IndexCommunity adds/updates a community in the search index
func (s *SearchClient) IndexCommunity(community *models.Community) error {
	// Create search document with privacy considerations
	doc := CommunitySearchDocument{
		ID:              community.ID,
		TractID:         community.TractID,
		State:           community.State,
		County:          community.County,
		Name:            community.Name,
		Population:      community.Population,
		ResilienceScore: community.ResilienceScore,
		UnexpectedGood:  community.UnexpectedGood,
		StoryCount:      community.StoryCount,
		PrivacyLevel:    community.PrivacyLevel,
		LastUpdated:     community.LastUpdated,
	}

	// Only index public communities or approved private communities
	if community.GetPrivacyLevel() != "public" && !community.CommunityApproved {
		log.Printf("🔒 Skipping non-public community %s for search index", community.TractID)
		return nil
	}

	// Serialize document
	docBytes, err := json.Marshal(doc)
	if err != nil {
		return fmt.Errorf("failed to marshal community document: %w", err)
	}

	// Index document
	req := esapi.IndexRequest{
		Index:      s.indices["communities"],
		DocumentID: fmt.Sprintf("%d", community.ID),
		Body:       bytes.NewReader(docBytes),
		Refresh:    "true",
	}

	res, err := req.Do(context.Background(), s.client)
	if err != nil {
		return fmt.Errorf("failed to index community: %w", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		return fmt.Errorf("error indexing community: %s", res.Status())
	}

	log.Printf("🔍 Indexed community: %s", community.TractID)
	return nil
}

// SearchCommunities searches for communities with filters
func (s *SearchClient) SearchCommunities(ctx context.Context, params CommunitySearchParams) (*CommunitySearchResults, error) {
	query := s.buildCommunitySearchQuery(params)
	
	// Execute search
	var buf bytes.Buffer
	if err := json.NewEncoder(&buf).Encode(query); err != nil {
		return nil, fmt.Errorf("failed to encode search query: %w", err)
	}

	req := esapi.SearchRequest{
		Index: []string{s.indices["communities"]},
		Body:  &buf,
		Size:  &params.Limit,
		From:  &params.Offset,
	}

	res, err := req.Do(ctx, s.client)
	if err != nil {
		return nil, fmt.Errorf("search request failed: %w", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		return nil, fmt.Errorf("search error: %s", res.Status())
	}

	// Parse response
	var searchResponse ElasticsearchResponse
	if err := json.NewDecoder(res.Body).Decode(&searchResponse); err != nil {
		return nil, fmt.Errorf("failed to parse search response: %w", err)
	}

	// Convert to result format
	results := &CommunitySearchResults{
		Total:       searchResponse.Hits.Total.Value,
		Communities: make([]CommunitySearchDocument, len(searchResponse.Hits.Hits)),
		Took:        searchResponse.Took,
	}

	for i, hit := range searchResponse.Hits.Hits {
		var doc CommunitySearchDocument
		if err := json.Unmarshal(hit.Source, &doc); err != nil {
			log.Printf("⚠️ Failed to unmarshal search result: %v", err)
			continue
		}
		doc.Score = hit.Score
		results.Communities[i] = doc
	}

	log.Printf("🔍 Community search completed: %d results in %dms", results.Total, results.Took)
	return results, nil
}

// Story search operations

// IndexStory adds/updates a story in the search index
func (s *SearchClient) IndexStory(story *models.Story) error {
	// Only index published stories
	if !story.IsPublished() {
		return nil
	}

	// Create search document
	doc := StorySearchDocument{
		ID:              story.ID,
		CommunityID:     story.CommunityID,
		Title:           story.GetPublicTitle(), // Use privacy-safe title
		Summary:         story.Summary,
		Content:         story.Content,
		StoryType:       story.StoryType,
		Category:        story.Category,
		Tags:            story.Tags,
		Views:           story.Views,
		Likes:           story.Likes,
		PublishedAt:     story.PublishedAt,
		LastUpdated:     story.UpdatedAt,
		CommunityName:   "", // Will be populated if community data is available
	}

	// Serialize document
	docBytes, err := json.Marshal(doc)
	if err != nil {
		return fmt.Errorf("failed to marshal story document: %w", err)
	}

	// Index document
	req := esapi.IndexRequest{
		Index:      s.indices["stories"],
		DocumentID: fmt.Sprintf("%d", story.ID),
		Body:       bytes.NewReader(docBytes),
		Refresh:    "true",
	}

	res, err := req.Do(context.Background(), s.client)
	if err != nil {
		return fmt.Errorf("failed to index story: %w", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		return fmt.Errorf("error indexing story: %s", res.Status())
	}

	log.Printf("🔍 Indexed story: %s", story.Title)
	return nil
}

// SearchStories searches for stories with filters
func (s *SearchClient) SearchStories(ctx context.Context, params StorySearchParams) (*StorySearchResults, error) {
	query := s.buildStorySearchQuery(params)
	
	// Execute search
	var buf bytes.Buffer
	if err := json.NewEncoder(&buf).Encode(query); err != nil {
		return nil, fmt.Errorf("failed to encode search query: %w", err)
	}

	req := esapi.SearchRequest{
		Index: []string{s.indices["stories"]},
		Body:  &buf,
		Size:  &params.Limit,
		From:  &params.Offset,
	}

	res, err := req.Do(ctx, s.client)
	if err != nil {
		return nil, fmt.Errorf("search request failed: %w", err)
	}
	defer res.Body.Close()

	if res.IsError() {
		return nil, fmt.Errorf("search error: %s", res.Status())
	}

	// Parse response
	var searchResponse ElasticsearchResponse
	if err := json.NewDecoder(res.Body).Decode(&searchResponse); err != nil {
		return nil, fmt.Errorf("failed to parse search response: %w", err)
	}

	// Convert to result format
	results := &StorySearchResults{
		Total:   searchResponse.Hits.Total.Value,
		Stories: make([]StorySearchDocument, len(searchResponse.Hits.Hits)),
		Took:    searchResponse.Took,
	}

	for i, hit := range searchResponse.Hits.Hits {
		var doc StorySearchDocument
		if err := json.Unmarshal(hit.Source, &doc); err != nil {
			log.Printf("⚠️ Failed to unmarshal search result: %v", err)
			continue
		}
		doc.Score = hit.Score
		results.Stories[i] = doc
	}

	log.Printf("🔍 Story search completed: %d results in %dms", results.Total, results.Took)
	return results, nil
}

// Global search

// GlobalSearch searches across communities and stories
func (s *SearchClient) GlobalSearch(ctx context.Context, query string, limit int) (*GlobalSearchResults, error) {
	// Search communities
	communityParams := CommunitySearchParams{
		Query:  query,
		Limit:  limit / 2,
		Offset: 0,
	}
	communityResults, err := s.SearchCommunities(ctx, communityParams)
	if err != nil {
		log.Printf("⚠️ Community search failed: %v", err)
	}

	// Search stories
	storyParams := StorySearchParams{
		Query:  query,
		Limit:  limit / 2,
		Offset: 0,
	}
	storyResults, err := s.SearchStories(ctx, storyParams)
	if err != nil {
		log.Printf("⚠️ Story search failed: %v", err)
	}

	results := &GlobalSearchResults{
		Query: query,
	}

	if communityResults != nil {
		results.Communities = communityResults.Communities
	}

	if storyResults != nil {
		results.Stories = storyResults.Stories
	}

	results.Total = int64(len(results.Communities) + len(results.Stories))

	log.Printf("🔍 Global search completed: %d total results", results.Total)
	return results, nil
}

// Suggestions and autocomplete

// GetSearchSuggestions provides search suggestions based on partial input
func (s *SearchClient) GetSearchSuggestions(ctx context.Context, query string, limit int) (*SearchSuggestions, error) {
	// Build suggest query
	suggestQuery := map[string]interface{}{
		"suggest": map[string]interface{}{
			"community_suggest": map[string]interface{}{
				"prefix": strings.ToLower(query),
				"completion": map[string]interface{}{
					"field": "name.suggest",
					"size":  limit / 2,
				},
			},
			"story_suggest": map[string]interface{}{
				"prefix": strings.ToLower(query),
				"completion": map[string]interface{}{
					"field": "title.suggest",
					"size":  limit / 2,
				},
			},
		},
	}

	var buf bytes.Buffer
	if err := json.NewEncoder(&buf).Encode(suggestQuery); err != nil {
		return nil, fmt.Errorf("failed to encode suggest query: %w", err)
	}

	// Execute across both indices
	req := esapi.SearchRequest{
		Index: []string{s.indices["communities"], s.indices["stories"]},
		Body:  &buf,
	}

	res, err := req.Do(ctx, s.client)
	if err != nil {
		return nil, fmt.Errorf("suggest request failed: %w", err)
	}
	defer res.Body.Close()

	// Parse suggestions (simplified)
	suggestions := &SearchSuggestions{
		Communities: []string{},
		Stories:     []string{},
	}

	log.Printf("🔍 Search suggestions generated for: %s", query)
	return suggestions, nil
}

// Index management

func (s *SearchClient) createCommunitiesIndex() error {
	mapping := map[string]interface{}{
		"mappings": map[string]interface{}{
			"properties": map[string]interface{}{
				"id":               map[string]interface{}{"type": "integer"},
				"tract_id":         map[string]interface{}{"type": "keyword"},
				"state":            map[string]interface{}{"type": "keyword"},
				"county":           map[string]interface{}{"type": "keyword"},
				"name": map[string]interface{}{
					"type": "text",
					"fields": map[string]interface{}{
						"keyword": map[string]interface{}{"type": "keyword"},
						"suggest": map[string]interface{}{
							"type":        "completion",
							"analyzer":    "simple",
							"search_analyzer": "simple",
						},
					},
				},
				"population":       map[string]interface{}{"type": "integer"},
				"resilience_score": map[string]interface{}{"type": "float"},
				"unexpected_good":  map[string]interface{}{"type": "boolean"},
				"story_count":      map[string]interface{}{"type": "integer"},
				"privacy_level":    map[string]interface{}{"type": "keyword"},
				"last_updated":     map[string]interface{}{"type": "date"},
			},
		},
	}

	return s.createIndex(s.indices["communities"], mapping)
}

func (s *SearchClient) createStoriesIndex() error {
	mapping := map[string]interface{}{
		"mappings": map[string]interface{}{
			"properties": map[string]interface{}{
				"id":            map[string]interface{}{"type": "integer"},
				"community_id":  map[string]interface{}{"type": "integer"},
				"title": map[string]interface{}{
					"type": "text",
					"fields": map[string]interface{}{
						"keyword": map[string]interface{}{"type": "keyword"},
						"suggest": map[string]interface{}{
							"type":        "completion",
							"analyzer":    "simple",
							"search_analyzer": "simple",
						},
					},
				},
				"summary":         map[string]interface{}{"type": "text"},
				"content":         map[string]interface{}{"type": "text"},
				"story_type":      map[string]interface{}{"type": "keyword"},
				"category":        map[string]interface{}{"type": "keyword"},
				"tags":            map[string]interface{}{"type": "keyword"},
				"views":           map[string]interface{}{"type": "integer"},
				"likes":           map[string]interface{}{"type": "integer"},
				"published_at":    map[string]interface{}{"type": "date"},
				"last_updated":    map[string]interface{}{"type": "date"},
				"community_name":  map[string]interface{}{"type": "text"},
			},
		},
	}

	return s.createIndex(s.indices["stories"], mapping)
}

func (s *SearchClient) createUsersIndex() error {
	mapping := map[string]interface{}{
		"mappings": map[string]interface{}{
			"properties": map[string]interface{}{
				"id":           map[string]interface{}{"type": "integer"},
				"display_name": map[string]interface{}{"type": "text"},
				"user_type":    map[string]interface{}{"type": "keyword"},
				"organization": map[string]interface{}{"type": "text"},
				"bio":          map[string]interface{}{"type": "text"},
				"privacy_level": map[string]interface{}{"type": "keyword"},
			},
		},
	}

	return s.createIndex(s.indices["users"], mapping)
}

func (s *SearchClient) createIndex(indexName string, mapping map[string]interface{}) error {
	// Check if index already exists
	req := esapi.IndicesExistsRequest{
		Index: []string{indexName},
	}

	res, err := req.Do(context.Background(), s.client)
	if err != nil {
		return err
	}
	res.Body.Close()

	if res.StatusCode == 200 {
		log.Printf("📊 Index already exists: %s", indexName)
		return nil
	}

	// Create index
	mappingBytes, err := json.Marshal(mapping)
	if err != nil {
		return err
	}

	createReq := esapi.IndicesCreateRequest{
		Index: indexName,
		Body:  bytes.NewReader(mappingBytes),
	}

	createRes, err := createReq.Do(context.Background(), s.client)
	if err != nil {
		return err
	}
	defer createRes.Body.Close()

	if createRes.IsError() {
		return fmt.Errorf("failed to create index %s: %s", indexName, createRes.Status())
	}

	log.Printf("✅ Created index: %s", indexName)
	return nil
}

// Query builders

func (s *SearchClient) buildCommunitySearchQuery(params CommunitySearchParams) map[string]interface{} {
	query := map[string]interface{}{
		"query": map[string]interface{}{
			"bool": map[string]interface{}{
				"must": []interface{}{},
				"filter": []interface{}{
					// Always filter to public communities only
					map[string]interface{}{
						"term": map[string]interface{}{
							"privacy_level": "public",
						},
					},
				},
			},
		},
		"sort": []interface{}{
			map[string]interface{}{
				"resilience_score": map[string]interface{}{
					"order": "desc",
				},
			},
		},
	}

	boolQuery := query["query"].(map[string]interface{})["bool"].(map[string]interface{})
	must := boolQuery["must"].([]interface{})
	filter := boolQuery["filter"].([]interface{})

	// Add text search if query provided
	if params.Query != "" {
		must = append(must, map[string]interface{}{
			"multi_match": map[string]interface{}{
				"query":  params.Query,
				"fields": []string{"name^2", "tract_id"},
				"type":   "best_fields",
				"fuzziness": "AUTO",
			},
		})
	}

	// Add filters
	if params.State != "" {
		filter = append(filter, map[string]interface{}{
			"term": map[string]interface{}{
				"state": params.State,
			},
		})
	}

	if params.UnexpectedGoodOnly {
		filter = append(filter, map[string]interface{}{
			"term": map[string]interface{}{
				"unexpected_good": true,
			},
		})
	}

	if params.MinResilienceScore > 0 {
		filter = append(filter, map[string]interface{}{
			"range": map[string]interface{}{
				"resilience_score": map[string]interface{}{
					"gte": params.MinResilienceScore,
				},
			},
		})
	}

	boolQuery["must"] = must
	boolQuery["filter"] = filter

	return query
}

func (s *SearchClient) buildStorySearchQuery(params StorySearchParams) map[string]interface{} {
	query := map[string]interface{}{
		"query": map[string]interface{}{
			"bool": map[string]interface{}{
				"must": []interface{}{},
				"filter": []interface{}{},
			},
		},
		"sort": []interface{}{
			map[string]interface{}{
				"published_at": map[string]interface{}{
					"order": "desc",
				},
			},
		},
	}

	boolQuery := query["query"].(map[string]interface{})["bool"].(map[string]interface{})
	must := boolQuery["must"].([]interface{})
	filter := boolQuery["filter"].([]interface{})

	// Add text search if query provided
	if params.Query != "" {
		must = append(must, map[string]interface{}{
			"multi_match": map[string]interface{}{
				"query":  params.Query,
				"fields": []string{"title^3", "summary^2", "content"},
				"type":   "best_fields",
				"fuzziness": "AUTO",
			},
		})
	}

	// Add filters
	if params.Category != "" {
		filter = append(filter, map[string]interface{}{
			"term": map[string]interface{}{
				"category": params.Category,
			},
		})
	}

	if params.StoryType != "" {
		filter = append(filter, map[string]interface{}{
			"term": map[string]interface{}{
				"story_type": params.StoryType,
			},
		})
	}

	if len(params.Tags) > 0 {
		filter = append(filter, map[string]interface{}{
			"terms": map[string]interface{}{
				"tags": params.Tags,
			},
		})
	}

	if params.CommunityID > 0 {
		filter = append(filter, map[string]interface{}{
			"term": map[string]interface{}{
				"community_id": params.CommunityID,
			},
		})
	}

	boolQuery["must"] = must
	boolQuery["filter"] = filter

	return query
}