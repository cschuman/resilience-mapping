// Story models for community narratives
// Created: January 31, 2025  
// Purpose: Capture and share community resilience stories with dignity

package models

import (
	"time"
	"database/sql/driver"
	"encoding/json"
	"errors"
	"strings"
)

// Story represents a community resilience story
type Story struct {
	ID            int       `json:"id" gorm:"primaryKey;autoIncrement"`
	CommunityID   int       `json:"community_id" gorm:"not null;index"`
	Community     Community `json:"community,omitempty" gorm:"foreignKey:CommunityID"`
	
	// Story metadata
	Title         string    `json:"title" gorm:"size:255;not null"`
	Slug          string    `json:"slug" gorm:"size:255;uniqueIndex;not null"`
	Summary       string    `json:"summary" gorm:"size:500;not null"`
	Content       string    `json:"content" gorm:"type:text;not null"`
	
	// Story categorization
	StoryType     string    `json:"story_type" gorm:"size:50;not null;index"`
	Tags          Tags      `json:"tags" gorm:"type:jsonb"`
	Category      string    `json:"category" gorm:"size:100;not null;index"`
	
	// Community voice and attribution
	Storyteller   Storyteller `json:"storyteller" gorm:"type:jsonb"`
	Attribution   string      `json:"attribution" gorm:"size:255"`
	CommunityRole string      `json:"community_role" gorm:"size:100"`
	
	// Content details
	ResilienceFactors []string `json:"resilience_factors" gorm:"type:jsonb"`
	ChallengesAd     []string `json:"challenges_addressed" gorm:"type:jsonb"`
	Solutions        []string `json:"solutions" gorm:"type:jsonb"`
	Impact           string   `json:"impact" gorm:"type:text"`
	
	// Media and assets
	Images        []Image `json:"images,omitempty" gorm:"type:jsonb"`
	Videos        []Video `json:"videos,omitempty" gorm:"type:jsonb"`
	AudioClips    []Audio `json:"audio_clips,omitempty" gorm:"type:jsonb"`
	Documents     []Document `json:"documents,omitempty" gorm:"type:jsonb"`
	
	// Engagement metrics
	Views         int       `json:"views" gorm:"default:0"`
	Shares        int       `json:"shares" gorm:"default:0"`
	Likes         int       `json:"likes" gorm:"default:0"`
	Comments      []Comment `json:"comments,omitempty" gorm:"foreignKey:StoryID"`
	
	// Publication and moderation
	Status        string    `json:"status" gorm:"size:20;default:'draft';index"`
	PublishedAt   *time.Time `json:"published_at"`
	FeaturedUntil *time.Time `json:"featured_until"`
	
	// Community approval and consent
	CommunityApproved bool      `json:"community_approved" gorm:"default:false"`
	ConsentForm       string    `json:"consent_form" gorm:"size:255"`
	ApprovalNotes     string    `json:"approval_notes" gorm:"type:text"`
	
	// SEO and discoverability
	MetaDescription string `json:"meta_description" gorm:"size:160"`
	Keywords        []string `json:"keywords" gorm:"type:jsonb"`
	
	// Accessibility
	AltText       string `json:"alt_text" gorm:"type:text"`
	AudioDesc     string `json:"audio_description" gorm:"type:text"`
	Transcripts   []Transcript `json:"transcripts,omitempty" gorm:"type:jsonb"`
	
	// Language and translation
	Language      string `json:"language" gorm:"size:5;default:'en'"`
	Translations  []Translation `json:"translations,omitempty" gorm:"type:jsonb"`
	
	// Data management
	CreatedBy     int       `json:"created_by" gorm:"not null"`
	UpdatedBy     int       `json:"updated_by"`
	CreatedAt     time.Time `json:"created_at" gorm:"autoCreateTime"`
	UpdatedAt     time.Time `json:"updated_at" gorm:"autoUpdateTime"`
	
	// Content integrity
	Version       int    `json:"version" gorm:"default:1"`
	ChangeLog     string `json:"change_log" gorm:"type:text"`
}

// Storyteller represents the person sharing their story
type Storyteller struct {
	Name         string `json:"name,omitempty"`
	Title        string `json:"title,omitempty"`
	Organization string `json:"organization,omitempty"`
	Bio          string `json:"bio,omitempty"`
	Anonymous    bool   `json:"anonymous"`
	Verified     bool   `json:"verified"`
}

// Tags for story categorization
type Tags []string

// Media types for rich content
type Image struct {
	URL         string `json:"url"`
	AltText     string `json:"alt_text"`
	Caption     string `json:"caption,omitempty"`
	Credit      string `json:"credit,omitempty"`
	Width       int    `json:"width,omitempty"`
	Height      int    `json:"height,omitempty"`
}

type Video struct {
	URL         string `json:"url"`
	Thumbnail   string `json:"thumbnail"`
	Duration    int    `json:"duration"` // seconds
	Caption     string `json:"caption,omitempty"`
	Transcript  string `json:"transcript,omitempty"`
}

type Audio struct {
	URL         string `json:"url"`
	Duration    int    `json:"duration"` // seconds
	Caption     string `json:"caption,omitempty"`
	Transcript  string `json:"transcript,omitempty"`
}

type Document struct {
	URL         string `json:"url"`
	Title       string `json:"title"`
	Description string `json:"description,omitempty"`
	FileType    string `json:"file_type"`
	FileSize    int    `json:"file_size"` // bytes
}

type Transcript struct {
	Language    string `json:"language"`
	Content     string `json:"content"`
	TimeCoded   bool   `json:"time_coded"`
}

type Translation struct {
	Language    string `json:"language"`
	Title       string `json:"title"`
	Summary     string `json:"summary"`
	Content     string `json:"content"`
	Translator  string `json:"translator,omitempty"`
}

// Comment represents community engagement
type Comment struct {
	ID        int       `json:"id" gorm:"primaryKey;autoIncrement"`
	StoryID   int       `json:"story_id" gorm:"not null;index"`
	UserID    int       `json:"user_id" gorm:"not null"`
	Content   string    `json:"content" gorm:"type:text;not null"`
	Status    string    `json:"status" gorm:"size:20;default:'pending'"`
	CreatedAt time.Time `json:"created_at" gorm:"autoCreateTime"`
}

// Value/Scan implementations for JSONB fields

func (t Tags) Value() (driver.Value, error) {
	return json.Marshal(t)
}

func (t *Tags) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("cannot scan non-bytes into Tags")
	}
	return json.Unmarshal(bytes, t)
}

func (s Storyteller) Value() (driver.Value, error) {
	return json.Marshal(s)
}

func (s *Storyteller) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("cannot scan non-bytes into Storyteller")
	}
	return json.Unmarshal(bytes, s)
}

// Helper methods for Story

// GetPublicTitle returns title with privacy considerations
func (s *Story) GetPublicTitle() string {
	if s.Storyteller.Anonymous {
		return strings.Replace(s.Title, s.Storyteller.Name, "[Community Member]", -1)
	}
	return s.Title
}

// IsPublished returns true if story is published
func (s *Story) IsPublished() bool {
	return s.Status == "published" && s.PublishedAt != nil
}

// IsFeatured returns true if story is currently featured
func (s *Story) IsFeatured() bool {
	if s.FeaturedUntil == nil {
		return false
	}
	return time.Now().Before(*s.FeaturedUntil)
}

// CanEdit returns true if story can be edited by user
func (s *Story) CanEdit(userID int) bool {
	return s.CreatedBy == userID || s.Status == "draft"
}

// GetReadingTime estimates reading time in minutes
func (s *Story) GetReadingTime() int {
	wordCount := len(strings.Fields(s.Content))
	// Average reading speed: 200 words per minute
	minutes := wordCount / 200
	if minutes < 1 {
		return 1
	}
	return minutes
}

// HasMedia returns true if story includes any media
func (s *Story) HasMedia() bool {
	return len(s.Images) > 0 || len(s.Videos) > 0 || len(s.AudioClips) > 0
}

// GetSEOKeywords returns SEO-friendly keywords
func (s *Story) GetSEOKeywords() string {
	return strings.Join(s.Keywords, ", ")
}

// NeedsApproval returns true if community approval is required
func (s *Story) NeedsApproval() bool {
	return !s.CommunityApproved && s.Status == "pending_approval"
}