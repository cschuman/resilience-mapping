package model

import (
	"math"
	"sort"
	"strconv"
	"strings"

	"gonum.org/v1/gonum/mat"

	"github.com/example/resilience-mapping-go/internal/config"
)

type OLSResult struct {
	R2 float64
}

// ExpectedBurden fits: burden ~ LILATracts_1And10 + low_income + rural + no_vehicle_far + State FE
// Returns model table with residuals and a summary (R^2).
func ExpectedBurden(burdened [][]string, fara [][]string, cfg *config.Config) ([][]string, *OLSResult, error) {
	if len(burdened) < 2 || len(fara) < 2 { return nil, nil, nil }
	bh := index(burdened[0])
	fhMap := headerIndex(fara[0])
	fh := index(fara[0])
	// join by TractFIPS (burdened) == GEOID (fara)
	head := []string{"TractFIPS","StateAbbr","burden","resid","resilience_score","GEOID"}
	mtab := [][]string{head}

	// build design matrix rows
	type row struct{ y float64; x []float64; keys []string }
	var rows []row

	// collect state dummies
	states := map[string]struct{}{}
	for i:=1; i<len(burdened); i++ { states[burdened[i][bh("StateAbbr")]] = struct{}{} }
	stateList := make([]string,0,len(states))
	for s := range states { stateList = append(stateList, s) }
	sort.Strings(stateList)
	// drop first for avoid collinearity
	stateIndex := map[string]int{}
	for i:=1; i<len(stateList); i++ { stateIndex[stateList[i]] = i-1 }

	// map FARA rows by GEOID or CensusTract
	fmap := map[string][]string{}
	for i:=1; i<len(fara); i++ {
		geoid := ""
		if idx, ok := fhMap["GEOID"]; ok {
			geoid = fara[i][idx]
		} else if idx, ok := fhMap["CensusTract"]; ok {
			geoid = fara[i][idx]
		}
		if geoid != "" { fmap[geoid] = fara[i] }
	}

	var yvals []float64
	for i:=1; i<len(burdened); i++ {
		tract := burdened[i][bh("TractFIPS")]
		geo := fmap[tract]
		if geo == nil { continue }

		y := parse(burdened[i][bh("burden")])

		x := []float64{1} // intercept
		// LILATracts_1And10
		x = append(x, parse(geo[fh("LILATracts_1And10")]))
		// low income
		x = append(x, parse(geo[fh("LI")]))
		// rural (1 - Urban)
		x = append(x, 1 - parse(geo[fh("Urban")]))
		// no vehicle far
		if cfg.Model.IncludeNoVehicle {
			x = append(x, parse(geo[fh("LA1and10_NoVehicle")]))
		}
		// state FE
		if cfg.Model.StateFixedEffects {
			for i:=1; i<len(stateList); i++ {
				if burdened[i][bh("StateAbbr")] == stateList[i] { // wrong index, fix below
					x = append(x, 1.0)
				} else {
					x = append(x, 0.0)
				}
			}
		}

		geoidKey := ""
		if idx, ok := fhMap["GEOID"]; ok {
			geoidKey = geo[idx]
		} else if idx, ok := fhMap["CensusTract"]; ok {
			geoidKey = geo[idx]
		}
		rows = append(rows, row{y: y, x: x, keys: []string{tract, burdened[i][bh("StateAbbr")], strconv.FormatFloat(y,'f',6,64), geoidKey}})
		yvals = append(yvals, y)
	}

	// Correct state FE construction (we mistakenly used i above), rebuild with proper loop per row
	for ridx := range rows {
		// remove old FE part and rebuild
		x := rows[ridx].x[:]
		baseLen := 1 + 3 + btoi(cfg.Model.IncludeNoVehicle) // intercept + 3 covariates + optional
		x = x[:baseLen]
		st := rows[ridx].keys[1]
		for i:=1; i<len(stateList); i++ {
			if st == stateList[i] { x = append(x, 1.0) } else { x = append(x, 0.0) }
		}
		rows[ridx].x = x
	}

	// Build X and y matrices
	p := len(rows[0].x)
	X := mat.NewDense(len(rows), p, nil)
	Y := mat.NewVecDense(len(rows), nil)
	for i,r := range rows {
		for j:=0; j<p; j++ { X.Set(i,j, r.x[j]) }
		Y.SetVec(i, r.y)
	}
	// Solve OLS via QR
	var qr mat.QR
	qr.Factorize(X)
	beta := mat.NewDense(p, 1, nil)
	Ym := mat.NewDense(len(rows), 1, nil)
	for i := 0; i < len(rows); i++ {
		Ym.Set(i, 0, Y.AtVec(i))
	}
	err := qr.SolveTo(beta, false, Ym)
	if err != nil { return nil, nil, err }
	// predictions & residuals
	pred := mat.NewVecDense(len(rows), nil)
	betaVec := mat.NewVecDense(p, nil)
	for i := 0; i < p; i++ {
		betaVec.SetVec(i, beta.At(i, 0))
	}
	pred.MulVec(X, betaVec)
	resids := mat.NewVecDense(len(rows), nil)
	resids.SubVec(Y, pred)
	// R^2
	meanY := mean(yvals)
	var ssTot, ssRes float64
	for i := 0; i < len(rows); i++ { dy := yvals[i]-meanY; ssTot += dy*dy; e := resids.AtVec(i); ssRes += e*e }
	r2 := 1 - ssRes/ssTot
	// build model table
	// std of residuals for z
	stdev := math.Sqrt(ssRes/float64(len(rows)))
	for i, r := range rows {
		res := resids.AtVec(i)
		score := (-res - 0.0) / (stdev + 1e-9)
		mtab = append(mtab, []string{r.keys[0], r.keys[1], r.keys[2], format(res), format(score), r.keys[3]})
	}
	return mtab, &OLSResult{R2: r2}, nil
}

func index(hdr []string) func(string) int {
	m := map[string]int{}
	for i,k := range hdr { m[strings.TrimSpace(k)] = i }
	return func(s string) int { return m[s] }
}

func headerIndex(hdr []string) map[string]int {
	m := map[string]int{}
	for i, k := range hdr { m[strings.TrimSpace(k)] = i }
	return m
}

func parse(s string) float64 { v, _ := strconv.ParseFloat(strings.TrimSpace(s), 64); return v }
func format(f float64) string { return strconv.FormatFloat(f, 'f', 6, 64) }
func mean(xs []float64) float64 { s:=0.0; for _,v := range xs { s+=v }; return s/float64(len(xs)) }
func btoi(b bool) int { if b { return 1 }; return 0 }
