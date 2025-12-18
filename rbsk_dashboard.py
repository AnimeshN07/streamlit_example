import streamlit as st
import geopandas as gpd
import folium
from folium import GeoJson, Choropleth
from streamlit_folium import folium_static
import pandas as pd
import branca.colormap as cm

# Page configuration
st.set_page_config(
    page_title="Public Health - ICDS Integrated Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        padding: 0.5rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        margin-top: -1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
    }
    /* Reduce spacing before main content */
    .block-container {
        padding-top: 2rem;
    }
    /* Smaller font for summary stats */
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Nandurbar Public Health - ICDS Integrated Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Source : Joint Screening Data - November 2025</p>', unsafe_allow_html=True)

# Load shapefiles
@st.cache_data
def load_rbsk_data():
    gdf = gpd.read_file('rbsk_shapefile_updated_js/rbsk_shapefile_updated_js.shp')
    if gdf.crs is not None:
        gdf = gdf.to_crs(epsg=4326)
    return gdf

@st.cache_data
def load_phc_data():
    gdf = gpd.read_file('phc_shapefile_js/phc_shapefile_js.shp')
    if gdf.crs is not None:
        gdf = gdf.to_crs(epsg=4326)
    return gdf

try:
    # Sidebar for controls
    st.sidebar.header("Dashboard Controls")
    st.sidebar.markdown("---")

    # Layer selection
    selected_layer = st.sidebar.radio(
        "Select Data Layer:",
        ["PHC","RBSK"],
        help="Choose between RBSK or PHC data layer"
    )

    # Load appropriate data based on selection
    if selected_layer == "RBSK":
        gdf = load_rbsk_data()
        column_mapping = {
            'SAM': 'SAM',
            'MAM': 'MAM',
            'Moderately UW': 'Moderately',
            'Severely UW': 'Severely U'
        }
        label_field = 'RBSK Team'
    else:  # PHC
        gdf = load_phc_data()
        column_mapping = {
            'Severely Stunted': 'Severely S',
            'Moderately Stunted': 'Moderate_2',
            'SAM': 'SAM',
            'MAM': 'MAM',
            'Obese': 'Obese',
            'Severely Underweight': 'Severely U',
            'Moderately Underweight': 'Moderately',
            'Overweight': 'Overweight'

        }
        label_field = 'PHC_Name'

    display_names = list(column_mapping.keys())
    actual_columns = list(column_mapping.values())

    st.sidebar.markdown("---")

    # Column selection
    selected_display = st.sidebar.selectbox(
        "Select Health Indicator:",
        display_names,
        help="Choose a health indicator to visualize on the map"
    )

    # Get the actual column name from the mapping
    selected_column = column_mapping[selected_display]

    # Color scheme selection
    color_scheme = st.sidebar.selectbox(
        "Color Scheme:",
        ['YlOrRd', 'RdYlGn_r', 'Blues', 'Reds', 'Greens', 'Purples', 'Viridis'],
        index=0,
        help="Select color scheme for the choropleth map"
    )

    # Label toggle
    show_labels = st.sidebar.checkbox(
        f"Show {selected_layer} Labels",
        value=False,
        help=f"Toggle to show/hide {selected_layer} labels on the map"
    )

    # Legend toggle
    show_legend = st.sidebar.checkbox(
        "Show Legend",
        value=True,
        help="Toggle to show/hide the color legend on the map"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard displays joint screening data (Poshantracker) for RBSK (Rashtriya Bal Swasthya Karyakram) "
        "convergence for November 2025."
    )

    # Main content - Full width map
    st.subheader(f"{selected_layer} - {selected_display}")

    # Calculate center of the map
    bounds = gdf.total_bounds
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2

    # Create folium map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap',
        control_scale=True
    )

    # Add CSS to hide the default white background for custom div icons
    custom_css = """
    <style>
    .custom-div-icon {
        background: transparent !important;
        border: none !important;
    }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    # Prepare data for choropleth
    gdf['selected_value'] = pd.to_numeric(gdf[selected_column], errors='coerce').fillna(0)

    # Create colormap based on selected color scheme
    min_val = gdf['selected_value'].min()
    max_val = gdf['selected_value'].max()

    # Define color palettes
    color_palettes = {
        'YlOrRd': ['#ffffcc', '#ffeda0', '#fed976', '#feb24c', '#fd8d3c', '#fc4e2a', '#e31a1c', '#b10026'],
        'RdYlGn_r': ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850'],
        'Blues': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594'],
        'Reds': ['#fff5f0', '#fee0d2', '#fcbba1', '#fc9272', '#fb6a4a', '#ef3b2c', '#cb181d', '#99000d'],
        'Greens': ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#005a32'],
        'Purples': ['#fcfbfd', '#efedf5', '#dadaeb', '#bcbddc', '#9e9ac8', '#807dba', '#6a51a3', '#4a1486'],
        'Viridis': ['#440154', '#482878', '#3e4989', '#31688e', '#26828e', '#1f9e89', '#35b779', '#6ece58']
    }

    if max_val > min_val:
        # Create step colormap for better legend display
        import numpy as np
        steps = 8
        index = list(np.linspace(min_val, max_val, steps))
        colormap = cm.StepColormap(
            colors=color_palettes[color_scheme],
            index=index,
            vmin=min_val,
            vmax=max_val,
            caption=f'{selected_display} Count'
        )
    else:
        colormap = cm.LinearColormap(
            colors=['#ffffcc', '#ffeda0'],
            vmin=0,
            vmax=1,
            caption=f'{selected_display} Count'
        )

    # Add choropleth layer with styling
    style_function = lambda x: {
        'fillColor': colormap(x['properties']['selected_value']) if x['properties']['selected_value'] is not None else '#gray',
        'color': '#000000',
        'weight': 1.5,
        'fillOpacity': 0.7,
    }

    # Add GeoJson with tooltips (no highlight function to prevent color change on hover)
    tooltip = folium.GeoJsonTooltip(
        fields=[label_field, selected_column],
        aliases=[f'{selected_layer}:', f'{selected_display}:'],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    )

    geojson = folium.GeoJson(
        gdf,
        style_function=style_function,
        tooltip=tooltip,
        name=f'{selected_layer} Layer'
    )
    geojson.add_to(m)

    # Add labels (conditionally based on toggle)
    if show_labels:
        for idx, row in gdf.iterrows():
            if row.geometry is not None and label_field in row:
                # Get centroid for label placement
                centroid = row.geometry.centroid
                folium.Marker(
                    location=[centroid.y, centroid.x],
                    icon=folium.DivIcon(
                        html=f'''
                            <div style="
                                font-size: 10px;
                                font-weight: bold;
                                color: #000;
                                background-color: rgba(255, 255, 255, 0.8);
                                padding: 2px 5px;
                                border-radius: 3px;
                                border: 1px solid #333;
                                text-align: center;
                                white-space: nowrap;
                                width: max-content;
                            ">
                                {row[label_field]}
                            </div>
                        ''',
                        class_name='custom-div-icon'
                    )
                ).add_to(m)

    # Add colormap to map (conditionally based on toggle)
    if show_legend:
        colormap.add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Display map with increased height to fit screen
    folium_static(m, width=None, height=800)

    # Full-width table section
    st.markdown("---")
    st.subheader(f"📋 Detailed Data Table - Sorted by {selected_display}")

    # Prepare table data - dynamically select columns based on layer
    table_columns = [label_field] + actual_columns
    table_data = gdf[table_columns].copy()

    # Create reverse mapping for renaming columns
    reverse_mapping = {v: k for k, v in column_mapping.items()}
    table_data = table_data.rename(columns=reverse_mapping)

    # Convert numeric columns
    for col in display_names:
        if col in table_data.columns:
            table_data[col] = pd.to_numeric(table_data[col], errors='coerce').fillna(0).astype(int)

    # Sort by selected column in descending order (using display name)
    table_data = table_data.sort_values(by=selected_display, ascending=False).reset_index(drop=True)

    # Add rank column
    table_data.insert(0, 'Rank', range(1, len(table_data) + 1))

    # Display styled table
    st.dataframe(
        table_data,
        use_container_width=True,
        height=400,
        hide_index=True
    )

    # Download button
    csv = table_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"{selected_layer.lower()}_data_{selected_display.lower().replace(' ', '_')}.csv",
        mime="text/csv",
        help="Download the current table data as CSV"
    )

    # Additional statistics section
    st.markdown("---")
    st.subheader("📈 Overall Statistics - All Indicators")

    # Create dynamic columns based on number of indicators
    num_indicators = len(display_names)
    cols = st.columns(min(num_indicators, 8))  # Max 8 columns

    stats_data = []
    for col_name in actual_columns:
        total = pd.to_numeric(gdf[col_name], errors='coerce').fillna(0).sum()
        stats_data.append({'Indicator': col_name, 'Total Cases': int(total)})

    stats_df = pd.DataFrame(stats_data)

    # Display metrics dynamically
    for idx, (display_name, actual_name) in enumerate(column_mapping.items()):
        if idx < len(cols):
            with cols[idx]:
                matching_row = stats_df[stats_df['Indicator']==actual_name]
                if not matching_row.empty:
                    total_cases = int(matching_row['Total Cases'].values[0])
                    # Shorten display name for metric if too long
                    short_name = display_name if len(display_name) <= 15 else display_name[:12] + "..."
                    st.metric(short_name, total_cases)

except FileNotFoundError:
    st.error("❌ Shapefile not found. Please ensure 'rbsk_shapefile_updated_js' folder is in the same directory as this script.")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "Public Health - ICDS Integrated Dashboard | Joint Screening Data for November 2024"
    "</p>",
    unsafe_allow_html=True
)
