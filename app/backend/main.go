package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"

	"github.com/example/resilience-mapping-go/internal/config"
	"github.com/example/resilience-mapping-go/internal/data"
	"github.com/example/resilience-mapping-go/internal/feature"
	"github.com/example/resilience-mapping-go/internal/model"
	"github.com/example/resilience-mapping-go/internal/geo"
)

func main() {
	root := &cobra.Command{
		Use:   "resilience",
		Short: "Resilience mapping CLI (PLACES × FARA)",
	}

	cfg := config.MustLoad()

	root.AddCommand(&cobra.Command{
		Use:   "data",
		Short: "Download and stage raw data",
		RunE: func(cmd *cobra.Command, args []string) error {
			fmt.Println("Downloading/staging data...")
			return data.DownloadAndStage(cfg)
		},
	})
	root.AddCommand(&cobra.Command{
		Use:   "model",
		Short: "Model expected burden and rank resilience",
		RunE: func(cmd *cobra.Command, args []string) error {
			fmt.Println("Modeling expected burden...")
			staged, err := data.LoadStaged(cfg)
			if err != nil { return err }
			wide, err := data.PivotPLACES(staged.PLACES, cfg.Model.Outcomes)
			if err != nil { return err }
			burdened := feature.ComposeBurden(wide, cfg.Model.Outcomes, cfg.Model.BurdenMethod)
			mtab, res, err := model.ExpectedBurden(burdened, staged.FARA, cfg)
			if err != nil { return err }
			fmt.Printf("OLS R^2: %.3f\n", res.R2)
			return data.SaveModelOutputs(cfg, burdened, mtab)
		},
	})
	root.AddCommand(&cobra.Command{
		Use:   "map",
		Short: "Make map artifacts (requires tracts GeoJSON)",
		RunE: func(cmd *cobra.Command, args []string) error {
			return geo.MakeMaps(cfg)
		},
	})

	// bind env for overrides
	viper.AutomaticEnv()
	if err := root.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
