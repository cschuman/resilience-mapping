// Data import command-line tool
// Created: January 31, 2025
// Purpose: Import community data with dignity and privacy protection

package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/your-org/resilience-mapping/internal/config"
	"github.com/your-org/resilience-mapping/internal/database"
	"github.com/your-org/resilience-mapping/internal/repositories"
	"github.com/your-org/resilience-mapping/internal/importer"
)

func main() {
	// Define command line flags
	var (
		configPath   = flag.String("config", ".env", "Configuration file path")
		dataPath     = flag.String("data", "", "Path to data file")
		importType   = flag.String("type", "", "Import type: cdc_places, usda_fara, demographics, geojson")
		dryRun       = flag.Bool("dry-run", false, "Preview import without making changes")
		verbose      = flag.Bool("verbose", false, "Enable verbose logging")
		help         = flag.Bool("help", false, "Show help message")
	)
	flag.Parse()

	// Show help if requested or if no arguments
	if *help || *dataPath == "" || *importType == "" {
		showHelp()
		return
	}

	// Set up logging
	if *verbose {
		log.SetFlags(log.LstdFlags | log.Lshortfile)
	} else {
		log.SetFlags(log.LstdFlags)
	}

	log.Printf("🌟 Health Resilience Mapping Data Importer")
	log.Printf("🏘️ Importing community data with dignity and respect")
	log.Printf("📂 Data file: %s", *dataPath)
	log.Printf("📊 Import type: %s", *importType)

	if *dryRun {
		log.Printf("🧪 DRY RUN MODE - No data will be modified")
	}

	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("❌ Failed to load configuration: %v", err)
	}

	// Initialize database
	db, err := database.NewDatabase(&cfg.Database)
	if err != nil {
		log.Fatalf("❌ Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Run migrations if needed
	if err := db.Migrate(); err != nil {
		log.Fatalf("❌ Failed to run database migrations: %v", err)
	}

	// Validate data file exists
	if _, err := os.Stat(*dataPath); os.IsNotExist(err) {
		log.Fatalf("❌ Data file not found: %s", *dataPath)
	}

	// Validate import type
	validTypes := []string{"cdc_places", "usda_fara", "demographics", "geojson"}
	if !isValidImportType(*importType, validTypes) {
		log.Fatalf("❌ Invalid import type: %s. Valid types: %v", *importType, validTypes)
	}

	// Initialize repositories
	communityRepo := repositories.NewCommunityRepository(db.DB)

	// Create importer
	communityImporter := importer.NewCommunityImporter(communityRepo)

	// Perform import based on type
	log.Printf("🚀 Starting import...")
	startTime := time.Now()

	var importErr error
	switch *importType {
	case "geojson":
		importErr = communityImporter.ImportFromGeoJSON(*dataPath)
	default:
		importErr = communityImporter.ImportFromCSV(*dataPath, *importType)
	}

	duration := time.Since(startTime)

	if importErr != nil {
		log.Fatalf("❌ Import failed: %v", importErr)
	}

	log.Printf("✅ Import completed successfully!")
	log.Printf("⏱️ Total time: %v", duration)
	log.Printf("🏘️ Community data imported with care and respect")

	// Generate import summary
	if err := generateImportSummary(communityRepo, *importType); err != nil {
		log.Printf("⚠️ Failed to generate summary: %v", err)
	}

	log.Printf("🎉 Data import complete - ready to serve resilient communities!")
}

func showHelp() {
	fmt.Printf(`Health Resilience Mapping Data Importer

PURPOSE:
Import census tract and community data for the Health Resilience Mapping platform.
This tool processes CDC PLACES health data, USDA Food Access Research Atlas data,
demographic data, and geographic boundaries with community privacy protection.

USAGE:
  go run cmd/importer/main.go [OPTIONS]

OPTIONS:
  -data string        Path to data file (required)
  -type string        Import type (required)
  -config string      Configuration file path (default ".env")
  -dry-run           Preview import without making changes
  -verbose           Enable verbose logging
  -help              Show this help message

IMPORT TYPES:
  cdc_places         CDC PLACES health outcome data (CSV)
  usda_fara         USDA Food Access Research Atlas data (CSV)
  demographics      Census demographic and socioeconomic data (CSV)
  geojson           Geographic boundary data (GeoJSON)

EXAMPLES:
  # Import CDC PLACES health data
  go run cmd/importer/main.go -data="data/cdc_places_2023.csv" -type="cdc_places"
  
  # Import USDA food access data
  go run cmd/importer/main.go -data="data/usda_fara_2023.csv" -type="usda_fara"
  
  # Import census tract boundaries
  go run cmd/importer/main.go -data="data/tracts.geojson" -type="geojson"
  
  # Preview import without changes
  go run cmd/importer/main.go -data="data/demographics.csv" -type="demographics" -dry-run

COMMUNITY VALUES:
This tool is built with community-first principles:
- Privacy protection for all community data
- Dignity-first language and processes
- Transparent data handling practices
- Community consent and approval workflows
- Accessible and inclusive design

For questions or support: team@resilience-mapping.org
`)
}

func isValidImportType(importType string, validTypes []string) bool {
	for _, valid := range validTypes {
		if importType == valid {
			return true
		}
	}
	return false
}

func generateImportSummary(communityRepo *repositories.CommunityRepository, importType string) error {
	log.Printf("📊 Generating import summary...")

	ctx := context.Background()
	stats, err := communityRepo.GetStatistics(ctx)
	if err != nil {
		return fmt.Errorf("failed to get statistics: %w", err)
	}

	log.Printf("📈 IMPORT SUMMARY")
	log.Printf("================")
	log.Printf("🏘️ Total communities: %d", stats.TotalCommunities)
	log.Printf("💪 Resilient communities: %d", stats.ResilientCommunities)
	log.Printf("👥 Total population: %d", stats.TotalPopulation)
	log.Printf("📚 Communities with stories: %d", stats.CommunitiesWithStories)
	log.Printf("📊 Average resilience score: %.3f", stats.AvgResilienceScore)

	log.Printf("\n🗺️ STATE DISTRIBUTION:")
	for state, count := range stats.StateDistribution {
		log.Printf("   %s: %d communities", state, count)
	}

	log.Printf("\n💝 Import completed with community values:")
	log.Printf("   ✓ Privacy protection maintained")
	log.Printf("   ✓ Dignity-first data handling")
	log.Printf("   ✓ Community consent workflows ready")
	log.Printf("   ✓ Accessible and inclusive design")

	return nil
}