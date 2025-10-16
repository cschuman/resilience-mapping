// Community models for resilience mapping
// Created: January 31, 2025
// Purpose: Core data structures for 1,059 resilient communities

package models

import (
	"time"
	"database/sql/driver"
	"encoding/json"
	"errors"
)

// Community represents a resilient community census tract
type Community struct {
	ID          int       `json:"id" gorm:"primaryKey;autoIncrement"`
	TractID     string    `json:"tract_id" gorm:"uniqueIndex;size:11;not null"` // GEOID11
	State       string    `json:"state" gorm:"size:2;not null;index"`
	County      string    `json:"county" gorm:"size:3;not null;index"`
	Name        string    `json:"name" gorm:"size:255;not null;index"`
	Population  int       `json:"population" gorm:"not null"`
	
	// Geographic data
	Geometry    Geometry  `json:"geometry" gorm:"type:geometry(MULTIPOLYGON,4326);not null"`
	Centroid    Point     `json:"centroid" gorm:"type:geometry(POINT,4326);not null"`
	
	// Resilience metrics
	HealthOutcome     float64 `json:"health_outcome" gorm:"not null"`
	FoodAccess        float64 `json:"food_access" gorm:"not null"`
	ResilienceScore   float64 `json:"resilience_score" gorm:"not null;index"`
	UnexpectedGood    bool    `json:"unexpected_good" gorm:"not null;index"`
	
	// Demographics
	Demographics      Demographics `json:"demographics" gorm:"embedded"`
	
	// Socioeconomic indicators
	MedianIncome      int     `json:"median_income"`
	PovertyRate       float64 `json:"poverty_rate"`
	UnemploymentRate  float64 `json:"unemployment_rate"`
	
	// Health indicators  
	LifeExpectancy    float64 `json:"life_expectancy"`
	DiabetesRate      float64 `json:"diabetes_rate"`
	ObesityRate       float64 `json:"obesity_rate"`
	MentalHealthRate  float64 `json:"mental_health_rate"`
	
	// Food access indicators
	LowFoodAccess     float64 `json:"low_food_access"`
	SupermarketDist   float64 `json:"supermarket_distance"`
	FastFoodDensity   float64 `json:"fast_food_density"`
	
	// Community assets (for stories)
	CommunityAssets   CommunityAssets `json:"community_assets" gorm:"type:jsonb"`
	
	// Story connections
	Stories           []Story `json:"stories,omitempty" gorm:"foreignKey:CommunityID"`
	StoryCount        int     `json:"story_count" gorm:"default:0"`
	
	// Data quality and metadata
	DataQuality       string    `json:"data_quality" gorm:"size:20;default:'verified'"`
	LastUpdated       time.Time `json:"last_updated" gorm:"autoUpdateTime"`
	CreatedAt         time.Time `json:"created_at" gorm:"autoCreateTime"`
	
	// Community engagement
	ContactInfo       ContactInfo `json:"contact_info,omitempty" gorm:"type:jsonb"`
	CommunityApproved bool        `json:"community_approved" gorm:"default:false"`
	PrivacyLevel      string      `json:"privacy_level" gorm:"size:20;default:'public'"`
}

// Demographics embedded struct
type Demographics struct {
	TotalPopulation    int     `json:"total_population"`
	WhitePercent       float64 `json:"white_percent"`
	BlackPercent       float64 `json:"black_percent"`
	HispanicPercent    float64 `json:"hispanic_percent"`
	AsianPercent       float64 `json:"asian_percent"`
	NativePercent      float64 `json:"native_percent"`
	OtherPercent       float64 `json:"other_percent"`
	MedianAge          float64 `json:"median_age"`
	Under18Percent     float64 `json:"under_18_percent"`
	Over65Percent      float64 `json:"over_65_percent"`
}

// CommunityAssets stores community strengths and resources
type CommunityAssets struct {
	FaithOrganizations    []string `json:"faith_organizations"`
	CommunityOrganizations []string `json:"community_organizations"`
	HealthcareProviders   []string `json:"healthcare_providers"`
	EducationalInstitutions []string `json:"educational_institutions"`
	LocalBusinesses       []string `json:"local_businesses"`
	CommunityGardens      []string `json:"community_gardens"`
	RecreationCenters     []string `json:"recreation_centers"`
	TransportationAssets  []string `json:"transportation_assets"`
	CulturalAssets        []string `json:"cultural_assets"`
}

// ContactInfo for community representatives (privacy-protected)
type ContactInfo struct {
	OrganizationName  string `json:"organization_name,omitempty"`
	ContactPerson     string `json:"contact_person,omitempty"`
	Email             string `json:"email,omitempty"`
	Phone             string `json:"phone,omitempty"`
	Website           string `json:"website,omitempty"`
	PreferredContact  string `json:"preferred_contact,omitempty"`
	PubliclyVisible   bool   `json:"publicly_visible"`
}

// Geometry represents PostGIS geometry data
type Geometry struct {
	Type        string      `json:"type"`
	Coordinates interface{} `json:"coordinates"`
}

// Point represents a geographic point
type Point struct {
	Type        string    `json:"type"`
	Coordinates [2]float64 `json:"coordinates"` // [longitude, latitude]
}

// Value implements driver.Valuer for JSONB storage
func (ca CommunityAssets) Value() (driver.Value, error) {
	return json.Marshal(ca)
}

// Scan implements sql.Scanner for JSONB retrieval
func (ca *CommunityAssets) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("cannot scan non-bytes into CommunityAssets")
	}
	
	return json.Unmarshal(bytes, ca)
}

// Value implements driver.Valuer for JSONB storage
func (ci ContactInfo) Value() (driver.Value, error) {
	return json.Marshal(ci)
}

// Scan implements sql.Scanner for JSONB retrieval
func (ci *ContactInfo) Scan(value interface{}) error {
	if value == nil {
		return nil
	}
	
	bytes, ok := value.([]byte)
	if !ok {
		return errors.New("cannot scan non-bytes into ContactInfo")
	}
	
	return json.Unmarshal(bytes, ci)
}

// GetDisplayName returns a user-friendly name for the community
func (c *Community) GetDisplayName() string {
	if c.Name != "" {
		return c.Name
	}
	return c.TractID
}

// IsHighlyResilient returns true if community has exceptional resilience
func (c *Community) IsHighlyResilient() bool {
	return c.UnexpectedGood && c.ResilienceScore > 0.8
}

// GetPrivacyLevel returns the appropriate privacy level for data sharing
func (c *Community) GetPrivacyLevel() string {
	if c.CommunityApproved && c.PrivacyLevel == "public" {
		return "public"
	}
	return "protected"
}

// HasStories returns true if community has associated stories
func (c *Community) HasStories() bool {
	return c.StoryCount > 0
}

// CanContact returns true if community can be contacted publicly
func (c *Community) CanContact() bool {
	return c.ContactInfo.PubliclyVisible && c.CommunityApproved
}