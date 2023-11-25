import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, MultiPolygon
from shapely.wkt import loads
import os
import matplotlib.pyplot as plt

BASE_DIR = os.getcwd()

# Stops
stops = pd.read_csv(f"{BASE_DIR}/MTA-GTFS-FEED/stops.txt")
stops_lat_lon = stops[['stop_lat', 'stop_lon']]
stop_points = [(stops_lat_lon["stop_lon"][i], stops_lat_lon["stop_lat"][i]) for i in range(len(stops_lat_lon))]

# Convert to GPS Points
gdf_points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lon, lat in stop_points])

# Map districts
gdf = pd.read_csv(f'{BASE_DIR}/MAP-DISTRICTS/nycd.csv')
gdf['the_geom'] = gdf['the_geom'].apply(loads)
gdf = gpd.GeoDataFrame(gdf, geometry='the_geom')


# Ensure CRS is set correctly for both GeoDataFrames
# Example: gdf.set_crs(epsg=4326, inplace=True)
# Example: gdf_points.set_crs(epsg=4326, inplace=True)

joined = gpd.sjoin(gdf_points, gdf, how='inner', op='intersects')

# Plot the polygons
base = joined.plot(color='white', edgecolor='black')

# Plot the points on top, with a different color
gdf_points.plot(ax=base, marker='o', color='red', markersize=5)

# Customizing the plot
plt.title('Spatial Join Results')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Display the plot
plt.show()
