import joblib
from io import BytesIO
import boto3
import mlflow
from mlflow.tracking import MlflowClient
from tsfresh.feature_extraction import settings, extract_features
from .feature_extraction import add_offset_gradient



REMOTE_TRACKING_URI = 'http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/'


def load_model(path):
    """ 
    Function to load a joblib file from an s3 bucket or local directory.
    Arguments:
    * path: an s3 bucket or local directory path where the file is stored
    Outputs:
    * file: Joblib file loaded
    """

    # Path is an s3 bucket
    if path[:5] == "s3://":
        s3_bucket, s3_key = path.split("/")[2], path.split("/")[3:]
        s3_key = "/".join(s3_key)
        with BytesIO() as f:
            boto3.client("s3").download_fileobj(Bucket=s3_bucket, Key=s3_key, Fileobj=f)
            f.seek(0)
            file = joblib.load(f)

    # Path is a local directory
    else:
        with open(path, "rb") as f:
            file = joblib.load(f)

    return file



def get_model_and_features(model_uri, tracking_uri=REMOTE_TRACKING_URI):
    
    client = MlflowClient(tracking_uri=tracking_uri)
    
    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(model_uri)
    run_id = loaded_model.metadata.run_id
    relevant_features = client.get_run(run_id).data.tags['relevant_features'].replace("'", '')[1:-1].split(', ')
    offset = bool(client.get_run(run_id).data.tags['offset'])
    gradient = bool(client.get_run(run_id).data.tags['gradient'])

    return loaded_model, relevant_features, offset, gradient




def get_prediction_features(
    X, model_uri, tracking_uri=REMOTE_TRACKING_URI,  id="exp_unique_id", timesteps="timesteps"
):


    
    _, relevant_features, offset, gradient = get_model_and_features(model_uri)

    X = add_offset_gradient(X, offset=offset, gradient=gradient)
    # df = X.join(y)

    fc_parameters = settings.from_columns(relevant_features)

    prediction_data = extract_features(
        X, kind_to_fc_parameters=fc_parameters, column_id=id, column_sort=timesteps
    )

    prediction_data.columns = prediction_data.columns.str.replace('["]', "")


    return prediction_data



def make_prediction(df, model_uri, tracking_uri=REMOTE_TRACKING_URI,  id="exp_unique_id", timesteps="timesteps"):

    loaded_model, _, _, _ = get_model_and_features(model_uri, tracking_uri=REMOTE_TRACKING_URI)

    prediction_data = get_prediction_features(df, model_uri, tracking_uri,  id, timesteps)

    prediction = loaded_model.predict(prediction_data)

    return prediction

