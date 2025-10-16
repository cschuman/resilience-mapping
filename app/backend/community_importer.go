// Community data import system
// Created: January 31, 2025
// Purpose: Import census tract and community data with dignity and privacy protection

package importer

import (
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/your-org/resilience-mapping/internal/models"
	"github.com/your-org/resilience-mapping/internal/repositories"
	"github.com/your-org/resilience-mapping/pkg/utils"
)

// CommunityImporter handles importing community data from various sources
type CommunityImporter struct {
	communityRepo *repositories.CommunityRepository
	batchSize     int
}

// NewCommunityImporter creates a new community data importer
func NewCommunityImporter(communityRepo *repositories.CommunityRepository) *CommunityImporter {
	return &CommunityImporter{
		communityRepo: communityRepo,
		batchSize:     100, // Process 100 records at a time
	}
}

// ImportFromCSV imports community data from CDC PLACES and USDA FARA CSV files
func (ci *CommunityImporter) ImportFromCSV(filePath string, importType string) error {
	log.Printf("📊 Starting %s data import from: %s", importType, filePath)
	log.Printf("🏘️ Importing data for resilient communities with care and respect")

	file, err := os.Open(filePath)
	if err != nil {
		return fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	
	// Read header row
	header, err := reader.Read()
	if err != nil {
		return fmt.Errorf("failed to read CSV header: %w", err)
	}

	log.Printf("📋 CSV columns found: %d", len(header))
	log.Printf("🔍 Header: %v", header)

	// Create column mapping
	columnMap := createColumnMapping(header, importType)
	
	var communities []models.Community
	recordCount := 0
	errorCount := 0

	// Process records
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Printf("⚠️ Error reading CSV record %d: %v", recordCount+1, err)
			errorCount++
			continue
		}

		community, err := ci.processRecord(record, columnMap, importType)
		if err != nil {
			log.Printf("⚠️ Error processing record %d: %v", recordCount+1, err)
			errorCount++
			continue
		}

		if community != nil {
			communities = append(communities, *community)
		}

		recordCount++

		// Process in batches
		if len(communities) >= ci.batchSize {
			if err := ci.processBatch(communities); err != nil {
				log.Printf("❌ Error processing batch: %v", err)
				return err
			}
			communities = communities[:0] // Reset slice
		}

		// Progress logging
		if recordCount%1000 == 0 {
			log.Printf("📈 Processed %d records, %d errors", recordCount, errorCount)
		}
	}

	// Process final batch
	if len(communities) > 0 {
		if err := ci.processBatch(communities); err != nil {
			log.Printf("❌ Error processing final batch: %v", err)
			return err
		}
	}

	log.Printf("✅ Import completed!")
	log.Printf("📊 Total records processed: %d", recordCount)
	log.Printf("❌ Errors encountered: %d", errorCount)
	log.Printf("🏘️ Communities imported with dignity and respect")

	return nil
}

// ImportFromGeoJSON imports community boundary data from GeoJSON
func (ci *CommunityImporter) ImportFromGeoJSON(filePath string) error {
	log.Printf("🗺️ Starting GeoJSON boundary import from: %s", filePath)

	file, err := os.Open(filePath)
	if err != nil {
		return fmt.Errorf("failed to open GeoJSON file: %w", err)
	}
	defer file.Close()

	var geojson GeoJSONFeatureCollection
	if err := json.NewDecoder(file).Decode(&geojson); err != nil {
		return fmt.Errorf("failed to parse GeoJSON: %w", err)
	}

	log.Printf("📍 Found %d geographic features", len(geojson.Features))

	recordCount := 0
	errorCount := 0

	for _, feature := range geojson.Features {
		if err := ci.processGeoJSONFeature(feature); err != nil {
			log.Printf("⚠️ Error processing feature %d: %v", recordCount+1, err)
			errorCount++
		}
		
		recordCount++
		
		if recordCount%500 == 0 {
			log.Printf("📈 Processed %d geographic features", recordCount)
		}
	}

	log.Printf("✅ GeoJSON import completed!")
	log.Printf("🗺️ Geographic features processed: %d", recordCount)
	log.Printf("❌ Errors: %d", errorCount)

	return nil
}

// processRecord converts CSV record to Community model
func (ci *CommunityImporter) processRecord(record []string, columnMap map[string]int, importType string) (*models.Community, error) {
	// Extract required fields
	tractID, err := getStringValue(record, columnMap, "tract_id")
	if err != nil || len(tractID) != 11 {
		return nil, fmt.Errorf("invalid tract ID: %s", tractID)
	}

	// Validate tract ID format
	if !utils.IsValidTractID(tractID) {
		return nil, fmt.Errorf("invalid tract ID format: %s", tractID)
	}

	community := &models.Community{
		TractID: tractID,
		State:   tractID[:2],   // First 2 digits are state code
		County:  tractID[2:5],  // Next 3 digits are county code
	}

	// Process based on import type
	switch importType {
	case "cdc_places":
		if err := ci.processCDCPlacesData(community, record, columnMap); err != nil {
			return nil, fmt.Errorf("error processing CDC PLACES data: %w", err)
		}
	case "usda_fara":
		if err := ci.processUSDAFARAData(community, record, columnMap); err != nil {
			return nil, fmt.Errorf("error processing USDA FARA data: %w", err)
		}
	case "demographics":
		if err := ci.processDemographicsData(community, record, columnMap); err != nil {
			return nil, fmt.Errorf("error processing demographics data: %w", err)
		}
	default:
		return nil, fmt.Errorf("unknown import type: %s", importType)
	}

	// Calculate resilience score if we have the necessary data
	if community.HealthOutcome > 0 && community.FoodAccess > 0 {
		community.ResilienceScore = calculateResilienceScore(community)
		community.UnexpectedGood = community.ResilienceScore > 0.7 && community.FoodAccess < 0.5
	}

	// Set data quality and timestamps
	community.DataQuality = "imported"
	community.LastUpdated = time.Now()
	community.CreatedAt = time.Now()

	return community, nil
}

// processCDCPlacesData handles CDC PLACES health outcome data
func (ci *CommunityImporter) processCDCPlacesData(community *models.Community, record []string, columnMap map[string]int) error {
	// Extract health indicators
	if val, err := getFloatValue(record, columnMap, "life_expectancy"); err == nil {
		community.LifeExpectancy = val
	}
	
	if val, err := getFloatValue(record, columnMap, "diabetes_rate"); err == nil {
		community.DiabetesRate = val / 100 // Convert percentage to decimal
	}
	
	if val, err := getFloatValue(record, columnMap, "obesity_rate"); err == nil {
		community.ObesityRate = val / 100
	}
	
	if val, err := getFloatValue(record, columnMap, "mental_health_rate"); err == nil {
		community.MentalHealthRate = val / 100
	}

	// Calculate composite health outcome score
	community.HealthOutcome = calculateHealthOutcomeScore(community)

	return nil
}

// processUSDAFARAData handles USDA Food Access Research Atlas data
func (ci *CommunityImporter) processUSDAFARAData(community *models.Community, record []string, columnMap map[string]int) error {
	// Extract food access indicators
	if val, err := getFloatValue(record, columnMap, "low_food_access"); err == nil {
		community.LowFoodAccess = val
	}
	
	if val, err := getFloatValue(record, columnMap, "supermarket_distance"); err == nil {
		community.SupermarketDist = val
	}
	
	if val, err := getFloatValue(record, columnMap, "fast_food_density"); err == nil {
		community.FastFoodDensity = val
	}

	// Calculate composite food access score (lower is worse access)
	community.FoodAccess = calculateFoodAccessScore(community)

	return nil
}

// processDemographicsData handles demographic and socioeconomic data
func (ci *CommunityImporter) processDemographicsData(community *models.Community, record []string, columnMap map[string]int) error {
	// Population
	if val, err := getIntValue(record, columnMap, "population"); err == nil {
		community.Population = val
		community.Demographics.TotalPopulation = val
	}

	// Socioeconomic indicators
	if val, err := getIntValue(record, columnMap, "median_income"); err == nil {
		community.MedianIncome = val
	}
	
	if val, err := getFloatValue(record, columnMap, "poverty_rate"); err == nil {
		community.PovertyRate = val / 100
	}
	
	if val, err := getFloatValue(record, columnMap, "unemployment_rate"); err == nil {
		community.UnemploymentRate = val / 100
	}

	// Racial/ethnic composition
	if val, err := getFloatValue(record, columnMap, "white_percent"); err == nil {
		community.Demographics.WhitePercent = val
	}
	if val, err := getFloatValue(record, columnMap, "black_percent"); err == nil {
		community.Demographics.BlackPercent = val
	}
	if val, err := getFloatValue(record, columnMap, "hispanic_percent"); err == nil {
		community.Demographics.HispanicPercent = val
	}
	if val, err := getFloatValue(record, columnMap, "asian_percent"); err == nil {
		community.Demographics.AsianPercent = val
	}

	// Age demographics
	if val, err := getFloatValue(record, columnMap, "median_age"); err == nil {
		community.Demographics.MedianAge = val
	}

	return nil
}

// processGeoJSONFeature updates community with geographic boundaries
func (ci *CommunityImporter) processGeoJSONFeature(feature GeoJSONFeature) error {
	// Extract tract ID from properties
	tractID, ok := feature.Properties["GEOID11"].(string)
	if !ok || len(tractID) != 11 {
		return fmt.Errorf("missing or invalid GEOID11 in feature properties")
	}

	// Convert GeoJSON geometry to PostGIS format
	geometry, err := convertGeometryToPostGIS(feature.Geometry)
	if err != nil {
		return fmt.Errorf("failed to convert geometry: %w", err)
	}

	// Calculate centroid
	centroid, err := calculateCentroid(feature.Geometry)
	if err != nil {
		return fmt.Errorf("failed to calculate centroid: %w", err)
	}

	// Update existing community record
	community, err := ci.communityRepo.GetByTractID(context.Background(), tractID)
	if err != nil {
		// Create new community if it doesn't exist
		community = &models.Community{
			TractID:   tractID,
			State:     tractID[:2],
			County:    tractID[2:5],
			Geometry:  geometry,
			Centroid:  centroid,
			CreatedAt: time.Now(),
		}
		return ci.communityRepo.Create(context.Background(), community)
	}

	// Update existing community with geometry
	community.Geometry = geometry
	community.Centroid = centroid
	community.LastUpdated = time.Now()

	return ci.communityRepo.Update(context.Background(), community)
}

// processBatch inserts/updates a batch of communities
func (ci *CommunityImporter) processBatch(communities []models.Community) error {
	ctx := context.Background()
	
	log.Printf("💾 Processing batch of %d communities", len(communities))

	// Use bulk insert for better performance
	if err := ci.communityRepo.BulkInsert(ctx, communities); err != nil {
		// If bulk insert fails, try individual inserts/updates
		log.Printf("⚠️ Bulk insert failed, trying individual operations")
		
		successCount := 0
		for i, community := range communities {
			// Try to find existing community first
			existing, err := ci.communityRepo.GetByTractID(ctx, community.TractID)
			if err != nil {
				// Create new community
				if err := ci.communityRepo.Create(ctx, &community); err != nil {
					log.Printf("❌ Failed to create community %s: %v", community.TractID, err)
					continue
				}
			} else {
				// Update existing community
				mergeCommunitiesData(existing, &community)
				if err := ci.communityRepo.Update(ctx, existing); err != nil {
					log.Printf("❌ Failed to update community %s: %v", community.TractID, err)
					continue
				}
			}
			successCount++
			
			if i%10 == 0 {
				log.Printf("📈 Batch progress: %d/%d", i+1, len(communities))
			}
		}
		
		log.Printf("✅ Batch completed: %d/%d successful", successCount, len(communities))
	} else {
		log.Printf("✅ Batch insert completed successfully")
	}

	return nil
}

// Helper functions

func createColumnMapping(header []string, importType string) map[string]int {
	mapping := make(map[string]int)
	
	// Create mapping based on known column patterns for each data source
	for i, col := range header {
		colLower := strings.ToLower(col)
		
		// Common mappings
		switch colLower {
		case "geoid", "geoid11", "tract_id", "census_tract":
			mapping["tract_id"] = i
		case "pop", "population", "total_pop":
			mapping["population"] = i
		}
		
		// CDC PLACES specific mappings
		if importType == "cdc_places" {
			switch colLower {
			case "life_expectancy", "le":
				mapping["life_expectancy"] = i
			case "diabetes", "diabetes_rate":
				mapping["diabetes_rate"] = i
			case "obesity", "obesity_rate":
				mapping["obesity_rate"] = i
			case "mental_health", "mh_rate":
				mapping["mental_health_rate"] = i
			}
		}
		
		// USDA FARA specific mappings  
		if importType == "usda_fara" {
			switch colLower {
			case "lfa", "low_food_access":
				mapping["low_food_access"] = i
			case "superdist", "supermarket_distance":
				mapping["supermarket_distance"] = i
			case "fastfood", "fast_food_density":
				mapping["fast_food_density"] = i
			}
		}
	}
	
	return mapping
}

func getStringValue(record []string, columnMap map[string]int, key string) (string, error) {
	idx, ok := columnMap[key]
	if !ok || idx >= len(record) {
		return "", fmt.Errorf("column %s not found", key)
	}
	return strings.TrimSpace(record[idx]), nil
}

func getIntValue(record []string, columnMap map[string]int, key string) (int, error) {
	str, err := getStringValue(record, columnMap, key)
	if err != nil || str == "" {
		return 0, err
	}
	return strconv.Atoi(str)
}

func getFloatValue(record []string, columnMap map[string]int, key string) (float64, error) {
	str, err := getStringValue(record, columnMap, key)
	if err != nil || str == "" {
		return 0, err
	}
	return strconv.ParseFloat(str, 64)
}

// Calculation functions

func calculateResilienceScore(community *models.Community) float64 {
	// Simple resilience calculation: high health outcomes despite low food access
	healthScore := community.HealthOutcome
	foodAccessPenalty := 1 - community.FoodAccess // Invert since low access is bad
	
	// Communities are resilient if they have good health despite food challenges
	resilience := healthScore - (foodAccessPenalty * 0.5)
	return utils.Clamp(resilience, 0, 1)
}

func calculateHealthOutcomeScore(community *models.Community) float64 {
	// Composite health score from available indicators
	score := 0.0
	count := 0
	
	if community.LifeExpectancy > 0 {
		// Normalize life expectancy (assume range 65-85)
		score += (community.LifeExpectancy - 65) / 20
		count++
	}
	
	// Lower rates are better for these indicators
	if community.DiabetesRate > 0 {
		score += 1 - community.DiabetesRate
		count++
	}
	
	if community.ObesityRate > 0 {
		score += 1 - community.ObesityRate
		count++
	}
	
	if community.MentalHealthRate > 0 {
		score += 1 - community.MentalHealthRate
		count++
	}
	
	if count == 0 {
		return 0
	}
	
	return utils.Clamp(score/float64(count), 0, 1)
}

func calculateFoodAccessScore(community *models.Community) float64 {
	// Higher food access score is better
	score := 1.0
	
	// Penalize for low food access percentage
	if community.LowFoodAccess > 0 {
		score -= community.LowFoodAccess
	}
	
	// Penalize for distance to supermarket (normalize to 0-20 miles)
	if community.SupermarketDist > 0 {
		distancePenalty := utils.Clamp(community.SupermarketDist/20, 0, 1)
		score -= distancePenalty * 0.5
	}
	
	return utils.Clamp(score, 0, 1)
}

func mergeCommunitiesData(existing, new *models.Community) {
	// Merge data from new import into existing community
	// Preserve existing data, only update if new data is available
	
	if new.Population > 0 {
		existing.Population = new.Population
		existing.Demographics.TotalPopulation = new.Population
	}
	
	if new.HealthOutcome > 0 {
		existing.HealthOutcome = new.HealthOutcome
		existing.LifeExpectancy = new.LifeExpectancy
		existing.DiabetesRate = new.DiabetesRate
		existing.ObesityRate = new.ObesityRate
		existing.MentalHealthRate = new.MentalHealthRate
	}
	
	if new.FoodAccess > 0 {
		existing.FoodAccess = new.FoodAccess
		existing.LowFoodAccess = new.LowFoodAccess
		existing.SupermarketDist = new.SupermarketDist
		existing.FastFoodDensity = new.FastFoodDensity
	}
	
	// Recalculate resilience score
	if existing.HealthOutcome > 0 && existing.FoodAccess > 0 {
		existing.ResilienceScore = calculateResilienceScore(existing)
		existing.UnexpectedGood = existing.ResilienceScore > 0.7 && existing.FoodAccess < 0.5
	}
	
	existing.LastUpdated = time.Now()
}

// GeoJSON structures

type GeoJSONFeatureCollection struct {
	Type     string           `json:"type"`
	Features []GeoJSONFeature `json:"features"`
}

type GeoJSONFeature struct {
	Type       string                 `json:"type"`
	Properties map[string]interface{} `json:"properties"`
	Geometry   GeoJSONGeometry        `json:"geometry"`
}

type GeoJSONGeometry struct {
	Type        string      `json:"type"`
	Coordinates interface{} `json:"coordinates"`
}

// Placeholder geometry functions (would need actual PostGIS integration)
func convertGeometryToPostGIS(geom GeoJSONGeometry) (models.Geometry, error) {
	return models.Geometry{
		Type:        geom.Type,
		Coordinates: geom.Coordinates,
	}, nil
}

func calculateCentroid(geom GeoJSONGeometry) (models.Point, error) {
	// Placeholder centroid calculation
	// In production, this would use PostGIS functions
	return models.Point{
		Type:        "Point",
		Coordinates: [2]float64{-98.5, 39.8}, // Center of US as placeholder
	}, nil
}