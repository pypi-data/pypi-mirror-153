# !pip install raptor_functions pandas_profiling
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport
import sweetviz as sv
# from raptor_functions.datasets import get_data














def eda_sv(df, compare=False):

    df['result'] = df['result'].map({'Control':0, 'Covid':1})



    if compare:
        covid = df[df['result']==1]
        control = df[df['result']==0]
        my_report = sv.compare([covid, "Covid"], [control, "Control"], 'result')
        my_report.show_notebook(w=None, h=None, scale=None, layout='widescreen', filepath=None)
    
    else:
        my_report = sv.analyze(df, target_feat='result', pairwise_analysis='off')
        my_report.show_notebook(w=None, h=None, scale=None, layout='widescreen', filepath=None)





def eda_pp(df):
    profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
    # profile.to_file("pandas_profiling_report.html")
    # profile.to_widgets()
    profile.to_notebook_iframe()

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
# #
# df = get_data()
# #
# from pandas_profiling import ProfileReport
# profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
# profile.to_file("pandas_profiling_report.html")



# import sweetviz as sv
# my_report = sv.analyze(df)
# my_report.show_html() # Default arguments will generate to "SWEETVIZ_REPORT.html"



# from autoviz.AutoViz_Class import AutoViz_Class
# AV = AutoViz_Class()

# import nltk
# nltk.download('wordnet')

# _ = AV.AutoViz('df.csv')




# import dtale
# import dtale.app as dtale_app
# # dtale_app.USE_COLAB = True
# dtale_app.USE_NGROK = True
# dtale.show(df)