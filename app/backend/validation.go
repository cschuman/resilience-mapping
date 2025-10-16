// Input validation utilities
// Created: January 31, 2025
// Purpose: Validate user inputs with community-friendly messages

package validation

import (
	"regexp"
	"strings"
	"unicode/utf8"
)

// Common validation rules

// IsEmail validates email address format
func IsEmail(email string) bool {
	emailRegex := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
	return emailRegex.MatchString(email)
}

// IsStrongPassword validates password strength
func IsStrongPassword(password string) bool {
	if len(password) < 8 {
		return false
	}
	
	hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
	hasLower := regexp.MustCompile(`[a-z]`).MatchString(password)
	hasNumber := regexp.MustCompile(`\d`).MatchString(password)
	
	return hasUpper && hasLower && hasNumber
}

// IsValidUsername validates username format
func IsValidUsername(username string) bool {
	if len(username) < 3 || len(username) > 50 {
		return false
	}
	
	usernameRegex := regexp.MustCompile(`^[a-zA-Z0-9_-]+$`)
	return usernameRegex.MatchString(username)
}

// IsValidName validates person name
func IsValidName(name string) bool {
	if len(strings.TrimSpace(name)) == 0 {
		return false
	}
	
	if utf8.RuneCountInString(name) > 100 {
		return false
	}
	
	return true
}

// IsValidTractID validates census tract ID format
func IsValidTractID(tractID string) bool {
	// Census tract IDs are 11 characters: 2-digit state + 3-digit county + 6-digit tract
	if len(tractID) != 11 {
		return false
	}
	
	tractRegex := regexp.MustCompile(`^\d{11}$`)
	return tractRegex.MatchString(tractID)
}

// IsValidStorySlug validates story URL slug
func IsValidStorySlug(slug string) bool {
	if len(slug) < 3 || len(slug) > 100 {
		return false
	}
	
	slugRegex := regexp.MustCompile(`^[a-z0-9-]+$`)
	return slugRegex.MatchString(slug)
}

// ValidationResult represents validation outcome
type ValidationResult struct {
	Valid           bool     `json:"valid"`
	Errors          []string `json:"errors,omitempty"`
	CommunityErrors []string `json:"community_errors,omitempty"`
}

// NewValidationResult creates a new validation result
func NewValidationResult() *ValidationResult {
	return &ValidationResult{
		Valid:           true,
		Errors:          []string{},
		CommunityErrors: []string{},
	}
}

// AddError adds a validation error
func (v *ValidationResult) AddError(error, communityError string) {
	v.Valid = false
	v.Errors = append(v.Errors, error)
	v.CommunityErrors = append(v.CommunityErrors, communityError)
}

// Validate user registration input
func ValidateRegistration(email, username, password, firstName, lastName string) *ValidationResult {
	result := NewValidationResult()
	
	// Email validation
	if !IsEmail(email) {
		result.AddError(
			"Invalid email format",
			"Please enter a valid email address",
		)
	}
	
	// Username validation
	if !IsValidUsername(username) {
		result.AddError(
			"Username must be 3-50 characters and contain only letters, numbers, hyphens, and underscores",
			"Please choose a username between 3-50 characters using only letters, numbers, and dashes",
		)
	}
	
	// Password validation
	if !IsStrongPassword(password) {
		result.AddError(
			"Password must be at least 8 characters with uppercase, lowercase, and number",
			"Please create a strong password with at least 8 characters, including uppercase and lowercase letters and a number",
		)
	}
	
	// Name validation
	if !IsValidName(firstName) {
		result.AddError(
			"First name is required",
			"Please enter your first name",
		)
	}
	
	if !IsValidName(lastName) {
		result.AddError(
			"Last name is required",
			"Please enter your last name",
		)
	}
	
	return result
}

// Validate story creation input
func ValidateStory(title, summary, content string) *ValidationResult {
	result := NewValidationResult()
	
	// Title validation
	if len(strings.TrimSpace(title)) == 0 {
		result.AddError(
			"Title is required",
			"Please add a title for your story",
		)
	} else if utf8.RuneCountInString(title) > 255 {
		result.AddError(
			"Title too long (max 255 characters)",
			"Please shorten your title to 255 characters or less",
		)
	}
	
	// Summary validation
	if len(strings.TrimSpace(summary)) == 0 {
		result.AddError(
			"Summary is required",
			"Please add a brief summary of your story",
		)
	} else if utf8.RuneCountInString(summary) > 500 {
		result.AddError(
			"Summary too long (max 500 characters)",
			"Please shorten your summary to 500 characters or less",
		)
	}
	
	// Content validation
	if len(strings.TrimSpace(content)) == 0 {
		result.AddError(
			"Content is required",
			"Please write your story content",
		)
	} else if utf8.RuneCountInString(content) > 10000 {
		result.AddError(
			"Content too long (max 10,000 characters)",
			"Please shorten your story to 10,000 characters or less",
		)
	}
	
	return result
}

// SanitizeInput removes potentially harmful content
func SanitizeInput(input string) string {
	// Basic sanitization - in production, use a proper HTML sanitizer
	input = strings.TrimSpace(input)
	
	// Remove null bytes
	input = strings.ReplaceAll(input, "\x00", "")
	
	return input
}

// IsValidCoordinate validates latitude/longitude
func IsValidCoordinate(lat, lng float64) bool {
	return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180
}

// IsValidResilienceScore validates resilience score range
func IsValidResilienceScore(score float64) bool {
	return score >= 0.0 && score <= 1.0
}