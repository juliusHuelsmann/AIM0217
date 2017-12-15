import matplotlib.pyplot as plt
from explsports import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)
import random
from sklearn.manifold import *

maxRequiredSize = 18848 #< amount of lines per time unit. 
k = Sport(sizeLimit=maxRequiredSize) 
k.exportToScript()
