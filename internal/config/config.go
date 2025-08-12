package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
	"github.com/spf13/viper"
)

type Paths struct {
	RawDir          string `mapstructure:"raw_dir"`
	InterimDir      string `mapstructure:"interim_dir"`
	ProcessedDir    string `mapstructure:"processed_dir"`
	ExternalDir     string `mapstructure:"external_dir"`
	FiguresDir      string `mapstructure:"figures_dir"`
	PlacesTractCSV  string `mapstructure:"places_tract_csv_url"`
	FARAXLSX        string `mapstructure:"fara_xlsx_url"`
	TractsSHPZipURL string `mapstructure:"tracts_shp_zip_url"`
	TractsGeoJSON   string `mapstructure:"tracts_geojson_path"`
}

type Model struct {
	Outcomes            []string `mapstructure:"outcomes"`
	BurdenMethod        string   `mapstructure:"burden_method"`
	TopPct              float64  `mapstructure:"top_pct"`
	IncludeNoVehicle    bool     `mapstructure:"include_no_vehicle"`
	StateFixedEffects   bool     `mapstructure:"state_fixed_effects"`
}

type Config struct {
	Paths Paths `mapstructure:"paths"`
	Model Model `mapstructure:"model"`
}

func MustLoad() *Config {
	_ = godotenv.Load() // optional
	viper.SetConfigName("default")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("config")
	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("read config: %v", err)
	}
	// env overrides
	viper.BindEnv("paths.places_tract_csv_url", "PLACES_TRACT_CSV_URL")
	viper.BindEnv("paths.fara_xlsx_url", "FARA_XLSX_URL")
	viper.BindEnv("paths.tracts_shp_zip_url", "TRACTS_SHP_ZIP_URL")
	viper.BindEnv("paths.tracts_geojson_path", "TRACTS_GEOJSON_PATH")

	var cfg Config
	if err := viper.Unmarshal(&cfg); err != nil {
		log.Fatalf("unmarshal: %v", err)
	}
	// ensure dirs exist
	for _, d := range []string{cfg.Paths.RawDir, cfg.Paths.InterimDir, cfg.Paths.ProcessedDir, cfg.Paths.ExternalDir, cfg.Paths.FiguresDir} {
		if d == "" { continue }
		os.MkdirAll(d, 0o755)
	}
	return &cfg
}
