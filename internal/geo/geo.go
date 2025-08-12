package geo

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/paulmach/orb/geojson"

	"github.com/example/resilience-mapping-go/internal/config"
	"github.com/example/resilience-mapping-go/internal/data"
)

func MakeMaps(cfg *config.Config) error {
	gpath := cfg.Paths.TractsGeoJSON
	if gpath == "" { return fmt.Errorf("no tracts_geojson_path configured") }
	b, err := os.ReadFile(gpath)
	if err != nil { return err }
	fc, err := geojson.UnmarshalFeatureCollection(b)
	if err != nil { return err }

	// load model table
	mtab, err := data.LoadCSV(filepath.Join(cfg.Paths.ProcessedDir, "model_table_with_residuals.csv"))
	if err != nil { return err }
	m := map[string]map[string]string{}
	mh := headerIdx(mtab[0])
	for i:=1; i<len(mtab); i++ {
		geoid := mtab[i][mh["GEOID"]]
		m[geoid] = map[string]string{
			"resilience_score": mtab[i][mh["resilience_score"]],
			"burden": mtab[i][mh["burden"]],
			"resid": mtab[i][mh["resid"]],
		}
	}

	// join onto features
	for _, f := range fc.Features {
		geoid := propString(f.Properties, "GEOID")
		if geoid == "" { continue }
		if v, ok := m[geoid]; ok {
			for k, s := range v {
				// try numeric
				if x, err := strconv.ParseFloat(s, 64); err == nil {
					f.Properties[k] = x
				} else {
					f.Properties[k] = s
				}
			}
		}
	}
	// write joined geojson
	if err := os.MkdirAll(cfg.Paths.FiguresDir, 0o755); err != nil { return err }
	outgj := filepath.Join(cfg.Paths.FiguresDir, "resilience.geojson")
	bb, _ := json.MarshalIndent(fc, "", "  ")
	if err := os.WriteFile(outgj, bb, 0o644); err != nil { return err }

	// write a tiny Leaflet page
	html := `<!doctype html><html><head><meta charset="utf-8"/><title>Resilience Map</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>#map{height:92vh}</style></head><body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const map = L.map('map').setView([39.5,-98.35], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18}).addTo(map);
fetch('resilience.geojson').then(r=>r.json()).then(gj=>{
  function getColor(s){ // simple quantiles
    const v = s==null?null:parseFloat(s);
    if (v==null || isNaN(v)) return '#cccccc';
    if (v>1.5) return '#08306b';
    if (v>0.5) return '#2171b5';
    if (v>-0.5) return '#6baed6';
    if (v>-1.5) return '#c6dbef';
    return '#eff3ff';
  }
  L.geoJSON(gj, {
    style: f => ({color:'#999', weight: 0.2, fillOpacity: 0.9, fillColor: getColor(f.properties.resilience_score)}),
    onEachFeature: (f, layer) => {
      const p=f.properties;
      const html = '<b>Tract:</b> '+(p.GEOID||'')+'<br/>' +
                   '<b>Resilience z:</b> '+(p.resilience_score?.toFixed? p.resilience_score.toFixed(2) : p.resilience_score) + '<br/>' +
                   '<b>Burden:</b> '+(p.burden||'') + '<br/>' +
                   '<b>Resid:</b> '+(p.resid||'');
      layer.bindPopup(html);
    }
  }).addTo(map);
});
</script></body></html>`
	if err := os.WriteFile(filepath.Join(cfg.Paths.FiguresDir, "index.html"), []byte(html), 0o644); err != nil { return err }
	return nil
}

func headerIdx(h []string) map[string]int { m:=map[string]int{}; for i,k := range h { m[strings.TrimSpace(k)] = i }; return m }
func propString(p map[string]interface{}, key string) string { if v,ok := p[key]; ok { if s,ok2 := v.(string); ok2 { return s } }; return "" }
