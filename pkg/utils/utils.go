// Shared utility functions
// Created: January 31, 2025
// Purpose: Common utilities used throughout the application

package utils

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"math"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// String utilities

// GenerateSlug creates a URL-friendly slug from text
func GenerateSlug(text string) string {
	// Convert to lowercase
	slug := strings.ToLower(text)
	
	// Replace spaces and special characters with hyphens
	reg := regexp.MustCompile(`[^a-z0-9]+`)
	slug = reg.ReplaceAllString(slug, "-")
	
	// Remove leading/trailing hyphens
	slug = strings.Trim(slug, "-")
	
	// Limit length
	if len(slug) > 100 {
		slug = slug[:100]
		// Ensure it doesn't end with a hyphen
		slug = strings.TrimRight(slug, "-")
	}
	
	return slug
}

// TruncateText truncates text to specified length with ellipsis
func TruncateText(text string, maxLength int) string {
	if len(text) <= maxLength {
		return text
	}
	
	// Find last word boundary before maxLength
	truncated := text[:maxLength]
	lastSpace := strings.LastIndex(truncated, " ")
	if lastSpace > maxLength/2 { // Only truncate at word if it's not too short
		truncated = truncated[:lastSpace]
	}
	
	return truncated + "..."
}

// CleanSpaces removes extra whitespace and normalizes text
func CleanSpaces(text string) string {
	// Replace multiple spaces with single space
	reg := regexp.MustCompile(`\s+`)
	text = reg.ReplaceAllString(text, " ")
	
	// Trim leading/trailing spaces
	return strings.TrimSpace(text)
}

// Numeric utilities

// RoundToDecimal rounds float to specified decimal places
func RoundToDecimal(value float64, decimals int) float64 {
	multiplier := math.Pow(10, float64(decimals))
	return math.Round(value*multiplier) / multiplier
}

// PercentageChange calculates percentage change between two values
func PercentageChange(oldValue, newValue float64) float64 {
	if oldValue == 0 {
		if newValue == 0 {
			return 0
		}
		return 100 // 100% increase from zero
	}
	return ((newValue - oldValue) / oldValue) * 100
}

// Clamp constrains value between min and max
func Clamp(value, min, max float64) float64 {
	if value < min {
		return min
	}
	if value > max {
		return max
	}
	return value
}

// Time utilities

// FormatDuration formats duration in human-readable format
func FormatDuration(d time.Duration) string {
	if d < time.Minute {
		return "less than a minute"
	} else if d < time.Hour {
		minutes := int(d.Minutes())
		if minutes == 1 {
			return "1 minute"
		}
		return fmt.Sprintf("%d minutes", minutes)
	} else if d < 24*time.Hour {
		hours := int(d.Hours())
		if hours == 1 {
			return "1 hour"
		}
		return fmt.Sprintf("%d hours", hours)
	} else {
		days := int(d.Hours() / 24)
		if days == 1 {
			return "1 day"
		}
		return fmt.Sprintf("%d days", days)
	}
}

// TimeAgo returns human-readable time since given time
func TimeAgo(t time.Time) string {
	return FormatDuration(time.Since(t)) + " ago"
}

// ID generation

// GenerateID creates a random ID string
func GenerateID(length int) (string, error) {
	bytes := make([]byte, length/2)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes)[:length], nil
}

// MustGenerateID creates a random ID string or panics
func MustGenerateID(length int) string {
	id, err := GenerateID(length)
	if err != nil {
		panic(fmt.Sprintf("Failed to generate ID: %v", err))
	}
	return id
}

// Array utilities

// Contains checks if string slice contains a value
func Contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}

// ContainsInt checks if int slice contains a value
func ContainsInt(slice []int, item int) bool {
	for _, i := range slice {
		if i == item {
			return true
		}
	}
	return false
}

// Unique removes duplicates from string slice
func Unique(slice []string) []string {
	keys := make(map[string]bool)
	result := []string{}
	
	for _, item := range slice {
		if !keys[item] {
			keys[item] = true
			result = append(result, item)
		}
	}
	
	return result
}

// Map utilities

// GetStringWithDefault gets string value from map with default
func GetStringWithDefault(m map[string]interface{}, key, defaultValue string) string {
	if value, exists := m[key]; exists {
		if str, ok := value.(string); ok {
			return str
		}
	}
	return defaultValue
}

// GetIntWithDefault gets int value from map with default
func GetIntWithDefault(m map[string]interface{}, key string, defaultValue int) int {
	if value, exists := m[key]; exists {
		switch v := value.(type) {
		case int:
			return v
		case float64:
			return int(v)
		case string:
			if i, err := strconv.Atoi(v); err == nil {
				return i
			}
		}
	}
	return defaultValue
}

// Validation utilities

// IsValidUSState checks if string is a valid US state code
func IsValidUSState(state string) bool {
	validStates := map[string]bool{
		"AL": true, "AK": true, "AZ": true, "AR": true, "CA": true, "CO": true, "CT": true,
		"DE": true, "FL": true, "GA": true, "HI": true, "ID": true, "IL": true, "IN": true,
		"IA": true, "KS": true, "KY": true, "LA": true, "ME": true, "MD": true, "MA": true,
		"MI": true, "MN": true, "MS": true, "MO": true, "MT": true, "NE": true, "NV": true,
		"NH": true, "NJ": true, "NM": true, "NY": true, "NC": true, "ND": true, "OH": true,
		"OK": true, "OR": true, "PA": true, "RI": true, "SC": true, "SD": true, "TN": true,
		"TX": true, "UT": true, "VT": true, "VA": true, "WA": true, "WV": true, "WI": true,
		"WY": true, "DC": true,
	}
	
	return validStates[strings.ToUpper(state)]
}

// Community-specific utilities

// FormatPopulation formats population numbers with commas
func FormatPopulation(pop int) string {
	if pop < 1000 {
		return strconv.Itoa(pop)
	}
	
	str := strconv.Itoa(pop)
	result := ""
	
	for i, char := range str {
		if i > 0 && (len(str)-i)%3 == 0 {
			result += ","
		}
		result += string(char)
	}
	
	return result
}

// FormatResilienceScore formats resilience score as percentage
func FormatResilienceScore(score float64) string {
	percentage := score * 100
	return fmt.Sprintf("%.1f%%", percentage)
}

// CalculateDistance calculates distance between two lat/lng points in kilometers
func CalculateDistance(lat1, lng1, lat2, lng2 float64) float64 {
	const earthRadius = 6371 // Earth's radius in kilometers
	
	dLat := (lat2 - lat1) * math.Pi / 180
	dLng := (lng2 - lng1) * math.Pi / 180
	
	a := math.Sin(dLat/2)*math.Sin(dLat/2) +
		math.Cos(lat1*math.Pi/180)*math.Cos(lat2*math.Pi/180)*
		math.Sin(dLng/2)*math.Sin(dLng/2)
	
	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1-a))
	
	return earthRadius * c
}