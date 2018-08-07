#Adapted from https://geohackweek.github.io/raster/04-workingwithrasters/

from osgeo import gdal
import matplotlib.pyplot as plt

L8_data = "test.tif"

ds = gdal.Open(L8_data)

pixel_values = ds.ReadAsArray()


plt.imshow(pixel_values)
plt.colorbar()
