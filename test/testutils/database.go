// Test utilities for database operations
// Created: January 31, 2025  
// Purpose: Provide testing infrastructure for community-first platform

package testutils

import (
	"context"
	"fmt"
	"log"
	"os"
	"strings"
	"testing"
	"time"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"github.com/your-org/resilience-mapping/internal/config"
	"github.com/your-org/resilience-mapping/internal/database"
	"github.com/your-org/resilience-mapping/internal/models"
	"github.com/your-org/resilience-mapping/pkg/utils"
)

// TestDB provides test database functionality
type TestDB struct {
	*database.Database
	name string
}

// NewTestDB creates a new test database instance
func NewTestDB(t *testing.T) *TestDB {
	// Generate unique database name for this test
	dbName := fmt.Sprintf("resilience_test_%s_%d", 
		utils.GenerateID(8), time.Now().Unix())

	// Get test database URL from environment
	testDBURL := os.Getenv("TEST_DATABASE_URL")
	if testDBURL == "" {
		testDBURL = "postgres://resilience:resilience_dev_password_2025@localhost:5432/postgres?sslmode=disable"
	}

	// Connect to postgres database to create test database
	db, err := gorm.Open(postgres.Open(testDBURL), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		t.Fatalf("Failed to connect to test database: %v", err)
	}

	// Create test database
	sqlDB, _ := db.DB()
	defer sqlDB.Close()

	if err := db.Exec(fmt.Sprintf("CREATE DATABASE %s", dbName)).Error; err != nil {
		t.Fatalf("Failed to create test database: %v", err)
	}

	// Connect to the new test database
	cfg := &config.DatabaseConfig{
		Host:     "localhost",
		Port:     5432,
		User:     "resilience", 
		Password: "resilience_dev_password_2025",
		Name:     dbName,
		SSLMode:  "disable",
		LogLevel: "silent",
		MaxOpenConns: 5,
		MaxIdleConns: 2,
		ConnMaxLifetime: 5 * time.Minute,
		ConnMaxIdleTime: 5 * time.Minute,
	}

	testDB, err := database.NewDatabase(cfg)
	if err != nil {
		t.Fatalf("Failed to connect to test database: %v", err)
	}

	// Run migrations
	if err := testDB.Migrate(); err != nil {
		t.Fatalf("Failed to migrate test database: %v", err)
	}

	log.Printf("🧪 Created test database: %s", dbName)

	return &TestDB{
		Database: testDB,
		name:     dbName,
	}
}

// Close cleans up the test database
func (tdb *TestDB) Close(t *testing.T) {
	log.Printf("🧹 Cleaning up test database: %s", tdb.name)

	// Close the database connection
	tdb.Database.Close()

	// Connect to postgres database to drop test database
	testDBURL := os.Getenv("TEST_DATABASE_URL")
	if testDBURL == "" {
		testDBURL = "postgres://resilience:resilience_dev_password_2025@localhost:5432/postgres?sslmode=disable"
	}

	db, err := gorm.Open(postgres.Open(testDBURL), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		t.Errorf("Failed to connect for cleanup: %v", err)
		return
	}
	defer func() {
		sqlDB, _ := db.DB()
		sqlDB.Close()
	}()

	// Drop test database
	if err := db.Exec(fmt.Sprintf("DROP DATABASE %s", tdb.name)).Error; err != nil {
		t.Errorf("Failed to drop test database: %v", err)
	}

	log.Printf("✅ Test database cleaned up: %s", tdb.name)
}

// SeedTestData creates sample data for testing
func (tdb *TestDB) SeedTestData(t *testing.T) *TestFixtures {
	fixtures := &TestFixtures{}

	// Create admin user
	adminUser := &models.User{
		Email:           "admin@test.org",
		Username:        "testadmin",
		FirstName:       "Test",
		LastName:        "Admin",
		UserType:        "admin",
		Role:           "admin",
		Status:         "active",
		IsVerified:     true,
		EmailVerified:  true,
		ConsentGiven:   true,
		TermsAccepted:  true,
		PrivacyAccepted: true,
		Preferences: models.UserPreferences{
			Theme:    "light",
			Language: "en",
		},
		Notifications: models.NotificationSettings{
			EmailNotifications: true,
		},
	}
	adminUser.SetPassword("TestPassword123!")

	if err := tdb.Create(adminUser).Error; err != nil {
		t.Fatalf("Failed to create admin user: %v", err)
	}
	fixtures.AdminUser = adminUser

	// Create community member user
	memberUser := &models.User{
		Email:           "member@test.org",
		Username:        "testmember",
		FirstName:       "Test",
		LastName:        "Member",
		UserType:        "community_member",
		Role:           "member",
		Status:         "active",
		IsVerified:     true,
		EmailVerified:  true,
		ConsentGiven:   true,
		TermsAccepted:  true,
		PrivacyAccepted: true,
	}
	memberUser.SetPassword("TestPassword123!")

	if err := tdb.Create(memberUser).Error; err != nil {
		t.Fatalf("Failed to create member user: %v", err)
	}
	fixtures.MemberUser = memberUser

	// Create researcher user  
	researcherUser := &models.User{
		Email:           "researcher@test.org",
		Username:        "testresearcher",
		FirstName:       "Test",
		LastName:        "Researcher",
		UserType:        "researcher",
		Role:           "researcher",
		Status:         "active",
		IsVerified:     true,
		EmailVerified:  true,
		ConsentGiven:   true,
		TermsAccepted:  true,
		PrivacyAccepted: true,
		Organization:   "Test University",
		JobTitle:       "Research Scientist",
	}
	researcherUser.SetPassword("TestPassword123!")

	if err := tdb.Create(researcherUser).Error; err != nil {
		t.Fatalf("Failed to create researcher user: %v", err)
	}
	fixtures.ResearcherUser = researcherUser

	// Create test communities
	publicCommunity := &models.Community{
		TractID:         "01001020100",
		State:           "01",
		County:          "001", 
		Name:            "Test Community Public",
		Population:      2500,
		HealthOutcome:   0.75,
		FoodAccess:      0.45,
		ResilienceScore: 0.82,
		UnexpectedGood:  true,
		Demographics: models.Demographics{
			TotalPopulation: 2500,
			MedianAge:       35.5,
		},
		MedianIncome:      55000,
		PovertyRate:       0.12,
		LifeExpectancy:    78.5,
		DataQuality:       "test",
		CommunityApproved: true,
		PrivacyLevel:      "public",
	}

	if err := tdb.Create(publicCommunity).Error; err != nil {
		t.Fatalf("Failed to create public community: %v", err)
	}
	fixtures.PublicCommunity = publicCommunity

	privateCommunity := &models.Community{
		TractID:         "01001020200",
		State:           "01", 
		County:          "001",
		Name:            "Test Community Private",
		Population:      1800,
		HealthOutcome:   0.68,
		FoodAccess:      0.52,
		ResilienceScore: 0.71,
		UnexpectedGood:  false,
		Demographics: models.Demographics{
			TotalPopulation: 1800,
			MedianAge:       41.2,
		},
		MedianIncome:      48000,
		PovertyRate:       0.18,
		LifeExpectancy:    76.8,
		DataQuality:       "test",
		CommunityApproved: false,
		PrivacyLevel:      "private",
	}

	if err := tdb.Create(privateCommunity).Error; err != nil {
		t.Fatalf("Failed to create private community: %v", err)
	}
	fixtures.PrivateCommunity = privateCommunity

	// Associate member user with public community
	memberUser.CommunityID = &publicCommunity.ID
	if err := tdb.Save(memberUser).Error; err != nil {
		t.Fatalf("Failed to associate user with community: %v", err)
	}

	// Create test stories
	publishedStory := &models.Story{
		CommunityID: publicCommunity.ID,
		Title:       "Test Story - Community Resilience",
		Slug:        "test-story-community-resilience",
		Summary:     "A test story about community resilience and strength.",
		Content:     "This is test content for a community resilience story. It demonstrates how communities overcome challenges.",
		StoryType:   "community_strength",
		Category:    "resilience",
		Tags:        []string{"test", "resilience", "community"},
		Status:      "published",
		PublishedAt: timePtr(time.Now().Add(-24 * time.Hour)),
		Storyteller: models.Storyteller{
			Name:      "Test Storyteller",
			Anonymous: false,
			Verified:  true,
		},
		CommunityApproved: true,
		CreatedBy:        memberUser.ID,
		Views:            150,
		Likes:            25,
	}

	if err := tdb.Create(publishedStory).Error; err != nil {
		t.Fatalf("Failed to create published story: %v", err)
	}
	fixtures.PublishedStory = publishedStory

	draftStory := &models.Story{
		CommunityID: publicCommunity.ID,
		Title:       "Test Draft Story",
		Slug:        "test-draft-story",
		Summary:     "A draft story for testing.",
		Content:     "This is draft content.",
		StoryType:   "personal_journey",
		Category:    "health",
		Tags:        []string{"test", "draft"},
		Status:      "draft",
		CreatedBy:   memberUser.ID,
	}

	if err := tdb.Create(draftStory).Error; err != nil {
		t.Fatalf("Failed to create draft story: %v", err)
	}
	fixtures.DraftStory = draftStory

	log.Printf("✅ Test data seeded successfully")
	return fixtures
}

// TestFixtures contains commonly used test data
type TestFixtures struct {
	AdminUser        *models.User
	MemberUser       *models.User
	ResearcherUser   *models.User
	PublicCommunity  *models.Community
	PrivateCommunity *models.Community
	PublishedStory   *models.Story
	DraftStory       *models.Story
}

// ClearTable removes all data from a table
func (tdb *TestDB) ClearTable(t *testing.T, tableName string) {
	if err := tdb.Exec(fmt.Sprintf("TRUNCATE TABLE %s CASCADE", tableName)).Error; err != nil {
		t.Errorf("Failed to clear table %s: %v", tableName, err)
	}
}

// ClearAllTables removes all data from all tables
func (tdb *TestDB) ClearAllTables(t *testing.T) {
	tables := []string{"comments", "stories", "communities", "users"}
	for _, table := range tables {
		tdb.ClearTable(t, table)
	}
}

// AssertCommunityExists checks if a community exists in the database
func (tdb *TestDB) AssertCommunityExists(t *testing.T, tractID string) *models.Community {
	var community models.Community
	if err := tdb.Where("tract_id = ?", tractID).First(&community).Error; err != nil {
		t.Fatalf("Community with tract ID %s should exist: %v", tractID, err)
	}
	return &community
}

// AssertUserExists checks if a user exists in the database
func (tdb *TestDB) AssertUserExists(t *testing.T, email string) *models.User {
	var user models.User
	if err := tdb.Where("email = ?", email).First(&user).Error; err != nil {
		t.Fatalf("User with email %s should exist: %v", email, err)
	}
	return &user
}

// AssertStoryExists checks if a story exists in the database  
func (tdb *TestDB) AssertStoryExists(t *testing.T, slug string) *models.Story {
	var story models.Story
	if err := tdb.Where("slug = ?", slug).First(&story).Error; err != nil {
		t.Fatalf("Story with slug %s should exist: %v", slug, err)
	}
	return &story
}

// CountRows returns the number of rows in a table
func (tdb *TestDB) CountRows(t *testing.T, tableName string) int64 {
	var count int64
	if err := tdb.Table(tableName).Count(&count).Error; err != nil {
		t.Fatalf("Failed to count rows in %s: %v", tableName, err)
	}
	return count
}

// Helper functions

func timePtr(t time.Time) *time.Time {
	return &t
}

// Community-specific test helpers

// CreateTestCommunity creates a community for testing
func (tdb *TestDB) CreateTestCommunity(t *testing.T, tractID string, public bool) *models.Community {
	privacyLevel := "private"
	communityApproved := false
	if public {
		privacyLevel = "public"
		communityApproved = true
	}

	community := &models.Community{
		TractID:           tractID,
		State:             tractID[:2],
		County:            tractID[2:5],
		Name:              fmt.Sprintf("Test Community %s", tractID),
		Population:        2000,
		HealthOutcome:     0.7,
		FoodAccess:        0.5,
		ResilienceScore:   0.75,
		UnexpectedGood:    true,
		DataQuality:       "test",
		CommunityApproved: communityApproved,
		PrivacyLevel:      privacyLevel,
	}

	if err := tdb.Create(community).Error; err != nil {
		t.Fatalf("Failed to create test community: %v", err)
	}

	return community
}

// CreateTestStory creates a story for testing
func (tdb *TestDB) CreateTestStory(t *testing.T, communityID int, userID int, status string) *models.Story {
	story := &models.Story{
		CommunityID: communityID,
		Title:       "Test Story Title",
		Slug:        fmt.Sprintf("test-story-%d", time.Now().Unix()),
		Summary:     "Test story summary",
		Content:     "Test story content",
		StoryType:   "community_strength",
		Category:    "resilience",
		Tags:        []string{"test"},
		Status:      status,
		CreatedBy:   userID,
	}

	if status == "published" {
		now := time.Now()
		story.PublishedAt = &now
		story.CommunityApproved = true
	}

	if err := tdb.Create(story).Error; err != nil {
		t.Fatalf("Failed to create test story: %v", err)
	}

	return story
}

// CreateTestUser creates a user for testing
func (tdb *TestDB) CreateTestUser(t *testing.T, email, userType, role string) *models.User {
	user := &models.User{
		Email:           email,
		Username:        strings.Split(email, "@")[0],
		FirstName:       "Test",
		LastName:        "User",
		UserType:        userType,
		Role:           role,
		Status:         "active",
		IsVerified:     true,
		EmailVerified:  true,
		ConsentGiven:   true,
		TermsAccepted:  true,
		PrivacyAccepted: true,
	}
	user.SetPassword("TestPassword123!")

	if err := tdb.Create(user).Error; err != nil {
		t.Fatalf("Failed to create test user: %v", err)
	}

	return user
}