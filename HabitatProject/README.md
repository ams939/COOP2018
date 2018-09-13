## American Feline Habitat Project Scripts & Notebooks
### Brief Project Summary
The purpose of this project was to explore the habitats of four species in the Felidae family living within North & South America. A central theme to this project was to test using a Self-Organizing Map machine learning algorithm as an analysis tool for the data collected and learn how this algorihm functions.
To get data on the habitats of species of interest, first the model species were chosen.
The species chosen for this project were large members of the felidae family, namely *Panthera Onca* (Jaguar), *Leopardus Pardalis* (Ocelot), *Puma Concolor* (Mountain Lion) and *Lynx Canadenis* (Canadian Lynx).
Data for these species was acquired by retrieving specimen collection records of these species from Natural History institutes & collectors across the United States.
For this task, iDigBio (https://www.idigbio.org/) was used as the source of data as it is a central repository for digitized collection information from various US institutions.
As this project was concerned with the species habitats, only records with coordinate information or sufficient location information for manual georeferencing were kept from the data available at iDigBio.
For records where georeferencing was possible, it was done using Geo-Locate (http://www.geo-locate.org). A central assumption to the project here is that the location at which the species specimen in the record was collected, corresponds to its habitat location.
Thus to get information on the habitat at this location and quantify it for analysis purposes, the next step in the project was to attach environmental information to each coordinate point in the data.
This environmental information was retrieved in the form of geographic layer files that represented various habitat traits thought to be important for defining that particular habitat.
For this project, environmental layer data for precipitation, temperature, elevation and landcover were chosen as they seemed like they could be some of the defining aspects of a habitat.
These layers were sampled using the species' coordinate data to create a data table containing environmental data at each point for the chosen habitat traits.
This data was then analyzed using the Self-Organizing Map machine learning algorithm to primarily tease out clusters and then visualizing them on a geographic map.
The analysis process with the Self-Organizing Map was completed multiple times to see how changing parameters of the map's training affected the results.

This folder contains all of the scripts and notebooks used for the data cleaning & analysis processes in this project. Documentation & example usage can be found in this repository's "Jupyter Notebooks" folder.

### Folder Contents

The scripts mainly consist of data cleaning scripts which interact with data already housed in a PostgreSQL database, or work to load data into such a database.
Thus to utilize these scripts, a PostgreSQL database is needed for housing the data being processed.
As I was dealing with species data from iDigBio, the scripts expect the database tables & the data within to be in the format of field names and data provided by iDigBio.
Thus, the easiest way to load data into the table is to use my "APIPrototype" project scripts (located elsewhere in this repository) to query iDigBio's data and create the PostgreSQL table needed.

The Jupyter Notebooks in this folder mainly deal with visualizations of the data and creating the project's Self-Organizing Maps.

#### Python Scripts folders
Example usage of scripts can be found in the repository's "Jupyter Notebooks" folder as a Jupyter Notebook titled "Habitat Project Script Usage".

-----------------------------------------------------------------------------------------------------------------------------
**DEPENDENCIES** Scripts written in Python 3.6.4. The Python scripts in this folder require the following packages to operate: 
psycopg2, rasterio, pandas.

**Please also note** that since the scripts are dealing with a PostgreSQL database, the connection details for this database
must be provided for the script. This can be done as follows: The folders "DataCleaner" and "layerExtractor" have a script 
called "DBInfo.py", the connection details to the database need to be set in this scripts "connectDB()" function in both
folders as the other scripts rely on this function for the connection to the local database.
-----------------------------------------------------------------------------------------------------------------------------


**DataCleaner** - Contains "dataCleaner.py" which is a script that contains various functions for cleaning data within a PostgreSQL database. See folder's README for further documentation on functions.

**LayerExtractor** - Contains "layerExtractor.py" which is a script with functions for extracting & managing data from geographical layer data files and storing them in a PostgreSQL database. See folder's README for further documentation on functions.

**Testing** - Contains various scripts used for testing & doodling, not relevant to the functioning of other scripts.


#### Jupyter Notebooks folders
**DEPENDENCIES** Jupyter Notebooks contain code written in Python 3.6.4 and R 3.4.3. Python packages required are: folium. R packages required are: kohonen, ggplot2.

**Coordinate Visualization Notebooks** - Contain notebooks that visualize the coordinates in the species data used in the project. See folder README for more details.

**SOM** - Contains notebooks with various trained networks of the Self-Organized Map using different parameters. In addition, contains notebooks for the geographic visualization of the SOM clustering results.


