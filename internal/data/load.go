package data

import (
	"encoding/csv"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/example/resilience-mapping-go/internal/config"
)

type Staged struct {
	PLACES [][]string
	FARA   [][]string
}

func LoadCSV(path string) ([][]string, error) {
	f, err := os.Open(path)
	if err != nil { return nil, err }
	defer f.Close()
	r := csv.NewReader(f)
	r.FieldsPerRecord = -1
	rows, err := r.ReadAll()
	if err != nil { return nil, err }
	return rows, nil
}

func LoadStaged(cfg *config.Config) (*Staged, error) {
	p1 := filepath.Join(cfg.Paths.RawDir, "places_tract.csv")
	p2 := filepath.Join(cfg.Paths.InterimDir, "fara_2019.csv")
	pl, err := LoadCSV(p1)
	if err != nil { return nil, fmt.Errorf("load PLACES: %w", err) }
	tar, err := LoadCSV(p2)
	if err != nil { return nil, fmt.Errorf("load FARA: %w", err) }
	return &Staged{PLACES: pl, FARA: tar}, nil
}

// Pivot PLACES from long to wide by MeasureId -> outcome short name
func PivotPLACES(rows [][]string, outcomes []string) ([][]string, error) {
	if len(rows) == 0 { return nil, errors.New("empty PLACES") }
	h := headerIndex(rows[0])
	req := []string{"LocationID","MeasureId","Data_Value","StateAbbr"}
	for _, k := range req { if _, ok := h[k]; !ok { return nil, fmt.Errorf("PLACES missing %s", k) } }
	// map of (tract,state) -> outcome->value
	tab := map[string]map[string]string{}
	for i:=1; i<len(rows); i++ {
		r := rows[i]
		tract := r[h["LocationID"]]
		mid := r[h["MeasureId"]]
		val := r[h["Data_Value"]]
		state := r[h["StateAbbr"]]
		out := measureMap(mid)
		if out == "" { continue }
		if _, ok := tab[tract]; !ok { tab[tract] = map[string]string{"StateAbbr": state} }
		// only keep requested outcomes
		if contains(outcomes, out) {
			tab[tract][out] = val
		}
	}
	// build wide table
	head := []string{"TractFIPS","StateAbbr"}
	head = append(head, outcomes...)
	wide := [][]string{head}
	for tract, m := range tab {
		row := []string{tract, m["StateAbbr"]}
		for _, o := range outcomes {
			row = append(row, m[o])
		}
		wide = append(wide, row)
	}
	return wide, nil
}

func headerIndex(hdr []string) map[string]int {
	m := map[string]int{}
	for i, k := range hdr { m[strings.TrimSpace(k)] = i }
	return m
}

func measureMap(id string) string {
	switch strings.ToUpper(strings.TrimSpace(id)) {
	case "OBESITY": return "obesity"
	case "DIABETES": return "diabetes"
	case "BPHIGH": return "hypertension"
	case "CHD": return "chd"
	case "PHYSINACT": return "physical_inactivity"
	default: return ""
	}
}

func contains(xs []string, x string) bool {
	for _, a := range xs { if a == x { return true } }
	return false
}
