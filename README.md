# WinterOlympics-lib
A library to manipulate data from the location of the winter olympics
As part of the Geospatial Processing course at Politecnico di Milano, this project aims to create a Python library.
The library consists of several functions:

## Loading and exporting files
- load_shapefile(file_path): Load a shapefile into a GeoDataFrame.

- save_map_as_html(m, file_path): Save a folium map as an HTML file.

- save_attributes_to_csv(gdf, file_path): Save the attribute table of a GeoDataFrame to a CSV file.

## Creating maps
- create_map(gdf): Create a folium map with markers showing locations and their attributes.

- generate_heatmap(gdf): Generate a heatmap of point density using folium.

## Data manipulation
- calculate_distances(lat, lon, gdf): Calculate distances from a given latitude and longitude to points in a GeoDataFrame.

- get_user_input_and_calculate_distances(gdf): Prompt user for coordinates and calculate distances to GeoDataFrame points.

- save_geodataframe(gdf, file_path, file_format): Save a GeoDataFrame to a file in specified format (shp, geojson, csv).

- filter_by_attribute(gdf, column_name, value): Filter the GeoDataFrame by a specific column value.

## Testing the library
The file testing_library.ipynb contains lines of code that test all the functions of the library.

## Installation & Usage

- download the folder 'olympic locations files'
- download the library winter_olympics
  
**Install Required Libraries:**  
In the requirements.txt file are listed all the libraries needed to run the code  
