// Community repository for database operations
// Created: January 31, 2025
// Purpose: Data access layer for community information with privacy protection

package repositories

import (
	"fmt"
	"strings"
	"context"
	"time"
	
	"gorm.io/gorm"
	"github.com/your-org/resilience-mapping/internal/models"
)

// CommunityRepository handles database operations for communities
type CommunityRepository struct {
	db *gorm.DB
}

// NewCommunityRepository creates a new community repository
func NewCommunityRepository(db *gorm.DB) *CommunityRepository {
	return &CommunityRepository{db: db}
}

// Create inserts a new community
func (r *CommunityRepository) Create(ctx context.Context, community *models.Community) error {
	return r.db.WithContext(ctx).Create(community).Error
}

// GetByID retrieves community by ID
func (r *CommunityRepository) GetByID(ctx context.Context, id int) (*models.Community, error) {
	var community models.Community
	err := r.db.WithContext(ctx).
		Preload("Stories").
		First(&community, id).Error
	if err != nil {
		return nil, err
	}
	return &community, nil
}

// GetByTractID retrieves community by census tract ID
func (r *CommunityRepository) GetByTractID(ctx context.Context, tractID string) (*models.Community, error) {
	var community models.Community
	err := r.db.WithContext(ctx).
		Preload("Stories").
		Where("tract_id = ?", tractID).
		First(&community).Error
	if err != nil {
		return nil, err
	}
	return &community, nil
}

// GetAllResilient retrieves all unexpectedly resilient communities
func (r *CommunityRepository) GetAllResilient(ctx context.Context) ([]models.Community, error) {
	var communities []models.Community
	err := r.db.WithContext(ctx).
		Where("unexpected_good = ?", true).
		Order("resilience_score DESC").
		Find(&communities).Error
	if err != nil {
		return nil, err
	}
	return communities, nil
}

// SearchCommunities performs search with multiple criteria
func (r *CommunityRepository) SearchCommunities(ctx context.Context, params SearchParams) ([]models.Community, int64, error) {
	query := r.db.WithContext(ctx).Model(&models.Community{})
	
	// Apply filters
	if params.State != "" {
		query = query.Where("state = ?", params.State)
	}
	
	if params.County != "" {
		query = query.Where("county = ?", params.County)
	}
	
	if params.MinResilienceScore > 0 {
		query = query.Where("resilience_score >= ?", params.MinResilienceScore)
	}
	
	if params.MaxResilienceScore > 0 {
		query = query.Where("resilience_score <= ?", params.MaxResilienceScore)
	}
	
	if params.OnlyUnexpectedGood {
		query = query.Where("unexpected_good = ?", true)
	}
	
	if params.MinPopulation > 0 {
		query = query.Where("population >= ?", params.MinPopulation)
	}
	
	if params.MaxPopulation > 0 {
		query = query.Where("population <= ?", params.MaxPopulation)
	}
	
	if params.Query != "" {
		searchTerm := "%" + strings.ToLower(params.Query) + "%"
		query = query.Where("LOWER(name) LIKE ? OR tract_id LIKE ?", searchTerm, searchTerm)
	}
	
	// Privacy filter - only show approved communities in public contexts
	if params.PublicOnly {
		query = query.Where("community_approved = ? AND privacy_level = ?", true, "public")
	}
	
	// Get total count
	var total int64
	countQuery := query
	if err := countQuery.Count(&total).Error; err != nil {
		return nil, 0, err
	}
	
	// Apply sorting
	orderBy := "resilience_score DESC"
	if params.SortBy != "" {
		switch params.SortBy {
		case "name":
			orderBy = "name ASC"
		case "population":
			orderBy = "population DESC"
		case "resilience_score":
			orderBy = "resilience_score DESC"
		case "created_at":
			orderBy = "created_at DESC"
		}
	}
	query = query.Order(orderBy)
	
	// Apply pagination
	if params.Limit > 0 {
		query = query.Limit(params.Limit)
	}
	if params.Offset > 0 {
		query = query.Offset(params.Offset)
	}
	
	// Execute query
	var communities []models.Community
	err := query.Find(&communities).Error
	if err != nil {
		return nil, 0, err
	}
	
	return communities, total, nil
}

// GetNearby finds communities within a geographic radius
func (r *CommunityRepository) GetNearby(ctx context.Context, lat, lng float64, radiusKm float64) ([]models.Community, error) {
	var communities []models.Community
	
	// PostGIS query to find communities within radius
	query := `
		SELECT * FROM communities 
		WHERE ST_DWithin(
			centroid, 
			ST_GeomFromText('POINT(? ?)', 4326)::geography,
			? * 1000
		)
		ORDER BY ST_Distance(
			centroid, 
			ST_GeomFromText('POINT(? ?)', 4326)::geography
		)
	`
	
	err := r.db.WithContext(ctx).
		Raw(query, lng, lat, radiusKm, lng, lat).
		Scan(&communities).Error
	if err != nil {
		return nil, err
	}
	
	return communities, nil
}

// GetWithStories retrieves communities that have associated stories
func (r *CommunityRepository) GetWithStories(ctx context.Context, limit int) ([]models.Community, error) {
	var communities []models.Community
	err := r.db.WithContext(ctx).
		Preload("Stories", "status = ?", "published").
		Where("story_count > ?", 0).
		Order("story_count DESC").
		Limit(limit).
		Find(&communities).Error
	if err != nil {
		return nil, err
	}
	return communities, nil
}

// GetByState retrieves all communities in a specific state
func (r *CommunityRepository) GetByState(ctx context.Context, state string) ([]models.Community, error) {
	var communities []models.Community
	err := r.db.WithContext(ctx).
		Where("state = ?", state).
		Order("name ASC").
		Find(&communities).Error
	if err != nil {
		return nil, err
	}
	return communities, nil
}

// Update modifies an existing community
func (r *CommunityRepository) Update(ctx context.Context, community *models.Community) error {
	return r.db.WithContext(ctx).Save(community).Error
}

// UpdateStoryCount updates the cached story count for a community
func (r *CommunityRepository) UpdateStoryCount(ctx context.Context, communityID int) error {
	return r.db.WithContext(ctx).
		Model(&models.Community{}).
		Where("id = ?", communityID).
		Update("story_count", r.db.Model(&models.Story{}).Where("community_id = ? AND status = ?", communityID, "published").Select("count(*)")).
		Error
}

// Delete removes a community (soft delete)
func (r *CommunityRepository) Delete(ctx context.Context, id int) error {
	return r.db.WithContext(ctx).Delete(&models.Community{}, id).Error
}

// GetTopResilient returns communities with highest resilience scores
func (r *CommunityRepository) GetTopResilient(ctx context.Context, limit int) ([]models.Community, error) {
	var communities []models.Community
	err := r.db.WithContext(ctx).
		Where("unexpected_good = ?", true).
		Order("resilience_score DESC").
		Limit(limit).
		Find(&communities).Error
	if err != nil {
		return nil, err
	}
	return communities, nil
}

// GetStatistics returns aggregate statistics about communities
func (r *CommunityRepository) GetStatistics(ctx context.Context) (CommunityStats, error) {
	var stats CommunityStats
	
	// Total communities
	r.db.WithContext(ctx).Model(&models.Community{}).Count(&stats.TotalCommunities)
	
	// Resilient communities
	r.db.WithContext(ctx).Model(&models.Community{}).Where("unexpected_good = ?", true).Count(&stats.ResilientCommunities)
	
	// Average resilience score
	r.db.WithContext(ctx).Model(&models.Community{}).Select("AVG(resilience_score)").Scan(&stats.AvgResilienceScore)
	
	// Total population
	r.db.WithContext(ctx).Model(&models.Community{}).Select("SUM(population)").Scan(&stats.TotalPopulation)
	
	// Communities with stories
	r.db.WithContext(ctx).Model(&models.Community{}).Where("story_count > ?", 0).Count(&stats.CommunitiesWithStories)
	
	// State distribution
	var stateResults []struct {
		State string
		Count int64
	}
	r.db.WithContext(ctx).
		Model(&models.Community{}).
		Select("state, count(*) as count").
		Group("state").
		Order("count DESC").
		Scan(&stateResults)
	
	stats.StateDistribution = make(map[string]int64)
	for _, result := range stateResults {
		stats.StateDistribution[result.State] = result.Count
	}
	
	return stats, nil
}

// BulkInsert inserts multiple communities efficiently
func (r *CommunityRepository) BulkInsert(ctx context.Context, communities []models.Community) error {
	// Use batch insert for better performance
	batchSize := 100
	for i := 0; i < len(communities); i += batchSize {
		end := i + batchSize
		if end > len(communities) {
			end = len(communities)
		}
		
		if err := r.db.WithContext(ctx).Create(communities[i:end]).Error; err != nil {
			return fmt.Errorf("failed to insert batch %d-%d: %w", i, end, err)
		}
	}
	return nil
}

// SearchParams defines parameters for community search
type SearchParams struct {
	Query                string
	State                string
	County               string
	MinResilienceScore   float64
	MaxResilienceScore   float64
	OnlyUnexpectedGood   bool
	MinPopulation        int
	MaxPopulation        int
	SortBy               string
	Limit                int
	Offset               int
	PublicOnly           bool
}

// CommunityStats contains aggregate statistics
type CommunityStats struct {
	TotalCommunities      int64             `json:"total_communities"`
	ResilientCommunities  int64             `json:"resilient_communities"`
	AvgResilienceScore    float64           `json:"avg_resilience_score"`
	TotalPopulation       int64             `json:"total_population"`
	CommunitiesWithStories int64            `json:"communities_with_stories"`
	StateDistribution     map[string]int64  `json:"state_distribution"`
	LastUpdated           time.Time         `json:"last_updated"`
}