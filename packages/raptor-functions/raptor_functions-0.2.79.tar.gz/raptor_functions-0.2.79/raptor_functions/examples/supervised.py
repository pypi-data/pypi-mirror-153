import os
import sys
import glob
import numpy as np
import pandas as pd


PACKAGE_FOLDER =  os.environ.get('PACKAGE_FOLDER')
<<<<<<< HEAD
PACKAGE_FOLDER = '/media/psf/Desktop/Projects/Raptor/raptor_functions'
PACKAGE_FOLDER = '/raptor/raptor_functions' #'/home/raptor_functions' '/raptor/raptor_functions
=======
PACKAGE_FOLDER = '/Users/danielfiuzadosil/Documents/GitHub/raptor_functions/raptor_functions'

>>>>>>> e114c4e285d423eaf9202881d7c7be055031a323
print(PACKAGE_FOLDER)
# sys.path.insert(0, PACKAGE_FOLDER)
sys.path.append(PACKAGE_FOLDER)


import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import mlflow
# import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from raptor_functions.supervised.train import train_experiments
from raptor_functions.supervised.datasets import get_data
from raptor_functions.supervised.feature_extraction import get_training_features



df = get_data('handheld_data')

forest = RandomForestClassifier()
df = get_training_features(df, offset=False, gradient=False, tree_model=forest)

train_experiments(df)