package feature

import (
	"math"
	"strconv"
	"strings"
)

// ComposeBurden adds a 'burden' column as either z-mean or PCA(1) (PCA todo).
// Input: wide table: header [TractFIPS, StateAbbr, outcomes...]
func ComposeBurden(wide [][]string, outcomes []string, method string) [][]string {
	if len(wide) == 0 { return wide }
	h := indexMap(wide[0])
	// z-score each outcome
	means := make([]float64, len(outcomes))
	sds := make([]float64, len(outcomes))
	// compute means
	for j, o := range outcomes {
		sum := 0.0; n := 0.0
		for i:=1; i<len(wide); i++ {
			v := parseFloat(wide[i][h[o]])
			sum += v; n++
		}
		means[j] = sum / n
	}
	// stddev
	for j, o := range outcomes {
		var ss float64; n := 0.0
		for i:=1; i<len(wide); i++ { v := parseFloat(wide[i][h[o]]); ss += (v - means[j])*(v - means[j]); n++ }
		sds[j] = math.Sqrt(ss / n)
		if sds[j] == 0 { sds[j] = 1 } // avoid div-by-zero
	}
	// z-mean burden
	out := make([][]string, 0, len(wide))
	head := append([]string{}, wide[0]...)
	head = append(head, "burden")
	out = append(out, head)
	for i:=1; i<len(wide); i++ {
		zsum := 0.0
		for j, o := range outcomes {
			v := parseFloat(wide[i][h[o]])
			z := (v - means[j]) / sds[j]
			zsum += z
		}
		burden := zsum / float64(len(outcomes))
		row := append([]string{}, wide[i]...)
		row = append(row, formatFloat(burden))
		out = append(out, row)
	}
	return out
}

func indexMap(hdr []string) map[string]int {
	m := map[string]int{}
	for i,k := range hdr { m[k] = i }
	return m
}

func parseFloat(s string) float64 {
	x, err := strconv.ParseFloat(strings.TrimSpace(s), 64)
	if err != nil { return 0 }
	return x
}

func formatFloat(f float64) string {
	return strconv.FormatFloat(f, 'f', 6, 64)
}
