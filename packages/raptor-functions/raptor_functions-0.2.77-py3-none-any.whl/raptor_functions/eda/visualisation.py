import matplotlib
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# 
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
# 
from sklearn.manifold import TSNE, Isomap, MDS
from sklearn.decomposition import PCA, KernelPCA
import umap


def plot_sensors(df, all = True, exps_numbers = [1,2,3], sensors_numbers = [1,2,3,4,5,6,7,8,9,10,11,12], overlap = False, figure_name = 'sensor_response', path = os.getcwd()):
    """
    Returns a figure with the visualisation of the sensor response, and saves it as a .pdf figure
    
    Plot: the time dependent profiles of the sensor response [mV] against the elapsed time [s] for a wide range of combination of experiments.

    Parameters
    ----------
    df: pandas dataframe
        Dataframe containing all the experiments and sensor mesaurements. See raptor_functions 'preprocessing' functions to generate this dataframe from the raw .txt files
        df = [exp_unique_id, exp_name, timesteps, sensor_1 ... sensor_n, Humidity (r.h.), measurement_stage, date_exp,time_elapsed, datetime_exp_start,datetime_exp, filename,result]
    exps_numbers: list of integers
        Selection list of the experiments to be plotted. The 'exp_numbers' are given by the 'exp_unique_id' of the pandas dataframe 'df'.
    sensor_numbers: list of integers
        Selection list of the sensors to be plotted. The 'sensors_numbers' are given by the columns of the pandas dataframe 'df' - usually containing 24 sensor columns.
    overlap: boolean
        If overlap = True -> the different experiments (for one single sensor) are plotted in the same axis. Better for comparison of the response between different experiments.
        If overlap = False -> different experiments are plotted in different columns. Better to look at individual responses.
        Default: False
    figure_name: str
        Name to give the figure to be saved as .pdf
    path: str
        Absolute path where the figure will be saved. If nothing provided, saved in the working directory.
    
    Returns
    -------
    figure
        Outputs a matplolib object figure.
    file
        Saves a .pdf in the path with the figure

    """
    # -----------------------------------------------------------
    # 
    n_total_sensors = len(list(filter(lambda k: 'sensor' in k, df.columns.tolist())))
    n_total_exps = df['exp_unique_id'].nunique()
    # 
    if all == True:
        sensors_numbers = list(np.linspace(1, n_total_sensors, n_total_sensors, dtype= int))
        exps_numbers = list(np.linspace(0, n_total_exps-1, n_total_exps, dtype=int))  
    # 
    # Pre-processing
    experiments = []
    n_exp = len(exps_numbers)
    for i in range(len(exps_numbers)):
        df_exp = df.loc[df['exp_unique_id'] == exps_numbers[i]]
        experiments.append(df_exp)
    # 
    sensors = []
    n_subplots_y = len(sensors_numbers)
    for i in range(len(sensors_numbers)):
        sensor_number = sensors_numbers[i]
        sensor = 'sensor_' + str(sensor_number)
        sensors.append(sensor)
    # 
    legend = True
    # 
    if overlap == False and len(exps_numbers) == 1:
        overlap = True
    # 
    if len(exps_numbers) == 1 and len(sensors_numbers)==1:
        # 
        fig, ax = plt.subplots(figsize=(6, 2), tight_layout=True)
        ax.plot(df_exp['time_elapsed'], df_exp[sensor])
        ax.set_xlabel(r'{Time [s]}')
        ax.set_ylabel(r'{Response [mV]}')
        ax.set_title('Experiment ' + str(exps_numbers[0]) + ': ' + str(sensors[0]))
        # 

    elif overlap == True:
        alpha_val = 1
        linewidth_val = 1
        if n_exp >3:
            print("Warning: adding line tansparency (alpha = 0.7) and thinner lines (0.5) for enhaced visualisation.")
            alpha_val = 0.7
            linewidth_val = 0.5
        # 
        fig, axs = plt.subplots(n_subplots_y,1,figsize=(6, 1.5*n_subplots_y),sharex=True,tight_layout=True)
        for i in range(n_subplots_y):
            try:
                if i == 0:
                    axs[i].set_title('Experiments ' + str(exps_numbers) + '\n' + str(sensors[i]))
                else:
                    axs[i].set_title(str(sensors[i]))
                # 
                for j in range(n_exp):
                    axs[i].plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]],label = str(exps_numbers[j]), alpha=alpha_val, linewidth = linewidth_val)
                    handles, labels = axs[i].get_legend_handles_labels()
                axs[i].set_ylabel(r'{Response [mV]}')
                if i == n_subplots_y -1:
                    axs[i].set_xlabel(r'{Time [s]}')
                    fig.legend(handles, labels, bbox_to_anchor=(1,0.5), loc="center left", borderaxespad=0)
            except: # Handling error when axis is 1D: axs[i]. -> axs.
                if i == 0:
                    axs.set_title('Experiments ' + str(exps_numbers) + '\n' + str(sensors[i]))
                else:
                    axs.set_title(str(sensors[i]))
                # 
                for j in range(n_exp):
                    axs.plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]],label = str(exps_numbers[j]), alpha=alpha_val, linewidth = linewidth_val)
                    handles, labels = axs.get_legend_handles_labels()
                axs.set_ylabel(r'{Response [mV]}')
                if i == n_subplots_y -1:
                    axs.set_xlabel(r'{Time [s]}')
                    fig.legend(handles, labels, bbox_to_anchor=(1,0.5), loc="center left", borderaxespad=0)
                
        # 
    else:
        n_subplots_x = n_exp
        fig, axs = plt.subplots(n_subplots_y, n_subplots_x,figsize=(6*n_subplots_x, 1.5*n_subplots_y),sharex=True,tight_layout=True)
        for j in range(n_subplots_x):
            for i in range(n_subplots_y):
                try:
                    if i == 0:
                        axs[i,j].set_title('Experiment ' + str(exps_numbers[j]) + '\n' + str(sensors[i]))
                    else:
                        axs[i,j].set_title(str(sensors[i]))
                    # 
                    axs[i,j].plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]])
                    axs[i,j].set_ylabel(r'{Response [mV]}')
                    if i == n_subplots_y -1:
                        axs[i,j].set_xlabel(r'{Time [s]}')
                except: # Above fails when n_sensors = 1 -> as the axs[i,j] become a 2d Array
                    if i == 0:
                        axs[j].set_title('Experiment ' + str(exps_numbers[j]) + '\n' + str(sensors[i]))
                    else:
                        axs[j].set_title(str(sensors[i]))
                    # 
                    axs[j].plot(experiments[j]['time_elapsed'], experiments[j][sensors[i]])
                    axs[j].set_ylabel(r'{Response [mV]}')
                    if i == n_subplots_y -1:
                        axs[j].set_xlabel(r'{Time [s]}')
        # 
    # -----------------------------------------------------------
    figure_name_full = figure_name + '.pdf'
    if path != os.getcwd():
        plt.savefig(path + "/" + figure_name_full, bbox_inches='tight')
        print('Plot saved sucesfully!')
    else: 
        plt.savefig(figure_name_full, bbox_inches='tight')
        print('Plot saved sucesfully!')

# 
# 
#


def PCA_plot(X,y,scaler = True, plt_3D = True, figure_name = 'pca_plot', path = os.getcwd()):
    # 
    if plt_3D == True:
        n_components = 3
    else:
        n_components = 2
    pca = PCA(n_components=n_components)
    if scaler == True:
        pipe = Pipeline([('scaler', StandardScaler()), ('pca', pca)])
        principalComponents = pipe.fit_transform(X)
    else: 
        principalComponents = pca.fit_transform(X)
    # 
    principalDf = pd.DataFrame(data = principalComponents)
    # 
    colors = {'Control':'green', 'Covid':'red'}
    # 
    # 
    if n_components == 2:
        fig, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
        ax = sns.scatterplot(x=principalDf.iloc[:,0], y=principalDf.iloc[:,1], hue=y, alpha=0.9, edgecolor='black')
    elif n_components == 3:
        # 
        fig = plt.figure(figsize=(6,6))    
        ax = Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)    
        cmap = ListedColormap(sns.color_palette("husl", 256).as_hex())
        sc = ax.scatter(principalDf.iloc[:,0],principalDf.iloc[:,1],principalDf.iloc[:,2], c=y.map(colors), cmap=cmap, alpha=0.9, edgecolors='black')
        ax.set_zlabel('Axis 3')
    else:
        print('Error: please only select 2 or 3 axis for the Principal Component Analysis.')
    ax.set_xlabel('Axis 1')
    ax.set_ylabel('Axis 2')
    ax.set_title('Principal Component Analysis (PCA)')
    # -----------------------------------------------------------
    # TODO: create new directory if path specified doesn't exists
    figure_name_full = figure_name + '.pdf'
    if path != os.getcwd():
        plt.savefig(path + "/" + figure_name_full, bbox_inches='tight')
        print('Plot saved sucesfully!')
    else: 
        plt.savefig(figure_name_full, bbox_inches='tight')
        print('Plot saved sucesfully!')


# 
# 
# 

def dimension_reduction_plot(X,y,scaler = True, plt_3D = True, single_plot = True, figure_name = 'dr_plot', path = os.getcwd()):
    # 
    if plt_3D == True:
        n_components = 3
    else:
        n_components = 2
    # Methods
    import umap
    pca = PCA(n_components=n_components)
    mds = MDS(n_components=n_components)
    umap = umap.UMAP(n_components=n_components)
    tsne = TSNE(n_components=n_components)
    isomap = Isomap(n_components=n_components)
    kernelpca = KernelPCA(n_components=n_components)
    # 
    if scaler == True:
        scaled_X = StandardScaler().fit_transform(X)
        # 
        pc_pca = pca.fit_transform(scaled_X)
        pc_mds = mds.fit_transform(scaled_X)
        pc_umap = umap.fit_transform(scaled_X)
        pc_tsne = tsne.fit_transform(scaled_X)
        pc_isomap = isomap.fit_transform(scaled_X)
        pc_kernelpca = kernelpca.fit_transform(scaled_X)
    else: 
        pc_pca = pca.fit_transform(X)
        pc_mds = mds.fit_transform(X)
        pc_umap = umap.fit_transform(X)
        pc_tsne = tsne.fit_transform(X)
        pc_isomap = isomap.fit_transform(X)
        pc_kernelpca = kernelpca.fit_transform(X)
    # 
    df_pc_pca = pd.DataFrame(data = pc_pca)
    df_pc_mds = pd.DataFrame(data = pc_mds)
    df_pc_umap = pd.DataFrame(data = pc_umap)
    df_pc_tsne = pd.DataFrame(data = pc_tsne)
    df_pc_isomap = pd.DataFrame(data = pc_isomap)
    df_pc_kernelpca = pd.DataFrame(data = pc_kernelpca)
    # 
    df_pc_list = [df_pc_pca, df_pc_mds, df_pc_umap, df_pc_tsne, df_pc_isomap, df_pc_kernelpca]
    df_pc_name_list = ['PCA', 'MDS', 'UMAP', 't-SNE', 'isoMap', 'Kernel PCA']
    n_subplots = len(df_pc_list)
    # 
    colors = {'Control':'green', 'Covid':'red'}
    # 
    # 
    if n_components == 2:
        if single_plot == True:
            fig, ax = plt.subplots(n_subplots,1,figsize=(6, 5*n_subplots),tight_layout=True)
            for i in range(n_subplots):
                df_pc_temp = df_pc_list[i]
                df_pc_name_list_temp = df_pc_name_list[i]
                sns.scatterplot(x=df_pc_temp.iloc[:,0], y=df_pc_temp.iloc[:,1], hue=y, alpha=0.9, edgecolor='black', ax=ax[i])
                ax[i].set_title(df_pc_name_list_temp)
            plt.show()
        else:
            for i in range(len(df_pc_list)):
                df_pc_temp = df_pc_list[i]
                df_pc_name_list_temp = df_pc_name_list[i]
                # 
                fig, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
                ax = sns.scatterplot(x=df_pc_temp.iloc[:,0], y=df_pc_temp.iloc[:,1], hue=y, alpha=0.9, edgecolor='black')
                ax.set_xlabel('Axis 1')
                ax.set_ylabel('Axis 2')
                ax.set_title('Dimensional Reduction: ' + df_pc_name_list_temp)
                # -----------------------------------------------------------
                # TODO: create new directory if path specified doesn't exists
                figure_name_full = figure_name + '_' + str(df_pc_name_list_temp) + '.pdf'
                if path != os.getcwd():
                    plt.savefig(path + "/" + figure_name_full, bbox_inches='tight')
                    print('Plot saved sucesfully!')
                else: 
                    plt.savefig(figure_name_full, bbox_inches='tight')
                    print('Plot saved sucesfully in current path!')
                plt.show()
    elif n_components == 3:
        if single_plot == True:
            fig, ax = plt.subplots(figsize=(6, 5*n_subplots),tight_layout=True)
            plt.axis('off')
            for i in range(n_subplots):
                df_pc_temp = df_pc_list[i]
                df_pc_name_list_temp = df_pc_name_list[i]
                # 
                ax = fig.add_subplot(n_subplots, 1, i+1,projection='3d')
                cmap = ListedColormap(sns.color_palette("husl", 256).as_hex())
                ax.scatter(df_pc_temp.iloc[:,0],df_pc_temp.iloc[:,1],df_pc_temp.iloc[:,2], c=y.map(colors), cmap=cmap, alpha=0.9, edgecolors='black')
                ax.set_zlabel('Axis 3')
                ax.set_xlabel('Axis 1')
                ax.set_ylabel('Axis 2')
                ax.set_title(df_pc_name_list_temp)
            # -----------------------------------------------------------
            # TODO: create new directory if path specified doesn't exists
            figure_name_full = figure_name + '.pdf'
            if path != os.getcwd():
                plt.savefig(path + "/" + figure_name_full, bbox_inches='tight')
                print('Plot saved sucesfully!')
            else: 
                plt.savefig(figure_name_full, bbox_inches='tight')
                print('Plot saved sucesfully in current path!')
            plt.show()

        else:   
            for i in range(len(df_pc_list)):
                df_pc_temp = df_pc_list[i]
                df_pc_name_list_temp = df_pc_name_list[i]
                # 
                fig = plt.figure(figsize=(6,6))    
                ax = Axes3D(fig, auto_add_to_figure=False)
                fig.add_axes(ax)    
                cmap = ListedColormap(sns.color_palette("husl", 256).as_hex())
                sc = ax.scatter(df_pc_temp.iloc[:,0],df_pc_temp.iloc[:,1],df_pc_temp.iloc[:,2], c=y.map(colors), cmap=cmap, alpha=0.9, edgecolors='black')
                ax.set_zlabel('Axis 3')
                ax.set_xlabel('Axis 1')
                ax.set_ylabel('Axis 2')
                ax.set_title('Dimensional Reduction: ' + df_pc_name_list_temp)
                # -----------------------------------------------------------
                # TODO: create new directory if path specified doesn't exists
                figure_name_full = figure_name + '_' + str(df_pc_name_list_temp) + '.pdf'
                if path != os.getcwd():
                    plt.savefig(path + "/" + figure_name_full, bbox_inches='tight')
                    print('Plot saved sucesfully!')
                else: 
                    plt.savefig(figure_name_full, bbox_inches='tight')
                    print('Plot saved sucesfully in current path!')
                plt.show()
    else:
        print('Error: please only select 2 or 3 axis for the Principal Component Analysis.')