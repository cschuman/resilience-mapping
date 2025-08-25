// User models for authentication and authorization
// Created: January 31, 2025
// Purpose: Manage users while prioritizing community privacy and consent

package models

import (
	"time"
	"golang.org/x/crypto/bcrypt"
	"database/sql/driver"
	"encoding/json"
	"errors"
)

// User represents system users with privacy-first design
type User struct {
	ID          int       `json:"id" gorm:"primaryKey;autoIncrement"`
	Email       string    `json:"email" gorm:"uniqueIndex;size:255;not null"`
	Username    string    `json:"username" gorm:"uniqueIndex;size:100"`
	PasswordHash string   `json:"-" gorm:"size:255;not null"` // Never serialize password
	
	// Profile information
	FirstName   string    `json:"first_name" gorm:"size:100"`
	LastName    string    `json:"last_name" gorm:"size:100"`
	DisplayName string    `json:"display_name" gorm:"size:100"`
	Bio         string    `json:"bio" gorm:"size:500"`
	Avatar      string    `json:"avatar" gorm:"size:255"`
	
	// User type and permissions
	UserType    string    `json:"user_type" gorm:"size:50;not null;index"`
	Role        string    `json:"role" gorm:"size:50;not null;default:'member'"`
	Permissions Permissions `json:"permissions" gorm:"type:jsonb"`
	
	// Community connections
	CommunityID    *int      `json:"community_id,omitempty" gorm:"index"`
	Community      *Community `json:"community,omitempty" gorm:"foreignKey:CommunityID"`
	CommunityRole  string    `json:"community_role" gorm:"size:100"`
	
	// Professional information (for researchers/policymakers)
	Organization   string    `json:"organization" gorm:"size:255"`
	JobTitle       string    `json:"job_title" gorm:"size:255"`
	ResearchFocus  []string  `json:"research_focus" gorm:"type:jsonb"`
	Website        string    `json:"website" gorm:"size:255"`
	
	// Account status
	Status         string    `json:"status" gorm:"size:20;default:'active'"`
	IsVerified     bool      `json:"is_verified" gorm:"default:false"`
	VerifiedAt     *time.Time `json:"verified_at"`
	VerificationType string  `json:"verification_type" gorm:"size:50"`
	
	// Privacy and consent
	PrivacyLevel   string    `json:"privacy_level" gorm:"size:20;default:'private'"`
	ConsentGiven   bool      `json:"consent_given" gorm:"default:false"`
	ConsentDate    *time.Time `json:"consent_date"`
	DataRetention  string    `json:"data_retention" gorm:"size:50;default:'standard'"`
	
	// Authentication
	EmailVerified  bool      `json:"email_verified" gorm:"default:false"`
	LastLogin      *time.Time `json:"last_login"`
	LoginCount     int       `json:"login_count" gorm:"default:0"`
	
	// Security
	TwoFactorEnabled bool     `json:"two_factor_enabled" gorm:"default:false"`
	TwoFactorSecret  string   `json:"-" gorm:"size:32"` // Never serialize 2FA secret
	RecoveryTokens   []string `json:"-" gorm:"type:jsonb"` // Never serialize recovery tokens
	
	// Preferences
	Preferences    UserPreferences `json:"preferences" gorm:"type:jsonb"`
	Notifications  NotificationSettings `json:"notifications" gorm:"type:jsonb"`
	
	// Activity tracking
	StoriesCreated int       `json:"stories_created" gorm:"default:0"`
	CommentsPosted int       `json:"comments_posted" gorm:"default:0"`
	LastActivity   *time.Time `json:"last_activity"`
	
	// Content created by user
	Stories        []Story   `json:"stories,omitempty" gorm:"foreignKey:CreatedBy"`
	Comments       []Comment `json:"comments,omitempty" gorm:"foreignKey:UserID"`
	
	// Audit trail
	CreatedAt      time.Time `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt      time.Time `json:"updated_at" gorm:"autoUpdateTime"`
	CreatedBy      *int      `json:"created_by,omitempty"`
	
	// Terms acceptance
	TermsAccepted     bool       `json:"terms_accepted" gorm:"default:false"`
	TermsAcceptedAt   *time.Time `json:"terms_accepted_at"`
	PrivacyAccepted   bool       `json:"privacy_accepted" gorm:"default:false"`
	PrivacyAcceptedAt *time.Time `json:"privacy_accepted_at"`
}

// Permissions defines what actions a user can perform
type Permissions struct {
	CanCreateStories     bool `json:"can_create_stories"`
	CanEditOwnStories    bool `json:"can_edit_own_stories"`
	CanEditAllStories    bool `json:"can_edit_all_stories"`
	CanDeleteStories     bool `json:"can_delete_stories"`
	CanModerateComments  bool `json:"can_moderate_comments"`
	CanManageUsers       bool `json:"can_manage_users"`
	CanAccessResearch    bool `json:"can_access_research"`
	CanDownloadData      bool `json:"can_download_data"`
	CanContactCommunities bool `json:"can_contact_communities"`
	CanManageCommunities bool `json:"can_manage_communities"`
}

// UserPreferences stores user-specific settings
type UserPreferences struct {
	Theme             string   `json:"theme"` // light, dark, auto
	Language          string   `json:"language"`
	TimeZone          string   `json:"time_zone"`
	EmailFrequency    string   `json:"email_frequency"` // daily, weekly, monthly, never
	ShowEmail         bool     `json:"show_email"`
	ShowName          bool     `json:"show_name"`
	ShowOrganization  bool     `json:"show_organization"`
	PreferredCategories []string `json:"preferred_categories"`
	AccessibilityMode bool     `json:"accessibility_mode"`
}

// NotificationSettings controls what notifications user receives
type NotificationSettings struct {
	EmailNotifications    bool `json:"email_notifications"`
	StoryPublished        bool `json:"story_published"`
	CommentReceived       bool `json:"comment_received"`
	CommunityUpdates      bool `json:"community_updates"`
	ResearchUpdates       bool `json:"research_updates"`
	PolicyUpdates         bool `json:"policy_updates"`
	MonthlyDigest         bool `json:"monthly_digest"`
	SecurityAlerts        bool `json:"security_alerts"`
}

// Value/Scan implementations for JSONB fields

func (p Permissions) Value() (driver.Value, error) {
	return json.Marshal(p)
}

func (p *Permissions) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("cannot scan non-bytes into Permissions")
	}
	return json.Unmarshal(bytes, p)
}

func (up UserPreferences) Value() (driver.Value, error) {
	return json.Marshal(up)
}

func (up *UserPreferences) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("cannot scan non-bytes into UserPreferences")
	}
	return json.Unmarshal(bytes, up)
}

func (ns NotificationSettings) Value() (driver.Value, error) {
	return json.Marshal(ns)
}

func (ns *NotificationSettings) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("cannot scan non-bytes into NotificationSettings")
	}
	return json.Unmarshal(bytes, ns)
}

// User methods

// SetPassword hashes and sets user password
func (u *User) SetPassword(password string) error {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	u.PasswordHash = string(hash)
	return nil
}

// CheckPassword verifies password against hash
func (u *User) CheckPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.PasswordHash), []byte(password))
	return err == nil
}

// GetDisplayName returns the appropriate display name
func (u *User) GetDisplayName() string {
	if u.DisplayName != "" {
		return u.DisplayName
	}
	if u.FirstName != "" || u.LastName != "" {
		return u.FirstName + " " + u.LastName
	}
	return u.Username
}

// GetPublicProfile returns user info safe for public display
func (u *User) GetPublicProfile() map[string]interface{} {
	profile := map[string]interface{}{
		"id":           u.ID,
		"display_name": u.GetDisplayName(),
		"user_type":    u.UserType,
	}
	
	if u.Preferences.ShowEmail {
		profile["email"] = u.Email
	}
	
	if u.Preferences.ShowOrganization {
		profile["organization"] = u.Organization
		profile["job_title"] = u.JobTitle
	}
	
	if u.Bio != "" {
		profile["bio"] = u.Bio
	}
	
	if u.Avatar != "" {
		profile["avatar"] = u.Avatar
	}
	
	return profile
}

// CanPerform checks if user has specific permission
func (u *User) CanPerform(action string) bool {
	switch action {
	case "create_stories":
		return u.Permissions.CanCreateStories
	case "edit_own_stories":
		return u.Permissions.CanEditOwnStories
	case "edit_all_stories":
		return u.Permissions.CanEditAllStories
	case "delete_stories":
		return u.Permissions.CanDeleteStories
	case "moderate_comments":
		return u.Permissions.CanModerateComments
	case "manage_users":
		return u.Permissions.CanManageUsers
	case "access_research":
		return u.Permissions.CanAccessResearch
	case "download_data":
		return u.Permissions.CanDownloadData
	case "contact_communities":
		return u.Permissions.CanContactCommunities
	case "manage_communities":
		return u.Permissions.CanManageCommunities
	default:
		return false
	}
}

// IsActive returns true if user account is active
func (u *User) IsActive() bool {
	return u.Status == "active"
}

// IsCommunityMember returns true if user is connected to a community
func (u *User) IsCommunityMember() bool {
	return u.CommunityID != nil
}

// IsResearcher returns true if user is a researcher
func (u *User) IsResearcher() bool {
	return u.UserType == "researcher" || u.UserType == "academic"
}

// IsPolicymaker returns true if user is a policymaker
func (u *User) IsPolicymaker() bool {
	return u.UserType == "policymaker" || u.UserType == "government"
}

// HasAcceptedTerms returns true if user has accepted current terms
func (u *User) HasAcceptedTerms() bool {
	return u.TermsAccepted && u.PrivacyAccepted
}

// NeedsVerification returns true if user needs verification
func (u *User) NeedsVerification() bool {
	return !u.IsVerified && (u.IsResearcher() || u.IsPolicymaker())
}