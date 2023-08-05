import numpy as np
import pandas as pd
import xgboost as xgb
from boruta import BorutaPy
from tsfresh.utilities.dataframe_functions import impute
from tsfresh.feature_extraction import (
    ComprehensiveFCParameters,
    extract_features,
)
from tsfresh import extract_features
from .preprocess import offset_batch_samples, gradient_batch_samples


FEATURES = [
    "exp_unique_id",
    "timesteps",
    "sensor_1",
    "sensor_2",
    "sensor_3",
    "sensor_4",
    "sensor_5",
    "sensor_6",
    "sensor_7",
    "sensor_8",
    "sensor_9",
    "sensor_10",
    "sensor_11",
    "sensor_12",
    "sensor_13",
    "sensor_14",
    "sensor_15",
    "sensor_16",
    "sensor_17",
    "sensor_18",
    "sensor_19",
    "sensor_20",
    "sensor_21",
    "sensor_22",
    "sensor_23",
    "sensor_24",
]

TARGET_COL = "result"

extraction_settings = ComprehensiveFCParameters()


def get_all_features(
    X,
    unique_id="exp_unique_id",
    # label="result",
    timesteps="timesteps",
    features=FEATURES,
):

    features = [col for col in X if col.startswith('sensor')]
    features = [unique_id, timesteps] + features

    X = X[features]

    # X = df.drop(label, axis=1)
    # y = df.groupby(unique_id).first()[label]

    X_extracted = extract_features(
        X,
        column_id=unique_id,
        column_sort=timesteps,
        default_fc_parameters=extraction_settings,
        # we impute = remove all NaN features automatically
        impute_function=impute,
    )

    return X_extracted


xgb = xgb.XGBClassifier()



def select_relevant_features(X, y, tree_model=xgb):

    boruta = BorutaPy(
            estimator=tree_model,
            n_estimators="auto",
            max_iter=50,  # number of trials to perform
        )

    # fit Boruta (it accepts np.array, not pd.DataFrame)
    boruta.fit(np.array(X), np.array(y))

    # green and blue area are the important features identified by boruta algorithm
    green_area = X.columns[boruta.support_].to_list()
    blue_area = X.columns[boruta.support_weak_].to_list()

    relevant_features = green_area + blue_area
    X = X[relevant_features]

    return  X

unique_id="exp_unique_id"
label="result"
timesteps="timesteps"

def add_offset_gradient(X_raw, offset=False, gradient=False):

    
    X_all = []
    X_all.append(X_raw)

    if offset:
        X_offset = offset_batch_samples(X_raw)
        X_offset = X_offset.add_suffix(f'_offset')
        X_all.append(X_offset)

    if gradient:
        X_gradient = gradient_batch_samples(X_raw)
        X_gradient = X_gradient.add_suffix(f'_gradient')
        X_all.append(X_gradient)

    

    X_all = pd.concat(X_all, axis=1)

    return X_all

def get_training_features(df, offset=False, gradient=False, tree_model=xgb):
    y = df.groupby(unique_id).first()[label]
    X = df.drop(label, axis=1)
    X = add_offset_gradient(X, offset, gradient)
    print('Extracting all features')
    X = get_all_features(X)
    print('Selecting relevant features')
    X = select_relevant_features(X, y, tree_model=tree_model)

    df = X.join(y)

    return df



















































# import numpy as np
# import pandas as pd
# import xgboost as xgb
# from boruta import BorutaPy
# from tsfresh.utilities.dataframe_functions import impute
# from tsfresh.feature_extraction import (
#     ComprehensiveFCParameters,
#     extract_features,
# )
# from tsfresh import extract_features
# from .preprocess import offset_batch_samples, gradient_batch_samples


# FEATURES = [
#     "exp_unique_id",
#     "timesteps",
#     "sensor_1",
#     "sensor_2",
#     "sensor_3",
#     "sensor_4",
#     "sensor_5",
#     "sensor_6",
#     "sensor_7",
#     "sensor_8",
#     "sensor_9",
#     "sensor_10",
#     "sensor_11",
#     "sensor_12",
#     "sensor_13",
#     "sensor_14",
#     "sensor_15",
#     "sensor_16",
#     "sensor_17",
#     "sensor_18",
#     "sensor_19",
#     "sensor_20",
#     "sensor_21",
#     "sensor_22",
#     "sensor_23",
#     "sensor_24",
#     "result",
# ]

# TARGET_COL = "result"

# extraction_settings = ComprehensiveFCParameters()





# def get_features(
#     df,
#     unique_id="exp_unique_id",
#     label="result",
#     timesteps="timesteps",
#     features=FEATURES,
#     offset=False,
#     gradient=False
# ):

#     df = df[features]

#     X = df.drop(label, axis=1)
#     y = df.groupby(unique_id).first()[label]

#     X_all = []



#     print('Extracting feature from raw signals')

#     X_raw = extract_features(
#         X,
#         column_id=unique_id,
#         column_sort=timesteps,
#         default_fc_parameters=extraction_settings,

#         # we impute = remove all NaN features automatically
#         impute_function=impute,
#     )

#     X_all.append(X_raw)



#     if offset:
#         print('Extracting features from offset signals')
#         X_offset = offset_batch_samples(X)

#         X_offset = extract_features(
#             X,
#             column_id=unique_id,
#             column_sort=timesteps,
#             default_fc_parameters=extraction_settings,

#             # we impute = remove all NaN features automatically
#             impute_function=impute,
#         )

#         X_all.append(X_offset)

#     if gradient:
#         print('Extracting features from gradient signals')
#         X_gradient = gradient_batch_samples(X)
#         X_gradient = extract_features(
#             X,
#             column_id=unique_id,
#             column_sort=timesteps,
#             default_fc_parameters=extraction_settings,

#             # we impute = remove all NaN features automatically
#             impute_function=impute,
#         )
#         X_all.append(X_gradient) 

    

#     X = pd.concat(X_all, axis=1)


#     df = X.join(y)

#     return df, X, y


# xgb = xgb.XGBClassifier()


# def get_relevant_features(X, y, tree_model=xgb):

#     boruta = BorutaPy(
#         estimator=tree_model,
#         n_estimators="auto",
#         max_iter=100,  # number of trials to perform
#     )

#     # fit Boruta (it accepts np.array, not pd.DataFrame)
#     boruta.fit(np.array(X), np.array(y))

#     # green and blue area are the important features identified by boruta algorithm
#     green_area = X.columns[boruta.support_].to_list()
#     blue_area = X.columns[boruta.support_weak_].to_list()

#     relevant_features = green_area + blue_area
#     X = X[relevant_features]

#     df = X.join(y)

#     return df, X, y
