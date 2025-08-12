package data

import (
	"encoding/csv"
	"os"
	"path/filepath"

	"github.com/example/resilience-mapping-go/internal/config"
)

func SaveCSV(path string, rows [][]string) error {
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil { return err }
	f, err := os.Create(path)
	if err != nil { return err }
	defer f.Close()
	w := csv.NewWriter(f)
	defer w.Flush()
	for _, r := range rows { if err := w.Write(r); err != nil { return err } }
	return nil
}

func SaveModelOutputs(cfg *config.Config, burdened [][]string, mtab [][]string) error {
	if err := SaveCSV(filepath.Join(cfg.Paths.ProcessedDir, "burden_table.csv"), burdened); err != nil { return err }
	if err := SaveCSV(filepath.Join(cfg.Paths.ProcessedDir, "model_table_with_residuals.csv"), mtab); err != nil { return err }
	return nil
}
