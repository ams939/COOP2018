## American Feline Habitat Project Data Legend

#### Species included in this data
Panthera Onca - "Jaguar",
Leopardus Pardalis - "Ocelot",
Puma Concolor - "Mountain Lion/Puma/Cougar",
Lynx Canadensis - "Canadian Lynx"

#### raw_data.zip
Contains the raw species data files used in this project in csv format, UTF-8 encoded. This data was downloaded from www.iDigBio.orq using their Python API.
Data was retrieved in July 2018. All other species data in this folder (Data) has been derived from this raw species data.

#### [species name]_cleaned.csv
Cleaned species data in csv format, UTF-8 encoded. Cleaning entailed choosing relevant columns from the raw data, these being uuid, genus, specific epithet, locality, county, stateprovince and country.   
Cleaning also entailed adding longitude and latitude fields to this data that contain the information within the raw data's "geopoint" field.
Records that had sufficient locality information for georeferencing were georeferenced using Geolocate (www.geo-locate.org), records without coordinates after this step were removed.

#### [species name]_set.csv
Cleaned species data in csv format, UTF-8 encoded. This data is a cut down version of the <species name>_cleaned data, containing only uuid, genus, specificepithet, longitude and latitude from the dataset.
This data has new columns elevation, temperature, precipitation and landcover which are populated with data sampled from geographic layer data as follows:


elevation - USGS's Global Multi-Resolution Terrain Elevation Data 2010 (https://topotools.cr.usgs.gov/gmted_viewer/)

temperature & precipitation - CHELSA Bioclim Datasets "Annual Precipitation" and "Annual Mean Temperature" (http://chelsa-climate.org/downloads/)

landcover - USGS Land Cover Institute's 0.5km MODIS-based Gloval Land Cover Climatology dataset (https://landcover.usgs.gov/global_climatology.php)



All layer files were retreived in August 2018. Layers were cropped to cover North & South America. Sampling of layers was done using Python's rasterio library.

#### feline_data.csv
Combination of the four [species name]_set files into a single csv file thats purpose is to be fed to a Self-Organizing map for data analysis. 
