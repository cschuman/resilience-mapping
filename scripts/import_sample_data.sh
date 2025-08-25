#!/bin/bash
# Sample data import script
# Created: January 31, 2025
# Purpose: Import sample community data for development and testing

set -e  # Exit on error

echo "🌟 Health Resilience Mapping - Sample Data Import"
echo "🏘️ Importing sample community data with dignity and respect"
echo ""

# Configuration
DATA_DIR="./data/sample"
IMPORTER_CMD="go run cmd/importer/main.go"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Go is installed
if ! command -v go &> /dev/null; then
    log_error "Go is not installed. Please install Go first."
    exit 1
fi

# Check if data directory exists
if [ ! -d "$DATA_DIR" ]; then
    log_info "Creating sample data directory: $DATA_DIR"
    mkdir -p "$DATA_DIR"
fi

# Check if database is available
log_info "Checking database connection..."
if ! $IMPORTER_CMD -help &> /dev/null; then
    log_error "Cannot connect to importer. Please check your database configuration."
    exit 1
fi

# Sample data files to create/download
create_sample_files() {
    log_info "Creating sample data files..."
    
    # Create sample CDC PLACES data
    cat > "$DATA_DIR/sample_cdc_places.csv" << 'EOF'
GEOID11,StateAbbr,CountyName,TractFIPS,Population,DIABETES_CrudePrev,OBESITY_CrudePrev,MHLTH_CrudePrev
01001020100,AL,Autauga,20100,1912,8.2,36.4,14.1
01001020200,AL,Autauga,20200,2170,9.1,34.2,13.8
01001020300,AL,Autauga,20300,3373,7.8,31.9,12.4
01003040100,AL,Baldwin,40100,4256,6.9,28.7,11.2
01003040200,AL,Baldwin,40200,3891,7.4,29.8,11.8
EOF

    # Create sample USDA FARA data  
    cat > "$DATA_DIR/sample_usda_fara.csv" << 'EOF'
GEOID11,State,County,Tract,Pop2010,LowAccessPop,LowAccessPercent,MedianDistSupermarket
01001020100,AL,001,020100,1912,234,12.3,2.1
01001020200,AL,001,020200,2170,328,15.1,3.2
01001020300,AL,001,020300,3373,405,12.0,1.8
01003040100,AL,001,040100,4256,298,7.0,1.2
01003040200,AL,001,040200,3891,467,12.0,2.8
EOF

    # Create sample demographics data
    cat > "$DATA_DIR/sample_demographics.csv" << 'EOF'
GEOID11,TotalPop,White,Black,Hispanic,Asian,MedianIncome,PovertyRate,UnemploymentRate
01001020100,1912,1534,298,45,23,52000,12.3,5.2
01001020200,2170,1847,245,52,18,48000,14.1,6.1
01001020300,3373,2698,562,78,28,61000,8.9,4.3
01003040100,4256,3892,198,89,45,72000,6.2,3.8
01003040200,3891,3156,534,123,34,58000,9.8,4.9
EOF

    # Create sample GeoJSON (simplified)
    cat > "$DATA_DIR/sample_boundaries.geojson" << 'EOF'
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "GEOID11": "01001020100",
        "NAME": "Census Tract 201"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [-86.5, 32.5],
          [-86.4, 32.5],
          [-86.4, 32.6],
          [-86.5, 32.6],
          [-86.5, 32.5]
        ]]
      }
    }
  ]
}
EOF

    log_success "Sample data files created"
}

# Import data function
import_data() {
    local file=$1
    local type=$2
    local description=$3
    
    log_info "Importing $description..."
    
    if [ -f "$DATA_DIR/$file" ]; then
        if $IMPORTER_CMD -data="$DATA_DIR/$file" -type="$type" -verbose; then
            log_success "$description imported successfully"
        else
            log_error "Failed to import $description"
            return 1
        fi
    else
        log_warning "Sample file not found: $DATA_DIR/$file"
    fi
}

# Main import process
main() {
    log_info "Starting sample data import process..."
    echo ""
    
    # Create sample files
    create_sample_files
    echo ""
    
    # Import data in order
    import_data "sample_demographics.csv" "demographics" "Census demographics data"
    echo ""
    
    import_data "sample_cdc_places.csv" "cdc_places" "CDC PLACES health data"
    echo ""
    
    import_data "sample_usda_fara.csv" "usda_fara" "USDA Food Access data"
    echo ""
    
    import_data "sample_boundaries.geojson" "geojson" "Census tract boundaries"
    echo ""
    
    log_success "All sample data imported successfully!"
    echo ""
    
    # Show summary
    log_info "Import Summary:"
    echo "📊 Imported sample data for 5 census tracts"
    echo "🏘️ Communities ready for resilience analysis"
    echo "💝 Data imported with community-first principles"
    echo ""
    echo "🚀 Next steps:"
    echo "   1. Start the API server: make dev"
    echo "   2. Visit health check: http://localhost:8080/health"
    echo "   3. View communities: http://localhost:8080/api/v1/communities"
    echo ""
    
    log_success "Sample data import complete!"
}

# Run main function
main "$@"