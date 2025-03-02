import dash
import dash_leaflet as dl
import dash_html_components as html
from dash.dependencies import Output, Input
import geopandas as gpd
import awsS3CityflowTrips
import awsS3Connection


lista_de_opciones = awsS3CityflowTrips.getListRoutesFiles()

dataframe = awsS3Connection.get_data_given_index(lista_de_opciones[0])
gdf = gpd.GeoDataFrame(
    dataframe, 
    geometry=gpd.points_from_xy(dataframe['overlap_origin_long'], dataframe['overlap_origin_lat'])
) 


# Initialize the Dash app
app = dash.Dash(__name__)

# Load and process the GeoJSON file
gdf_shapefile = gpd.read_file('./geojson_hgo.geojson')
gdf_shapefile = gdf_shapefile.to_crs(epsg=4326)

# Convert the full GeoDataFrame to GeoJSON format
geojson_data = gdf_shapefile.to_json()

# Print GeoJSON data to check structure
print("GeoJSON Data:", geojson_data[:1])

# Define the layout of the app

    # Define the layout of the app
app.layout = html.Div([
    dl.Map(center=[gdf_shapefile.geometry.centroid.y.mean(), gdf_shapefile.geometry.centroid.x.mean()], zoom=10, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=gdf_shapefile.to_geo_dict(), id="geojson"),  # No need to filter, just pass full GeoJSON
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block",'opacity': 0.6}),
    html.Div(id='feature-info', children="Click on a feature to see its properties"),
    dl.Map(id='points-map', center=[gdf_shapefile.geometry.centroid.y.mean(), gdf_shapefile.geometry.centroid.x.mean()], zoom=10, children=[
        dl.TileLayer(),
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block",'opacity': 0.6}),
])

# Define the callback to handle click events
@app.callback(
    [Output('feature-info', 'children'),
        Output('points-map', 'children')],
    [Input('geojson', 'clickData')],
)
def display_feature_info(feature):
    print("Clicked Feature:", feature)  # Add this line for debugging
    if feature is not None:
        # Optionally format the properties to make it more readable
        properties = feature
        # Extract the geometry of the clicked feature
        feature_geometry = feature['geometry']
        
        # Convert the feature geometry to a GeoDataFrame
        feature_gdf = gpd.GeoDataFrame.from_features([feature])
        
        # Ensure the CRS matches
        feature_gdf = feature_gdf.set_crs(epsg=4326)
        
        # Filter the original GeoDataFrame to only include points within the feature geometry
        points_within = gdf[gdf.geometry.within(feature_gdf.geometry.iloc[0])]
        
        # Convert the filtered points to a dictionary format for display
        properties = points_within.to_dict('records')
        
        # Create markers for the points within
        markers = [dl.Marker(position=[point.y, point.x]) for point in points_within.geometry]
        
        return html.Pre(str(properties)), [dl.TileLayer()] + markers  # You can format properties as needed
    return "Click on a feature to see its properties", [dl.TileLayer()]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
