# RBSK-Poshantracker Convergence Dashboard

A professional interactive dashboard for visualizing RBSK (Rashtriya Bal Swasthya Karyakram) and Poshantracker (ICDS) joint screening data for November 2024.

## Features

- **Interactive Choropleth Map**: Visualize health indicators across RBSK teams with color-coded regions
- **Team Labels**: Clear labels displayed on map geometries showing RBSK team names
- **Multiple Health Indicators**:
  - SAM (Severe Acute Malnutrition)
  - MAM (Moderate Acute Malnutrition)
  - Obese
  - Moderately Underweight
  - Severely Underweight
- **Dynamic Column Selection**: Choose different health indicators to visualize
- **Sorted Data Table**: View all data in descending order by selected indicator
- **Summary Statistics**: Key metrics and overall statistics for all indicators
- **Download Capability**: Export data as CSV for further analysis
- **Professional Styling**: Clean, modern interface with responsive layout

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard using Streamlit:

```bash
streamlit run rbsk_dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Dashboard Components

### Map View
- Choropleth map showing the selected health indicator
- RBSK team labels on each geometry
- Interactive tooltips with team name and indicator value
- Color legend for easy interpretation
- Zoom and pan controls

### Controls (Sidebar)
- **Health Indicator Selection**: Choose which metric to visualize
- **Color Scheme**: Select from multiple color schemes for the choropleth map
- **About Section**: Information about the dashboard

### Data Table
- Displays all RBSK teams with their health indicator values
- Automatically sorted by selected indicator in descending order
- Includes ranking column
- Shows all available health indicators for comparison

### Statistics
- Total number of RBSK teams
- Total cases for selected indicator
- Average cases per team
- Team with highest count
- Overall statistics for all indicators

## Data Structure

The dashboard expects a shapefile with the following columns:
- `RBSK Team`: Team identifier/name
- `SAM`: Severe Acute Malnutrition cases
- `MAM`: Moderate Acute Malnutrition cases
- `Obese`: Obesity cases
- `Moderately`: Moderately Underweight cases
- `Severely U`: Severely Underweight cases

## File Structure

```
app/
├── rbsk_dashboard.py          # Main dashboard application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── rbsk_shapefile_updated_js/ # Shapefile directory
    ├── rbsk_shapefile_updated_js.shp
    ├── rbsk_shapefile_updated_js.dbf
    ├── rbsk_shapefile_updated_js.shx
    ├── rbsk_shapefile_updated_js.prj
    └── rbsk_shapefile_updated_js.cpg
```

## Technologies Used

- **Streamlit**: Web application framework
- **GeoPandas**: Geospatial data processing
- **Folium**: Interactive map visualization
- **Pandas**: Data manipulation and analysis
- **Branca**: Color mapping for choropleth

## Notes

- The shapefile is automatically converted to WGS84 (EPSG:4326) for web mapping
- Numeric values are validated and missing data is handled gracefully
- The map centers automatically based on the shapefile bounds
- All visualizations update dynamically when changing the selected indicator

## Support

For issues or questions, please refer to the shapefile documentation or contact the data administrator.
# streamlit_example
