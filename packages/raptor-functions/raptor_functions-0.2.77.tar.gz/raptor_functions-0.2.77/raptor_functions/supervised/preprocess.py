import pandas as pd
import os
import random
import numpy as np
import re
import warnings


SENSOR_FEATURES = [
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



def find_header_value(field, filename):
    """Finds the location of a keyword (exp_name, date, etc.) from the header of the .txt file

    Args:
        field (_type_): _description_
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """

    with open(filename) as f:
        for line_no, line in enumerate(f):
            if line.startswith(field):
                # Get the part of the string after the field name
                end_of_string = line[len(field) :]
                string = end_of_string[:-1]
                # break
                return string, line_no


def get_exp_stage(
    time, data_points_per_sec=4, baseline=2, absorb=7, pause=1, desorb=5, flush=23
):

    # data_points_per_sec: data point per second

    baseline_time = baseline * data_points_per_sec
    if time <= baseline_time:
        return "baseline"
    absorb_time = baseline_time + absorb * data_points_per_sec
    if time <= absorb_time:
        return "absorb"
    pause_time = absorb_time + pause * data_points_per_sec
    if time <= pause_time:
        return "pause"
    desorb_time = pause_time + desorb * data_points_per_sec
    if time <= desorb_time:
        return "desorb"
    flush_time = desorb_time + flush * data_points_per_sec
    if time <= flush_time:
        return "flush"
    wait_time = flush_time + flush * data_points_per_sec
    if time <= wait_time:
        return "wait"
    else:
        warnings.warn("Warning...........Can't process stage")
        return "nan"


def rename_columns(df):

    for col in df.columns:
        if "Sen" in col:
            new_col = re.findall("\d+", col)[0]
            df.rename(columns={col: f"sensor_{new_col}"}, inplace=True)
    df.rename(columns={"Data Points": "timesteps", "Humidity (%r.h.)":"humidity"}, inplace=True)
    # df.columns = df.columns.str.replace(r"[( r.h. %)]", "")

    return df


def get_label(f):

    filename = f.split("/")[-1]
    exp_name, _ = find_header_value("Name of the experiment =", f)

    if (
        ("Neg" in filename)
        or ("Control" in filename)
        or ("CONTROL" in filename)
        or ("Neg" in exp_name)
        or ("Control" in exp_name)
        or ("CONTROL" in exp_name)
        or ("Neg" in filename)
    ):
        return "Control"
    elif (
        ("Pos" in filename)
        or ("Covid" in filename)
        or ("COVID" in filename)
        or ("Pos" in exp_name)
        or ("Covid" in exp_name)
        or ("COVID" in exp_name)
        or ("Pos" in filename)
    ):
        return "Covid"
    else:
        warnings.warn("Warning...........Can't get label")
        return "Other"


def get_data_points_per_sec(f):
    global data_points_per_sec
    field = "Acquired data point per second = "
    data_points_per_sec = float(find_header_value(field, f)[0])
    return data_points_per_sec


def get_exp_stage_duration(f):

    # global baseline, absorb, pause, desorb, flush

    baseline = float(find_header_value("Base", f)[0][-4:])
    absorb = float(find_header_value("Absorb = ", f)[0])
    pause = float(find_header_value("Pause = ", f)[0])
    desorb = float(find_header_value("Desorb = ", f)[0])
    flush = float(find_header_value("Flush = ", f)[0])

    return baseline, absorb, pause, desorb, flush


def offset_one_sample(df_temp, baseline, data_points_per_sec):

    datapoints = int(baseline * data_points_per_sec)
    avg_baseline = df_temp[SENSOR_FEATURES].iloc[:datapoints].mean().values

    df_temp[SENSOR_FEATURES] = df_temp[SENSOR_FEATURES].apply(
        lambda row: row - avg_baseline, axis=1
    )

    return df_temp


def offset_batch_samples(df, id_col="exp_unique_id", baseline=2, data_points_per_sec=4):
    """normalises all sensors in each cycle of experiment by subtracting the average of the sensor voltage in the 1st 2 sec from sensor voltage in other periods 

    Args:
        df (pandas dataframe): dataframe of cyclic sensor data
        sec (int, optional): number of seconds to use for offsetting. Defaults to 2.
        id_col (str, optional): unique id of each cycle of experiment. Defaults to 'exp_unique_id'.

    Returns:
        pandas dataframe: _description_
    """
    samples = df.groupby(id_col)
    df_list = []
    for i, sample in samples:
        df_list.append(offset_one_sample(sample, baseline=baseline, data_points_per_sec=data_points_per_sec))
    return pd.concat(df_list)



def gradient_one_sample(df):
    df[SENSOR_FEATURES] = df[SENSOR_FEATURES].diff().fillna(df[SENSOR_FEATURES].diff().shift(-1))
    return df


def gradient_batch_samples(df, id_col="exp_unique_id"):
    """normalises all sensors in each cycle of experiment by subtracting the average of the sensor voltage in the 1st 2 sec from sensor voltage in other periods 

    Args:
        df (pandas dataframe): dataframe of cyclic sensor data
        sec (int, optional): number of seconds to use for offsetting. Defaults to 2.
        id_col (str, optional): unique id of each cycle of experiment. Defaults to 'exp_unique_id'.

    Returns:
        pandas dataframe: _description_
    """
    samples = df.groupby(id_col)
    df_list = []
    for i, sample in samples:
        df_list.append(gradient_one_sample(sample))
    return pd.concat(df_list)



def fillna_columns(df_temp):

    num = df_temp._get_numeric_data()
    num[num < 0] = np.nan
    num = num.fillna(num.mean())
    return df_temp


def preprocess_single_file(
    f,
    parse_time=True,
    parse_filename=True,
    rename_column=True,
    fillna=True,
    offset=False,
    has_label=True,
):
    """preprocess a single cycle (one txt file) of experiment

    Args:
        f (str): file path with txt extension
        rename_column (bool, optional): rename columns. Defaults to True.
        fillna (bool, optional): replaces extreme negative values with mean of column. Defaults to True.
        offset (bool, optional): normalises all sensors in each cycle of experiment by subtracting the average of the sensor voltage in the 1st 2 sec from sensor voltage in other periods . Defaults to True.
        has_label (bool, optional): extracts label and add to dataframe. Defaults to True.

    Returns:
        pandas dataframe: dataframe of features in a cycle(one txt file)
    """

    _, line_no = find_header_value("Data Points", f)

    df_temp = pd.read_csv(f, sep="\t", header=(line_no - 1))

    data_points_per_sec = get_data_points_per_sec(f)
    baseline, absorb, pause, desorb, flush = get_exp_stage_duration(f)

    df_temp['exp_unique_id'] = 0

    df_temp["measurement_stage"] = df_temp["Data Points"].apply(
        get_exp_stage,
        data_points_per_sec=data_points_per_sec,
        baseline=baseline,
        absorb=absorb,
        pause=pause,
        desorb=desorb,
        flush=flush,
    )

    if parse_time:
        date, _ = find_header_value("Date = ", f)
        df_temp["date_exp"], _ = find_header_value("Date = ", f)
        df_temp["time_elapsed"] = df_temp.index / 4
        time_start, _ = find_header_value("Time = ", f)
        time_elapsed = df_temp.index / 4
        df_temp["datetime_exp_start"] = time_start
        df_temp["datetime_exp"] = pd.to_datetime(
            date + " " + time_start
        ) + pd.to_timedelta(time_elapsed, unit="s")



    if parse_filename:
        df_temp["filename"] = f.split("/")[-1]



    df_temp["exp_name"] = find_header_value("Name of the experiment = ", f)[0][1:-1]

    if rename_column:
        df_temp = rename_columns(df_temp)

    if fillna:
        df_temp = fillna_columns(df_temp)

    if offset:
        df_temp = offset_batch_samples(df_temp, baseline=baseline, data_points_per_sec=data_points_per_sec)


    repeat_no = find_header_value("Repeat No. = ", f)[0].split("/")[0]
    df_temp["repeat_no"] = repeat_no

    if has_label:
        df_temp["result"] = get_label(f)
        df_temp = reorder_columns(df_temp)
        return df_temp

    df_temp = reorder_columns(df_temp)

    return df_temp


def get_all_files(parent_dir):
    all_files = []
    for path, subdirs, files in os.walk(parent_dir):
        for name in files:
            if (name.endswith("txt")) and (len(name) > 25) and ("Wash" not in name):
                all_files.append(os.path.join(path, name))
    return all_files


def get_single_repeat(df):
    """select one (chosen at random) of repeat experiemnts

    Args:
        df (pandas dataframe): dataframe of cyclic sensor data with repeat experiments

    Returns:
        pandas dataframe: dataframe with only one of each repeat experiemnt
    """

    g = df.groupby(["exp_name"])

    exp_names = list(set(df["exp_name"]))
    all = []
    for i in exp_names:
        df = g.get_group(i)

        uniq_files = list(df["filename"].unique())
        file_chosen = random.choice(uniq_files)
        df = df[df["filename"] == file_chosen]
        all.append(df)
    return pd.concat(all)


def reorder_columns(df):
    """reorders features with exp_unique_id as first column asnd result as last

    Args:
        df (pandas dataframe): _description_

    Returns:
        pandas dataframe: _description_
    """
    feature_len = len(df.columns)

    try:
        df.insert(feature_len-1, 'result', df.pop('result'))
        df.insert(0, 'exp_unique_id', df.pop('exp_unique_id'))
    except:
        pass



    # col_list = df.columns.tolist()
    # new_col_list = [col_list[-1]] + [col_list[-2]] + col_list[:-2]
    # df = df[new_col_list]

    return df


def preprocess_all_files(
    path_to_measurements,
    parse_time=True,
    parse_filename=True,
    rename_column=True,
    no_repeat=False,
    fillna=True,
    offset=False,
    has_label=True,
):
    """preprocess all cycle (all txt file) of experiment

    Args:
        path_to_measurements (str): folder path to measurements
        parse_time (bool, optional): extract time features. Defaults to True.
        parse_filename (bool, optional): adds filename to dataframe. Defaults to True.
        rename_column (bool, optional): rename columns. Defaults to True.
        no_repeat (bool, optional): _description_. Defaults to False.
        fillna (bool, optional): replaces extreme negative values with mean of column. Defaults to True.
        offset (bool, optional): normalises all sensors in each cycle of experiment by subtracting the average of the sensor voltage in the 1st 2 sec from sensor voltage in other periods . Defaults to True.
        has_label (bool, optional): extracts label and add to dataframe. Defaults to True.

    Returns:
        pandas dataframe: dataframe of features in a cycle(one txt file)
    """

    list_files = get_all_files(path_to_measurements)

    df_list = []
    for i, f in enumerate(list_files):

        df_temp = preprocess_single_file(
            f,
            parse_time=parse_time,
            parse_filename=parse_filename,
            offset=offset,
            fillna=fillna,
            has_label=has_label,
        )
        df_temp["exp_unique_id"] = i
        df_list.append(df_temp)

    df = pd.concat(df_list)
    df = reorder_columns(df)


    if no_repeat:
        return get_single_repeat(df)
    else:
        return df
