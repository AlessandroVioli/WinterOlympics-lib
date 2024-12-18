import geopandas as gpd
import folium
import numpy as np
import pandas as pd
    
from folium.plugins import HeatMap

# List Available Functions
def operations():
    """
    Display a list of available functions with short explanations.
    """
    functions_info = [
        ("- load_shapefile(file_path)", "Load a shapefile into a GeoDataFrame.\n"),
        ("- create_map(gdf)", "Create a folium map with markers showing locations and their attributes.\n"),
        ("- calculate_distances(lat, lon, gdf)", "Calculate distances from a given latitude and longitude to points in a GeoDataFrame.\n"),
        ("- get_user_input_and_calculate_distances(gdf)", "Prompt user for coordinates and calculate distances to GeoDataFrame points.\n"),
        ("- save_geodataframe(gdf, file_path, file_format)", "Save a GeoDataFrame to a file in specified format (shp, geojson, csv).\n"),
        ("- filter_by_attribute(gdf, column_name, value)", "Filter the GeoDataFrame by a specific column value.\n"),
        ("- generate_heatmap(gdf)", "Generate a heatmap of point density using folium.\n"),
        ("- save_map_as_html(m, file_path)", "Save a folium map as an HTML file.\n"),
        ("- save_attributes_to_csv(gdf, file_path)", "Save the attribute table of a GeoDataFrame to a CSV file.\n")
    ]
    
    print("Available Functions and Their Descriptions:\n")
    for func, desc in functions_info:
        print(f"{func}: {desc}")




#LOAD SHAPEFILE
# Function to load the shapefile containing the info of the dataframe
def load_shapefile(file_path):
    """
    Load a shapefile into a GeoDataFrame.
    :param file_path: str, path to the shapefile
    :return: GeoDataFrame
    """
    # Reads the shapefile at the specified file path and returns a GeoDataFrame
    return gpd.read_file(file_path)


#CREATE MAP
# Function to create the map in which there are the locations as labels
def create_map(gdf):
    """
    Create a folium map with markers for each point and a popup showing info from the GeoDataFrame.
    :param gdf: GeoDataFrame with latitude and longitude columns
    :return: folium Map object
    """
    # Ensure the GeoDataFrame is in EPSG:4326 (WGS 84) coordinate reference system
    gdf = gdf.to_crs(epsg=4326)
    
    # Create new columns for latitude and longitude from the geometry points
    gdf['latitude'] = gdf.geometry.y
    gdf['longitude'] = gdf.geometry.x
    
    # Calculate the center of the map based on the average latitude and longitude of all points
    map_center = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
    
    # Create a folium map object, centered at the calculated location
    m = folium.Map(location=map_center, zoom_start=8)
    
    # Iterate through each row in the GeoDataFrame and create a marker with information
    for idx, row in gdf.iterrows():
        lat = row['latitude']
        lon = row['longitude']
                
        # Create a string with the information you want to display in the popup
        popup_content = f"""
        <strong>Point ID:</strong> {row.name}<br>
        <strong>Latitude:</strong> {lat}<br>
        <strong>Longitude:</strong> {lon}<br>
        <strong>City:</strong> {row['city']}<br>
        <strong>Venue Name:</strong> {row['venue_name']}<br> 
        <strong>Region:</strong> {row['region']}<br> 
        <strong>Events:</strong> {row['events']}<br> 
        """
    
        # Create a marker with the popup showing location details and add it to the map
        folium.Marker([lat, lon], popup=folium.Popup(popup_content, max_width=300)).add_to(m)
    
    return m

#CALCULATE DISTANCES
# Function to calculate distances from a given latitude and longitude to all points in a GeoDataFrame
def calculate_distances(lat, lon, gdf):
    """
    Calculate distances from a given latitude and longitude to all points in a GeoDataFrame using NumPy.
    :param lat: float, latitude of the starting point
    :param lon: float, longitude of the starting point
    :param gdf: GeoDataFrame with 'latitude' and 'longitude' columns
    :return: DataFrame with distances in kilometers
    """
    # Create new columns for latitude and longitude from the geometry points
    gdf['latitude'] = gdf.geometry.y
    gdf['longitude'] = gdf.geometry.x
    
    # Work on a copy to avoid modifying the original GeoDataFrame
    gdf_copy = gdf
    
    # Ensure the GeoDataFrame is in EPSG:4326 (WGS 84)
    gdf_copy = gdf_copy.to_crs(epsg=4326)
    
    # Convert the user's latitude and longitude to radians for distance calculation
    lat1, lon1 = np.radians(lat), np.radians(lon)
    lat2, lon2 = np.radians(gdf_copy['latitude'].values), np.radians(gdf_copy['longitude'].values)
    
    # Apply the Haversine formula to compute the distance between the two points
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    radius_km = 6371  # Earth's radius in kilometers
    distances = radius_km * c  # Distances in kilometers
    
    # Create a new DataFrame to store the distances along with latitude and longitude
    distance_table = pd.DataFrame({
        'latitude': gdf_copy['latitude'],
        'longitude': gdf_copy['longitude'],
        'distance_km': distances
    })
    
    # Include other relevant columns from the original GeoDataFrame
    other_columns = gdf_copy.columns.difference(['geometry', 'latitude', 'longitude'])
    for col in other_columns:
        distance_table[col] = gdf_copy[col].values
    
    # Sort the table by distance and reset the index
    distance_table = distance_table.sort_values(by='distance_km').reset_index(drop=True)
    
    # Select and return the relevant columns
    distance_table = distance_table[['latitude', 'longitude', 'distance_km', 'city', 'venue_name']]
    return distance_table

#GET USER INPUT AND CALCULATE DISTANCES FROM THE VENUES
# Function to interact with the user and calculate distances based on input
def get_user_input_and_calculate_distances(gdf):
    """
    Prompts the user for latitude and longitude, and calculates the distances to all points in the GeoDataFrame.
    :param gdf: GeoDataFrame with 'latitude' and 'longitude' columns
    :return: DataFrame with distances in kilometers
    """
    # Prompt the user to enter latitude and longitude
    try:
        lat = float(input("Enter latitude: "))
        lon = float(input("Enter longitude: "))
    except ValueError:
        # Handle invalid input (non-numeric values)
        print("Invalid input. Please enter numeric values for latitude and longitude.")
        return None
    
    # Call the calculate_distances function to get the table with distances
    distance_table = calculate_distances(lat, lon, gdf)

    return distance_table

# Save GeoDataFrame to File
def save_geodataframe(gdf, file_path, file_format="shp"):
    """
    Save a GeoDataFrame to a specified file format.
    :param gdf: GeoDataFrame to save
    :param file_path: str, path to save the file
    :param file_format: str, file format ('shp', 'geojson', 'csv')
    """
    if file_format == "shp":
        gdf.to_file(file_path, driver="ESRI Shapefile")
    elif file_format == "geojson":
        gdf.to_file(file_path, driver="GeoJSON")
    elif file_format == "csv":
        gdf.drop(columns='geometry').to_csv(file_path, index=False)
    else:
        raise ValueError("Unsupported file format. Use 'shp', 'geojson', or 'csv'.")

# Filter GeoDataFrame by Attribute
def filter_by_attribute(gdf, column_name, value):
    """
    Filter the GeoDataFrame by a specific attribute.
    :param gdf: GeoDataFrame to filter
    :param column_name: str, name of the column to filter by
    :param value: value to filter for
    :return: Filtered GeoDataFrame
    """
    return gdf[gdf[column_name] == value]

# Generate Heatmap
def generate_heatmap(gdf):
    """
    Generate a heatmap of point density using folium.
    :param gdf: GeoDataFrame with point geometry
    :return: folium Map object
    """
    gdf = gdf.to_crs(epsg=4326)
    heat_data = [[point.y, point.x] for point in gdf.geometry]
    map_center = [gdf.geometry.y.mean(), gdf.geometry.x.mean()]
    m = folium.Map(location=map_center, zoom_start=8)
    HeatMap(heat_data).add_to(m)
    return m

# Save Map as HTML
def save_map_as_html(m, file_path):
    """
    Save a folium map as an HTML file.
    :param m: folium Map object
    :param file_path: str, path to save the HTML file
    """
    m.save(file_path)

# Save Attributes of Shapefile to CSV
def save_attributes_to_csv(gdf, file_path):
    """
    Save the attribute table of a GeoDataFrame to a CSV file.
    :param gdf: GeoDataFrame with attributes
    :param file_path: str, path to save the CSV file
    """
    gdf.drop(columns='geometry').to_csv(file_path, index=False)
