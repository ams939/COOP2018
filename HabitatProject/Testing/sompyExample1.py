#Testing out the sompy python library

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from time import time

dlen = 200
#Creates a dataframe with 200 rows and 2 columns if values 0-1
Data1 = pd.DataFrame(data= 1*np.random.rand(dlen,2))

#Replaces the second column with a modification of the first column
Data1.values[:,1] = (Data1.values[:,0][:,np.newaxis] + .42*np.random.rand(dlen,1))[:,0]
#Functionality of np.newaxis https://stackoverflow.com/questions/29241056/how-does-numpy-newaxis-work-and-when-to-use-it
#Essentially [:,1] turns second original column into array, 
#np.newaxis turns back into column (vector) and [:,0] turns new column back to array
#that will replace to second column in the original data


Data2 = pd.DataFrame(data= 1*np.random.rand(dlen,2)+1)
Data2.values[:,1] = (-1*Data2.values[:,0][:,np.newaxis] + .62*np.random.rand(dlen,1))[:,0]

Data3 = pd.DataFrame(data= 1*np.random.rand(dlen,2)+2)
Data3.values[:,1] = (.5*Data3.values[:,0][:,np.newaxis] + 1*np.random.rand(dlen,1))[:,0]


Data4 = pd.DataFrame(data= 1*np.random.rand(dlen,2)+3.5)
Data4.values[:,1] = (-.1*Data4.values[:,0][:,np.newaxis] + .5*np.random.rand(dlen,1))[:,0]

Data = np.concatenate((Data1, Data2, Data3, Data4))

fig = plt.figure()
plt.plot(Data[:,0],Data[:,1],'ob',alpha=0.2, markersize=4)
fig.set_size_inches(7,7)