INSTALLATION

pip install PointsStatistics

Get Started

from PointsStatistics import PoisStatistics

#%% Define the radius of research around each point

r = 5000

#%% Define directories

# Path to the folder containing all the boundaries that subdived the entire study area
boundariesDir = '...\\boundaries'

# Path to the shapefile of the reference points
pointDir = '...\\pointDir.shp'

# Paths to the shapefile of the points of interest (POIs)
poi1 = '...\\poi1.shp'
poi2 = '...\\poi2.shp'
poi3 = '...\\poi3.shp'
poi4 = '...\\poi4.shp'
poi5 = '...\\poi5.shp'
poi6 = '...\\poi6.shp'

# Path to save the outputs
savingSumDir = '...\\POI_count.csv'
savingNearDir = '...\\POI_near.csv'

# List containing all the paths of the POIs
pois = [poi1, poi2, poi3, poi4, poi5, poi6]

#epsg code of the desired coordinate reference system in the example "UTM - WGS84 zone 32N"
crs = 32632

# Calling the functions
# Function that counts the number of POIs (for each type) inside the radius r of the reference points
# This function adds a column for each POI with the sum of the POIs inside the radius r
tabelloneSum = PoisStatistics(impreseDir).CountPois(provDir, pois, crs, r)

# This function counts the distance between the reference point and the closest POI (for each POI type)
# This function adds a column for each POI with the distance from the reference point
tabelloneNear = PoisStatistics(impreseDir).Nearest(impreseDir, provDir, pois, crs)

#Saving the results to a ".csv" file
tabelloneSum.to_csv(savingSumDir)
tabelloneNear.to_csv(savingNearDir)