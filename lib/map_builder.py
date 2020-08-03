import plotly.express as px
import os


def build_map_figure(data, geojson, indicator):
    return px.choropleth_mapbox(data,  # Data
                                color=f"properties.{indicator}",  # Column giving the color intensity of the region
                                locations='properties.LOCATION',
                                featureidkey='properties.LOCATION',
                                geojson=geojson,  # The GeoJSON file
                                zoom=6,  # Zoom
                                mapbox_style="carto-positron",
                                # Mapbox style, for different maps you need a Mapbox account and a token
                                center={"lat": 7.5, "lon": -75.133},  # Center
                                color_continuous_scale=os.environ.get('MAP_COLOR_SCALE'),  # Color Scheme
                                opacity=0.5,  # Opacity of the map
                                width=900,
                                height=800
                                )
