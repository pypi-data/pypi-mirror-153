import pandas as pd
import warnings


def get_data(data="validated_breath_data"):
    """Loads data into a dataframe

    Args:
        data (str, optional): name of data to be loaded. 
        examples of data include 'validated_breath_data', 'lab_data', 'repeat_experiment', 'handheld_data'.
        Defaults to 'validated_breath_data'.


    Returns:
        pandas dataframe: 
    """

    if data == "validated_breath_data":
        url = "https://drive.google.com/file/d/1CJ3e8NKS2KgUidZMLBFP0ktq2_y87eHb/view?usp=sharing"
        url = "https://drive.google.com/uc?id=" + url.split("/")[-2]

    elif data == "lab_data":
        url = "https://drive.google.com/file/d/1dz3vrsOLbqiedSIslxbioUhS82MB96WS/view?usp=sharing"
        url = "https://drive.google.com/uc?id=" + url.split("/")[-2]

    elif data == "repeat_experiment":
        url = "https://drive.google.com/file/d/1r83aSt_LJ-nGVLXohFKbk8oUlGwtJ4Gi/view?usp=sharing"
        url = "https://drive.google.com/uc?id=" + url.split("/")[-2]

    elif data == "handheld_data":
        url = "https://drive.google.com/file/d/1YZ6PDQpT9QkeVBLuRK6hThgaI54av6sf/view?usp=sharing"
        url = "https://drive.google.com/uc?id=" + url.split("/")[-2]

    else:

        return warnings.warn(
            "Warning...........Data not available. Available data include: \
        'validated_breath_data', 'lab_data', 'repeat_experiment', 'handheld_data'"
        )

    return pd.read_csv(url, index_col=0)
