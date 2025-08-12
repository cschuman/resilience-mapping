package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/xuri/excelize/v2"
)

func main() {
	// Path to the Excel file
	filePath := "/Users/corey/Projects/resilience-mapping-go/data/raw/fara_2019.xlsx"
	
	// Open the Excel file
	f, err := excelize.OpenFile(filePath)
	if err != nil {
		log.Fatalf("Failed to open Excel file: %v", err)
	}
	defer func() {
		if err := f.Close(); err != nil {
			log.Printf("Failed to close Excel file: %v", err)
		}
	}()

	// Get all sheet names
	sheetNames := f.GetSheetList()
	fmt.Printf("Excel file: %s\n", filePath)
	fmt.Printf("Total sheets found: %d\n\n", len(sheetNames))

	// Define possible GEOID column name variations
	possibleGEOIDNames := []string{
		"geoid", "GEOID", "Geoid", "GeoId", "GeoID",
		"censustract", "CENSUSTRACT", "CensusTract", "Census_Tract", "census_tract",
		"tract", "TRACT", "Tract", "tract_id", "TRACT_ID", "TractID",
		"fips", "FIPS", "Fips", "fips_code", "FIPS_CODE", "FipsCode",
		"id", "ID", "Id", "identifier", "IDENTIFIER", "Identifier",
		"code", "CODE", "Code", "geo_code", "GEO_CODE", "GeoCode",
	}

	// Process each sheet
	for i, sheetName := range sheetNames {
		fmt.Printf("=== Sheet %d: %s ===\n", i+1, sheetName)
		
		// Get the first row (headers)
		rows, err := f.GetRows(sheetName)
		if err != nil {
			fmt.Printf("Error reading sheet %s: %v\n\n", sheetName, err)
			continue
		}
		
		if len(rows) == 0 {
			fmt.Printf("Sheet %s is empty\n\n", sheetName)
			continue
		}
		
		// Display header columns
		headers := rows[0]
		fmt.Printf("Total columns: %d\n", len(headers))
		fmt.Printf("Header columns:\n")
		for j, header := range headers {
			fmt.Printf("  [%d] %s\n", j, header)
		}
		
		// Check for potential GEOID columns
		fmt.Printf("\nPotential GEOID columns found:\n")
		foundGEOID := false
		for j, header := range headers {
			headerLower := strings.ToLower(strings.TrimSpace(header))
			for _, possibleName := range possibleGEOIDNames {
				if headerLower == strings.ToLower(possibleName) {
					fmt.Printf("  [%d] %s (matches: %s)\n", j, header, possibleName)
					foundGEOID = true
					break
				}
			}
		}
		
		if !foundGEOID {
			fmt.Printf("  No exact matches found for common GEOID column names\n")
			
			// Look for partial matches
			fmt.Printf("\nPossible partial matches:\n")
			for j, header := range headers {
				headerLower := strings.ToLower(strings.TrimSpace(header))
				for _, possibleName := range possibleGEOIDNames {
					possibleLower := strings.ToLower(possibleName)
					if strings.Contains(headerLower, possibleLower) || strings.Contains(possibleLower, headerLower) {
						fmt.Printf("  [%d] %s (partial match with: %s)\n", j, header, possibleName)
						break
					}
				}
			}
		}
		
		// Show first few data rows to understand the structure
		fmt.Printf("\nFirst 3 data rows (excluding header):\n")
		maxRows := 4 // header + 3 data rows
		if len(rows) > maxRows {
			maxRows = len(rows)
		}
		if maxRows > 4 {
			maxRows = 4
		}
		
		for rowIdx := 1; rowIdx < maxRows && rowIdx < len(rows); rowIdx++ {
			row := rows[rowIdx]
			fmt.Printf("  Row %d: ", rowIdx)
			for colIdx := 0; colIdx < len(row) && colIdx < 10; colIdx++ { // Show first 10 columns
				if colIdx > 0 {
					fmt.Printf(" | ")
				}
				cellValue := row[colIdx]
				if len(cellValue) > 20 {
					cellValue = cellValue[:17] + "..."
				}
				fmt.Printf("%s", cellValue)
			}
			if len(row) > 10 {
				fmt.Printf(" | ... (%d more columns)", len(row)-10)
			}
			fmt.Printf("\n")
		}
		
		fmt.Printf("\n" + strings.Repeat("-", 80) + "\n\n")
	}
	
	fmt.Printf("Analysis complete!\n")
	fmt.Printf("\nSUMMARY:\n")
	fmt.Printf("- File: %s\n", filePath)
	fmt.Printf("- Total sheets: %d\n", len(sheetNames))
	for _, sheetName := range sheetNames {
		fmt.Printf("  - %s\n", sheetName)
	}
}