// Story repository for database operations  
// Created: January 31, 2025
// Purpose: Data access layer for community stories with dignity-first design

package repositories

import (
	"context"
	"fmt"
	"strings"
	"time"
	
	"gorm.io/gorm"
	"github.com/your-org/resilience-mapping/internal/models"
)

// StoryRepository handles database operations for stories
type StoryRepository struct {
	db *gorm.DB
}

// NewStoryRepository creates a new story repository
func NewStoryRepository(db *gorm.DB) *StoryRepository {
	return &StoryRepository{db: db}
}

// Create inserts a new story
func (r *StoryRepository) Create(ctx context.Context, story *models.Story) error {
	return r.db.WithContext(ctx).Create(story).Error
}

// GetByID retrieves story by ID
func (r *StoryRepository) GetByID(ctx context.Context, id int) (*models.Story, error) {
	var story models.Story
	err := r.db.WithContext(ctx).
		Preload("Community").
		Preload("Comments").
		First(&story, id).Error
	if err != nil {
		return nil, err
	}
	return &story, nil
}

// GetBySlug retrieves story by URL slug
func (r *StoryRepository) GetBySlug(ctx context.Context, slug string) (*models.Story, error) {
	var story models.Story
	err := r.db.WithContext(ctx).
		Preload("Community").
		Preload("Comments").
		Where("slug = ? AND status = ?", slug, "published").
		First(&story).Error
	if err != nil {
		return nil, err
	}
	return &story, nil
}

// GetByCommunityID retrieves all stories for a specific community
func (r *StoryRepository) GetByCommunityID(ctx context.Context, communityID int, publishedOnly bool) ([]models.Story, error) {
	var stories []models.Story
	query := r.db.WithContext(ctx).Where("community_id = ?", communityID)
	
	if publishedOnly {
		query = query.Where("status = ?", "published")
	}
	
	err := query.Order("created_at DESC").Find(&stories).Error
	if err != nil {
		return nil, err
	}
	return stories, nil
}

// GetPublished retrieves published stories with pagination
func (r *StoryRepository) GetPublished(ctx context.Context, params StorySearchParams) ([]models.Story, int64, error) {
	query := r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("status = ?", "published")
	
	// Apply filters
	if params.CommunityID > 0 {
		query = query.Where("community_id = ?", params.CommunityID)
	}
	
	if params.StoryType != "" {
		query = query.Where("story_type = ?", params.StoryType)
	}
	
	if params.Category != "" {
		query = query.Where("category = ?", params.Category)
	}
	
	if params.Query != "" {
		searchTerm := "%" + strings.ToLower(params.Query) + "%"
		query = query.Where(
			"LOWER(title) LIKE ? OR LOWER(summary) LIKE ? OR LOWER(content) LIKE ?",
			searchTerm, searchTerm, searchTerm,
		)
	}
	
	if len(params.Tags) > 0 {
		// Search in JSONB tags array
		for _, tag := range params.Tags {
			query = query.Where("tags @> ?", fmt.Sprintf(`["%s"]`, tag))
		}
	}
	
	if params.FeaturedOnly {
		now := time.Now()
		query = query.Where("featured_until IS NOT NULL AND featured_until > ?", now)
	}
	
	// Get total count
	var total int64
	countQuery := query
	if err := countQuery.Count(&total).Error; err != nil {
		return nil, 0, err
	}
	
	// Apply sorting
	orderBy := "created_at DESC"
	if params.SortBy != "" {
		switch params.SortBy {
		case "title":
			orderBy = "title ASC"
		case "views":
			orderBy = "views DESC"
		case "likes":
			orderBy = "likes DESC"
		case "published_at":
			orderBy = "published_at DESC"
		case "updated_at":
			orderBy = "updated_at DESC"
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
	
	// Load associations
	query = query.Preload("Community")
	
	// Execute query
	var stories []models.Story
	err := query.Find(&stories).Error
	if err != nil {
		return nil, 0, err
	}
	
	return stories, total, nil
}

// GetFeatured retrieves currently featured stories
func (r *StoryRepository) GetFeatured(ctx context.Context, limit int) ([]models.Story, error) {
	var stories []models.Story
	now := time.Now()
	
	err := r.db.WithContext(ctx).
		Preload("Community").
		Where("status = ? AND featured_until IS NOT NULL AND featured_until > ?", "published", now).
		Order("featured_until ASC").
		Limit(limit).
		Find(&stories).Error
	
	if err != nil {
		return nil, err
	}
	return stories, nil
}

// GetPopular retrieves stories with highest engagement
func (r *StoryRepository) GetPopular(ctx context.Context, limit int, timeframe string) ([]models.Story, error) {
	var stories []models.Story
	query := r.db.WithContext(ctx).
		Preload("Community").
		Where("status = ?", "published")
	
	// Apply timeframe filter
	if timeframe != "all" {
		var since time.Time
		switch timeframe {
		case "week":
			since = time.Now().AddDate(0, 0, -7)
		case "month":
			since = time.Now().AddDate(0, -1, 0)
		case "year":
			since = time.Now().AddDate(-1, 0, 0)
		}
		if !since.IsZero() {
			query = query.Where("published_at >= ?", since)
		}
	}
	
	err := query.
		Order("(views * 1 + likes * 2 + shares * 3) DESC").
		Limit(limit).
		Find(&stories).Error
	
	if err != nil {
		return nil, err
	}
	return stories, nil
}

// GetByUserID retrieves stories created by a specific user
func (r *StoryRepository) GetByUserID(ctx context.Context, userID int) ([]models.Story, error) {
	var stories []models.Story
	err := r.db.WithContext(ctx).
		Preload("Community").
		Where("created_by = ?", userID).
		Order("created_at DESC").
		Find(&stories).Error
	if err != nil {
		return nil, err
	}
	return stories, nil
}

// GetDrafts retrieves draft stories for a user
func (r *StoryRepository) GetDrafts(ctx context.Context, userID int) ([]models.Story, error) {
	var stories []models.Story
	err := r.db.WithContext(ctx).
		Preload("Community").
		Where("created_by = ? AND status = ?", userID, "draft").
		Order("updated_at DESC").
		Find(&stories).Error
	if err != nil {
		return nil, err
	}
	return stories, nil
}

// GetPendingApproval retrieves stories awaiting community approval
func (r *StoryRepository) GetPendingApproval(ctx context.Context) ([]models.Story, error) {
	var stories []models.Story
	err := r.db.WithContext(ctx).
		Preload("Community").
		Where("status = ?", "pending_approval").
		Order("created_at ASC").
		Find(&stories).Error
	if err != nil {
		return nil, err
	}
	return stories, nil
}

// Update modifies an existing story
func (r *StoryRepository) Update(ctx context.Context, story *models.Story) error {
	story.Version++
	return r.db.WithContext(ctx).Save(story).Error
}

// UpdateStatus changes story status (draft -> pending -> published)
func (r *StoryRepository) UpdateStatus(ctx context.Context, id int, status string, userID int) error {
	updates := map[string]interface{}{
		"status":     status,
		"updated_by": userID,
		"updated_at": time.Now(),
	}
	
	// Set published_at when publishing
	if status == "published" {
		updates["published_at"] = time.Now()
	}
	
	return r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("id = ?", id).
		Updates(updates).Error
}

// IncrementViews increases view count for a story
func (r *StoryRepository) IncrementViews(ctx context.Context, id int) error {
	return r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("id = ?", id).
		Update("views", gorm.Expr("views + ?", 1)).Error
}

// IncrementLikes increases like count for a story  
func (r *StoryRepository) IncrementLikes(ctx context.Context, id int) error {
	return r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("id = ?", id).
		Update("likes", gorm.Expr("likes + ?", 1)).Error
}

// IncrementShares increases share count for a story
func (r *StoryRepository) IncrementShares(ctx context.Context, id int) error {
	return r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("id = ?", id).
		Update("shares", gorm.Expr("shares + ?", 1)).Error
}

// Delete removes a story (soft delete)
func (r *StoryRepository) Delete(ctx context.Context, id int) error {
	return r.db.WithContext(ctx).Delete(&models.Story{}, id).Error
}

// GetCategories returns all available story categories
func (r *StoryRepository) GetCategories(ctx context.Context) ([]string, error) {
	var categories []string
	err := r.db.WithContext(ctx).
		Model(&models.Story{}).
		Distinct("category").
		Where("status = ?", "published").
		Pluck("category", &categories).Error
	if err != nil {
		return nil, err
	}
	return categories, nil
}

// GetTags returns all available tags
func (r *StoryRepository) GetTags(ctx context.Context) ([]string, error) {
	var stories []models.Story
	err := r.db.WithContext(ctx).
		Select("tags").
		Where("status = ?", "published").
		Find(&stories).Error
	if err != nil {
		return nil, err
	}
	
	// Extract unique tags from JSONB
	tagSet := make(map[string]bool)
	for _, story := range stories {
		for _, tag := range story.Tags {
			tagSet[tag] = true
		}
	}
	
	tags := make([]string, 0, len(tagSet))
	for tag := range tagSet {
		tags = append(tags, tag)
	}
	
	return tags, nil
}

// GetStatistics returns aggregate story statistics
func (r *StoryRepository) GetStatistics(ctx context.Context) (StoryStats, error) {
	var stats StoryStats
	
	// Total published stories
	r.db.WithContext(ctx).Model(&models.Story{}).Where("status = ?", "published").Count(&stats.TotalPublished)
	
	// Total draft stories
	r.db.WithContext(ctx).Model(&models.Story{}).Where("status = ?", "draft").Count(&stats.TotalDrafts)
	
	// Pending approval
	r.db.WithContext(ctx).Model(&models.Story{}).Where("status = ?", "pending_approval").Count(&stats.PendingApproval)
	
	// Total views
	r.db.WithContext(ctx).Model(&models.Story{}).Where("status = ?", "published").Select("SUM(views)").Scan(&stats.TotalViews)
	
	// Total likes
	r.db.WithContext(ctx).Model(&models.Story{}).Where("status = ?", "published").Select("SUM(likes)").Scan(&stats.TotalLikes)
	
	// Average reading time
	var avgReadingTime float64
	r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("status = ?", "published").
		Select("AVG(LENGTH(content) / 200.0)"). // 200 words per minute
		Scan(&avgReadingTime)
	stats.AvgReadingTime = int(avgReadingTime)
	
	// Category distribution
	var categoryResults []struct {
		Category string
		Count    int64
	}
	r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("status = ?", "published").
		Select("category, count(*) as count").
		Group("category").
		Order("count DESC").
		Scan(&categoryResults)
	
	stats.CategoryDistribution = make(map[string]int64)
	for _, result := range categoryResults {
		stats.CategoryDistribution[result.Category] = result.Count
	}
	
	// Stories by community count
	r.db.WithContext(ctx).
		Model(&models.Story{}).
		Where("status = ?", "published").
		Select("COUNT(DISTINCT community_id)").
		Scan(&stats.CommunitiesWithStories)
	
	stats.LastUpdated = time.Now()
	return stats, nil
}

// StorySearchParams defines parameters for story search
type StorySearchParams struct {
	Query        string
	CommunityID  int
	StoryType    string
	Category     string
	Tags         []string
	FeaturedOnly bool
	SortBy       string
	Limit        int
	Offset       int
}

// StoryStats contains aggregate story statistics
type StoryStats struct {
	TotalPublished         int64             `json:"total_published"`
	TotalDrafts           int64             `json:"total_drafts"`
	PendingApproval       int64             `json:"pending_approval"`
	TotalViews            int64             `json:"total_views"`
	TotalLikes            int64             `json:"total_likes"`
	AvgReadingTime        int               `json:"avg_reading_time_minutes"`
	CategoryDistribution  map[string]int64  `json:"category_distribution"`
	CommunitiesWithStories int64            `json:"communities_with_stories"`
	LastUpdated           time.Time         `json:"last_updated"`
}