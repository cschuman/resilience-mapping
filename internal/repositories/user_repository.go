// User repository for database operations
// Created: January 31, 2025
// Purpose: Data access layer for user management with privacy-first approach

package repositories

import (
	"context"
	"fmt"
	"strings"
	"time"
	
	"gorm.io/gorm"
	"github.com/your-org/resilience-mapping/internal/models"
)

// UserRepository handles database operations for users
type UserRepository struct {
	db *gorm.DB
}

// NewUserRepository creates a new user repository
func NewUserRepository(db *gorm.DB) *UserRepository {
	return &UserRepository{db: db}
}

// Create inserts a new user
func (r *UserRepository) Create(ctx context.Context, user *models.User) error {
	return r.db.WithContext(ctx).Create(user).Error
}

// GetByID retrieves user by ID
func (r *UserRepository) GetByID(ctx context.Context, id int) (*models.User, error) {
	var user models.User
	err := r.db.WithContext(ctx).
		Preload("Community").
		First(&user, id).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// GetByEmail retrieves user by email address
func (r *UserRepository) GetByEmail(ctx context.Context, email string) (*models.User, error) {
	var user models.User
	err := r.db.WithContext(ctx).
		Preload("Community").
		Where("email = ?", strings.ToLower(email)).
		First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// GetByUsername retrieves user by username
func (r *UserRepository) GetByUsername(ctx context.Context, username string) (*models.User, error) {
	var user models.User
	err := r.db.WithContext(ctx).
		Preload("Community").
		Where("username = ?", strings.ToLower(username)).
		First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

// Search searches for users with filters
func (r *UserRepository) Search(ctx context.Context, params UserSearchParams) ([]models.User, int64, error) {
	query := r.db.WithContext(ctx).Model(&models.User{})
	
	// Apply filters
	if params.UserType != "" {
		query = query.Where("user_type = ?", params.UserType)
	}
	
	if params.Role != "" {
		query = query.Where("role = ?", params.Role)
	}
	
	if params.Status != "" {
		query = query.Where("status = ?", params.Status)
	}
	
	if params.CommunityID > 0 {
		query = query.Where("community_id = ?", params.CommunityID)
	}
	
	if params.Verified != nil {
		query = query.Where("is_verified = ?", *params.Verified)
	}
	
	if params.Organization != "" {
		orgTerm := "%" + strings.ToLower(params.Organization) + "%"
		query = query.Where("LOWER(organization) LIKE ?", orgTerm)
	}
	
	if params.Query != "" {
		searchTerm := "%" + strings.ToLower(params.Query) + "%"
		query = query.Where(
			"LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ? OR LOWER(display_name) LIKE ? OR LOWER(username) LIKE ?",
			searchTerm, searchTerm, searchTerm, searchTerm,
		)
	}
	
	// Privacy filter - respect user privacy settings
	if params.PublicOnly {
		query = query.Where("privacy_level = ?", "public")
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
		case "name":
			orderBy = "first_name ASC, last_name ASC"
		case "username":
			orderBy = "username ASC"
		case "email":
			orderBy = "email ASC"
		case "created_at":
			orderBy = "created_at DESC"
		case "last_login":
			orderBy = "last_login DESC"
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
	var users []models.User
	err := query.Find(&users).Error
	if err != nil {
		return nil, 0, err
	}
	
	return users, total, nil
}

// GetByCommunityID retrieves all users associated with a community
func (r *UserRepository) GetByCommunityID(ctx context.Context, communityID int) ([]models.User, error) {
	var users []models.User
	err := r.db.WithContext(ctx).
		Where("community_id = ? AND status = ?", communityID, "active").
		Order("created_at ASC").
		Find(&users).Error
	if err != nil {
		return nil, err
	}
	return users, nil
}

// GetByUserType retrieves users by type (researcher, policymaker, etc.)
func (r *UserRepository) GetByUserType(ctx context.Context, userType string) ([]models.User, error) {
	var users []models.User
	err := r.db.WithContext(ctx).
		Where("user_type = ? AND status = ?", userType, "active").
		Order("created_at DESC").
		Find(&users).Error
	if err != nil {
		return nil, err
	}
	return users, nil
}

// GetUnverified retrieves users who need verification
func (r *UserRepository) GetUnverified(ctx context.Context) ([]models.User, error) {
	var users []models.User
	err := r.db.WithContext(ctx).
		Where("is_verified = ? AND (user_type = ? OR user_type = ?)", false, "researcher", "policymaker").
		Order("created_at ASC").
		Find(&users).Error
	if err != nil {
		return nil, err
	}
	return users, nil
}

// Update modifies an existing user
func (r *UserRepository) Update(ctx context.Context, user *models.User) error {
	return r.db.WithContext(ctx).Save(user).Error
}

// UpdateLastLogin updates the user's last login time
func (r *UserRepository) UpdateLastLogin(ctx context.Context, userID int) error {
	now := time.Now()
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Updates(map[string]interface{}{
			"last_login":   &now,
			"login_count":  gorm.Expr("login_count + ?", 1),
			"last_activity": &now,
		}).Error
}

// UpdateActivity updates the user's last activity timestamp
func (r *UserRepository) UpdateActivity(ctx context.Context, userID int) error {
	now := time.Now()
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("last_activity", &now).Error
}

// UpdatePassword changes user password
func (r *UserRepository) UpdatePassword(ctx context.Context, userID int, hashedPassword string) error {
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("password_hash", hashedPassword).Error
}

// UpdateStatus changes user status (active, suspended, etc.)
func (r *UserRepository) UpdateStatus(ctx context.Context, userID int, status string) error {
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("status", status).Error
}

// VerifyUser marks user as verified
func (r *UserRepository) VerifyUser(ctx context.Context, userID int, verificationType string) error {
	now := time.Now()
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Updates(map[string]interface{}{
			"is_verified":       true,
			"verified_at":       &now,
			"verification_type": verificationType,
		}).Error
}

// VerifyEmail marks user email as verified
func (r *UserRepository) VerifyEmail(ctx context.Context, userID int) error {
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("email_verified", true).Error
}

// UpdatePreferences updates user preferences
func (r *UserRepository) UpdatePreferences(ctx context.Context, userID int, preferences models.UserPreferences) error {
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("preferences", preferences).Error
}

// UpdateNotifications updates user notification settings
func (r *UserRepository) UpdateNotifications(ctx context.Context, userID int, notifications models.NotificationSettings) error {
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("notifications", notifications).Error
}

// IncrementStoriesCreated increases story count for user
func (r *UserRepository) IncrementStoriesCreated(ctx context.Context, userID int) error {
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("stories_created", gorm.Expr("stories_created + ?", 1)).Error
}

// IncrementCommentsPosted increases comment count for user
func (r *UserRepository) IncrementCommentsPosted(ctx context.Context, userID int) error {
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", userID).
		Update("comments_posted", gorm.Expr("comments_posted + ?", 1)).Error
}

// Delete removes a user (soft delete with data retention compliance)
func (r *UserRepository) Delete(ctx context.Context, id int) error {
	// In a real implementation, this would anonymize/remove personal data
	// according to data retention policies and GDPR/CCPA requirements
	return r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("id = ?", id).
		Updates(map[string]interface{}{
			"status":      "deleted",
			"email":       fmt.Sprintf("deleted_%d@example.com", id),
			"first_name":  "",
			"last_name":   "",
			"display_name": "Deleted User",
			"bio":         "",
			"avatar":      "",
		}).Error
}

// EmailExists checks if email is already registered
func (r *UserRepository) EmailExists(ctx context.Context, email string) (bool, error) {
	var count int64
	err := r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("email = ?", strings.ToLower(email)).
		Count(&count).Error
	if err != nil {
		return false, err
	}
	return count > 0, nil
}

// UsernameExists checks if username is already taken
func (r *UserRepository) UsernameExists(ctx context.Context, username string) (bool, error) {
	var count int64
	err := r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("username = ?", strings.ToLower(username)).
		Count(&count).Error
	if err != nil {
		return false, err
	}
	return count > 0, nil
}

// GetStatistics returns aggregate user statistics
func (r *UserRepository) GetStatistics(ctx context.Context) (UserStats, error) {
	var stats UserStats
	
	// Total users
	r.db.WithContext(ctx).Model(&models.User{}).Where("status = ?", "active").Count(&stats.TotalUsers)
	
	// User type distribution
	var typeResults []struct {
		UserType string
		Count    int64
	}
	r.db.WithContext(ctx).
		Model(&models.User{}).
		Where("status = ?", "active").
		Select("user_type, count(*) as count").
		Group("user_type").
		Order("count DESC").
		Scan(&typeResults)
	
	stats.UserTypeDistribution = make(map[string]int64)
	for _, result := range typeResults {
		stats.UserTypeDistribution[result.UserType] = result.Count
	}
	
	// Verified users
	r.db.WithContext(ctx).Model(&models.User{}).Where("status = ? AND is_verified = ?", "active", true).Count(&stats.VerifiedUsers)
	
	// Community members
	r.db.WithContext(ctx).Model(&models.User{}).Where("status = ? AND community_id IS NOT NULL", "active").Count(&stats.CommunityMembers)
	
	// Active in last 30 days
	thirtyDaysAgo := time.Now().AddDate(0, 0, -30)
	r.db.WithContext(ctx).Model(&models.User{}).Where("status = ? AND last_activity > ?", "active", thirtyDaysAgo).Count(&stats.ActiveUsers)
	
	// New users this month
	startOfMonth := time.Now().AddDate(0, 0, -time.Now().Day()+1)
	r.db.WithContext(ctx).Model(&models.User{}).Where("status = ? AND created_at >= ?", "active", startOfMonth).Count(&stats.NewUsersThisMonth)
	
	stats.LastUpdated = time.Now()
	return stats, nil
}

// GetActiveUsers retrieves users active within specified timeframe
func (r *UserRepository) GetActiveUsers(ctx context.Context, since time.Time, limit int) ([]models.User, error) {
	var users []models.User
	err := r.db.WithContext(ctx).
		Where("status = ? AND last_activity > ?", "active", since).
		Order("last_activity DESC").
		Limit(limit).
		Find(&users).Error
	if err != nil {
		return nil, err
	}
	return users, nil
}

// UserSearchParams defines parameters for user search
type UserSearchParams struct {
	Query        string
	UserType     string
	Role         string
	Status       string
	CommunityID  int
	Organization string
	Verified     *bool
	PublicOnly   bool
	SortBy       string
	Limit        int
	Offset       int
}

// UserStats contains aggregate user statistics
type UserStats struct {
	TotalUsers           int64             `json:"total_users"`
	VerifiedUsers        int64             `json:"verified_users"`
	CommunityMembers     int64             `json:"community_members"`
	ActiveUsers          int64             `json:"active_users_30_days"`
	NewUsersThisMonth    int64             `json:"new_users_this_month"`
	UserTypeDistribution map[string]int64  `json:"user_type_distribution"`
	LastUpdated          time.Time         `json:"last_updated"`
}