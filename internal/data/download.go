package data

import (
	"encoding/csv"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/xuri/excelize/v2"

	"github.com/example/resilience-mapping-go/internal/config"
)

func httpGetBytes(url string) ([]byte, error) {
	if url == "" { return nil, errors.New("empty URL") }
	resp, err := http.Get(url)
	if err != nil { return nil, err }
	defer resp.Body.Close()
	if resp.StatusCode >= 300 {
		return nil, fmt.Errorf("GET %s: %s", url, resp.Status)
	}
	return io.ReadAll(resp.Body)
}

func writeFile(path string, b []byte) error {
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil { return err }
	return os.WriteFile(path, b, 0o644)
}

func DownloadAndStage(cfg *config.Config) error {
	// 1) PLACES tract CSV
	if cfg.Paths.PlacesTractCSV != "" {
		b, err := httpGetBytes(cfg.Paths.PlacesTractCSV)
		if err != nil { return err }
		if err := writeFile(filepath.Join(cfg.Paths.RawDir, "places_tract.csv"), b); err != nil { return err }
	}
	// 2) FARA XLSX
	if cfg.Paths.FARAXLSX != "" {
		b, err := httpGetBytes(cfg.Paths.FARAXLSX)
		if err != nil { return err }
		if err := writeFile(filepath.Join(cfg.Paths.RawDir, "fara_2019.xlsx"), b); err != nil { return err }
		// convert selected sheet to CSV into interim
		if err := faraXLSXToCSV(filepath.Join(cfg.Paths.RawDir, "fara_2019.xlsx"), filepath.Join(cfg.Paths.InterimDir, "fara_2019.csv")); err != nil { return err }
	}
	// 3) Tracts SHP zip (optional) — user should convert to GeoJSON externally if desired
	if cfg.Paths.TractsSHPZipURL != "" {
		// Just download; do not extract by default
		b, err := httpGetBytes(cfg.Paths.TractsSHPZipURL)
		if err == nil {
			_ = writeFile(filepath.Join(cfg.Paths.ExternalDir, "cb_2023_us_tract_500k.zip"), b)
		}
	}
	return nil
}

// Pull the first worksheet that contains a GEOID column; write as CSV
func faraXLSXToCSV(xlsxPath, csvOut string) error {
	f, err := excelize.OpenFile(xlsxPath)
	if err != nil { return err }
	defer f.Close()
	sheets := f.GetSheetList()
	var rows [][]string
	for _, sh := range sheets {
		rs, err := f.Rows(sh)
		if err != nil { continue }
		var hdr []string
		for rs.Next() {
			row, _ := rs.Columns()
			if hdr == nil {
				hdr = row
				// sanity: look for GEOID or CensusTract in header
				found := false
				for _, h := range hdr { 
					if strings.EqualFold(h, "GEOID") || strings.EqualFold(h, "CensusTract") { 
						found = true
						break 
					} 
				}
				if !found { 
					rows = nil // reset for next sheet
					break 
				} // try next sheet
				rows = append(rows, hdr)
				continue
			}
			if len(row) == 0 { continue }
			rows = append(rows, row)
		}
		if len(rows) > 1 { break }
	}
	if len(rows) <= 1 {
		return errors.New("could not find FARA sheet with GEOID column; please check xlsx");
	}
	// write csv
	if err := os.MkdirAll(filepath.Dir(csvOut), 0o755); err != nil { return err }
	w, err := os.Create(csvOut)
	if err != nil { return err }
	defer w.Close()
	cw := csv.NewWriter(w)
	defer cw.Flush()
	for _, r := range rows {
		if err := cw.Write(r); err != nil { return err }
	}
	return nil
}
