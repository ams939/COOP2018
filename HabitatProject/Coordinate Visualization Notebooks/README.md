## Notebooks for visualizing the coordinates in the American Feline datasets

### Short summary of each notebook
Note: For mapping, the notebooks are using a Python module called folium. This module has known issues with rendering while using Chrome, to see all the maps without issues it is recommended to use an alternate browser.

#### Preliminary coordinate visualization notebook
Visualization of the distribution of records that already had coordinates vs. records that were quickly given coordinates using GeoLocate's batch georeference functionality. These results were not verified as this was only a preliminary georeferencing effort to see if it would be beneficial.

#### Geolocate coordinate visualization
A visualization of coordinates acquired from Geolocate after a more thorough georeferencing effort.

#### Coordinate visualization
A visualization of coordinates in all of the data after a thorough georeferencing effort using Geolocate, represents points in the final cleaned dataset.

#### OutOfBounds.txt
A simple text file containing uuid's of records whose coordinates were in invalid areas such as over a waterbody etc. These records were deleted from the final dataset.