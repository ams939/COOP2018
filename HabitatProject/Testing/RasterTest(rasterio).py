import rasterio
import numpy as np
'''
#Printing version number of package (testing purposes)
print(rasterio.__version__)
'''
#Following docs here:
#https://rasterio.readthedocs.io/en/latest/quickstart.html#dataset-georeferencing

dataset = rasterio.open("bio1_test.tif")
dataset2 = rasterio.open("bio12_test.tif")

'''
#Print width and height of dataset
print(dataset.width)
print(dataset.height)
'''

'''
#Print bounds of dataset
print(dataset.bounds)
'''

'''
#Finding coordinates in data using transformation matrices
print(dataset.transform * (dataset.width, 0))
print(dataset2.transform * (dataset2.width, 0))
'''

'''
#Print coordinate system used by dataset
print(dataset.crs)
'''

#Accessing the raster dataset, bands in raster data indexed from 1
band = dataset.read(1) #Puts data in a numpy n-d array
band2 = dataset2.read(1)


#Converting from geographic coordinates to raster coordinates (pixel index)
row, col = dataset.index(-123.061, 40.978)
print(row, col)

#Finding the value of the pixel
print(band[row,col])

#Converting back from pixel index to geographic coordinates
print(dataset.xy(row, col))


'''
Getting the spatial coordinates of a pixel (corners of image).
NOTE: Reversed x and y in arguments(?)

print(dataset.xy(0, dataset.width, offset="ul"))

print(dataset2.xy(0, dataset2.width, offset="ul"))
'''

'''
TODO: Write a program that goes through each pixel, extracts its coordinates
and value into a new table.
'''