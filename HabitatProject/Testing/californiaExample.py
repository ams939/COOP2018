#SOM example from https://github.com/sevamoo/SOMPY/blob/master/sompy/examples/California%20Housing.ipynb

import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import fetch_california_housing

data = fetch_california_housing()
descr = data.DESCR
names = fetch_california_housing().feature_names+["HouseValue"]

data1 = np.column_stack([data.data, data.target])
