import plotly.express as px

color_scale = [
    "rgb(0,104,55)",
    "rgb(26,152,80)",
    "rgb(102,189,99)",
    "rgb(166,217,106)",
    "rgb(217,239,139)",
    "rgb(255,255,191)",
    "rgb(254,224,139)",
    "rgb(253,174,97)",
    "rgb(244,109,67)",
    "rgb(215,48,39)",
    "rgb(165,0,38)",
]


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
                                color_continuous_scale=color_scale,  # Color Scheme
                                opacity=0.5,  # Opacity of the map
                                width=900,
                                height=800

                                )
