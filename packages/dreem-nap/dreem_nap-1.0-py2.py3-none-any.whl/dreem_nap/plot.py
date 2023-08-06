import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
from os.path import exists, dirname
import os, sys
from scipy.stats import linregress
from matplotlib.offsetbox import AnchoredText
sys.path.append(os.path.abspath(""))
from dreem_nap import utils

strList, intList = list[str], list[int]

def tube_coverage_distribution(df:pd.DataFrame)->None:
    """Plot each construct vs its number of tubes covered, i.e the number of tubes containing this construct.
    
    Args:
        df: dataframe of interest.
    """

    plt.figure()
    plt.plot(np.array(df.groupby['construct']['tubes_covered'].mean().sort_values(ascending=False)))
    plt.xlabel('Constructs (sorted)')
    plt.ylabel('Amount of tubes covered')
    plt.grid()


def valid_construct_per_tube(df:pd.DataFrame)->None:
    """Plot how many valid constructs each tube has.

    Args:
        df: dataframe of interest.
    
    Raises:
        If the min_bases_cov value isn't the same for every tubes.
    """
    
    df.groupby('tube').count().reset_index().plot(kind='bar',x='tube', y='construct')
    assert len(df.min_bases.cov.unique()) == 1, "min_bases_cov isn't unique"
    plt.ylabel(f"Number of construct above {int(df.min_bases_cov.unique())} reads")
    plt.grid()


def base_coverage_ROI_for_all_constructs(df:pd.DataFrame)->None:
    """Plot the base-coverage of the worst-covered base of the Region of Interest, for each construct. 
    
    Args:
        df: dataframe of interest.
    """
    plt.figure()
    plt.plot(np.array(df['cov_bases_roi'].sort_values(ascending=False).reset_index())[:,1])
    plt.plot(np.arange(0,int(df.construct.count()),1), [int(df.min_bases_cov.unique())]*int(df.construct.count()))
    plt.legend(['Dataframe', '1000 reads line'])
    plt.xlabel('Constructs (sorted)')
    plt.ylabel('# of reads of the worst covered base in the ROI for each (tube, construct)')


def random_9_base_coverage(df:pd.DataFrame)->None:
    """Plot the base coverage of 9 randomly picked (tube, construct).

    Args:
        df: dataframe of interest.
    """

    random_selection = np.random.randint(len(df), size=(9))
    fig = plt.figure(figsize=(75,75))
    for i in range(9):
        axes1 = plt.subplot(int('33'+str(i+1)), figsize=(25,25))
        plt.plot(np.array(df['cov_bases'].iloc[random_selection[i]]))
        start, end = df['roi_start_index'].iloc[random_selection[i]], df['roi_end_index'].iloc[random_selection[i]]
        plt.plot(np.arange(start, end, 1), np.array(df['cov_bases'].iloc[random_selection[i]])[start:end])
        plt.plot(np.arange(0, len(df['cov_bases'].iloc[random_selection[i]])), len(df['cov_bases'].iloc[random_selection[i]])*[int(df.min_bases_cov.unique())])
        plt.xlabel("Bases")
        plt.ylabel("Coverage")
        plt.title(f"Construct {df['construct'].iloc[random_selection[i]]}, tube {df['tube'].iloc[random_selection[i]]} ")
        plt.grid()
        plt.legend(["Base coverage (all)", 'Base coverage (ROI)', 'min_bases_cov'])
        axes2 = axes1.twinx()   
        axes2.set_ylabel('Coverage [%]')
        axes2.set_ylim((0,100*max(df['cov_bases'].iloc[random_selection[i]]))/df['num_reads'].iloc[random_selection[i]])
    fig.tight_layout()


def base_coverage(df:pd.DataFrame, tube:str, construct:int)->None:
    """Plot the base coverage of a specific (tube, construct).
    
    Args:
        df: dataframe of interest.
        tube: tube of interest.
        construct: construct of interest.   
    """

    ax1 = plt.subplot()
    serie = df.set_index(['tube','construct']).loc[tube, construct]
    plt.plot(np.array(serie['cov_bases']))
    start, end = serie['roi_start_index'], serie['roi_end_index']
    plt.plot(np.arange(start, end, 1), np.array(serie['cov_bases'])[start:end])
    plt.plot(np.arange(0, len(serie['cov_bases'])), len(serie['cov_bases'])*[int(df.min_bases_cov.unique())])
    plt.xlabel("Bases")
    plt.ylabel("Coverage")
    plt.title(f"Construct {construct}, tube {tube} ")
    plt.grid()
    plt.legend(["Base coverage (all)", 'Base coverage (ROI)', 'min_bases_cov'])
    ax2 = ax1.twinx()   
    ax2.set_ylabel('Coverage [%]')
    ax2.set_ylim(0,100*max(serie['cov_bases'])/serie['num_reads'])
    plt.tight_layout()


def heatmap(df:pd.DataFrame, column:str)->None:
    """Plot the heatmap of a specific column of your dataframe, w.r.t the tubes and constructs.

    Args:
        df: a Pandas dataframe.
        column: a specific column of your dataframe.    
    """

    base_cov_plot = df.pivot("tube","construct", column).astype(float)
    f, ax = plt.subplots()
    sns.heatmap(base_cov_plot, annot=False, linewidths=0, ax=ax, norm=LogNorm())


def mutation_rate(plot_type:str, df:pd.DataFrame, tube:str, construct:int)->None:
    """Plot the mutation rate of a specific (tube, construct).

    Args:
        plot_type: 'sequence' or 'partition'. 
            - 'sequence' uses bases numbers as index and the original construct bases as colors.
            - 'partition' uses original sequence bases as index and the partition of mutated bases as colors.
        df: dataframe of interest.
        tube: tube of interest.
        construct: construct of interest.
    """

    df_use = df.set_index(['tube','construct'])
    
    if not plot_type in ['sequence','partition']:
        raise f"{plot_type} must be 'sequence' or 'partition', please check this argument"

    if plot_type == 'sequence':  # Plot the mutation rate for each base along the sequence

        mut_per_base = pd.DataFrame({'mut_rate': pd.Series(np.array(df_use[f"mut_bases"].loc[tube, construct][1:])/np.array(df_use[f"info_bases"].loc[tube, construct][1:]), dtype=object)
                                    ,'base':list(df_use['full_sequence'].loc[tube, construct])})\
                                    .reset_index()\
                                    .set_index(['base', 'index'])

        df_hist = pd.DataFrame()
        df_hist.index = mut_per_base.reset_index()['index']

        for base in ['A','C','G','T']:
            df_hist[base] = pd.Series(dtype=float)
            df_hist[base] = mut_per_base.loc[base]

        df_hist.index = mut_per_base.reset_index()['base']

        ax = df_hist.plot.bar(stacked=True, figsize=(35,7), color=['r','b','y','g'])
        plt.title(f"tube {tube}, construct {construct}")

    if plot_type == 'partition': # Plot the partition of mutations for each base along the sequence
        df_hist = pd.DataFrame()
        for base in ['A','C','G','T']:
            df_hist[f"mod_bases_{base}"]  = np.array(df_use[f"mod_bases_{base}"].loc[tube, construct][1:])/df_use['info_bases'].loc[tube, construct][1:]

        df_hist.index = list(df_use['full_sequence'].loc[tube,construct])

        ax = df_hist.plot.bar(stacked=True, figsize=(35,7), color=['r','b','y','g'])


def deltaG(df:pd.DataFrame, tube:str)->None:
    """Plot the mutation rate of each paired-predicted base of the ROI for each construct of a tube, w.r.t the deltaG estimation.
    
    Args:
        df: dataframe of interest.
        tube: tube of interest.
    """

    fig = utils.define_figure(title=tube,
                            xlabel='deltaG [kcal]',
                            ylabel='Mutation ratio',
                            figsize=(20,5))

    stack_for_plot = {'0':{'x':[],'y':[]},'1':{'x':[],'y':[]}}

    for construct in df.construct.unique():
        roi_part = utils.get_roi_info(df=df, tube=tube, construct=construct)
        for base in ['A','C']:
            for roi_struct_comp in ['0','1']:
                try:    
                    this_base_mut =  roi_part.xs((base,True,roi_struct_comp), level=('base','paired','roi_structure_comparison'))
                    stack_for_plot[roi_struct_comp]['x'].extend(this_base_mut['roi_deltaG'].to_list())
                    stack_for_plot[roi_struct_comp]['y'].extend(this_base_mut['mut_rate'].to_list())
                except:
                    continue
    plt.plot(stack_for_plot['0']['x'],stack_for_plot['0']['y'],'b.')
    plt.plot(stack_for_plot['1']['x'],stack_for_plot['1']['y'],'r.')
    plt.legend(['A and C bases of the ROI, predicted paired by RNAstructure for both the ROI sequence and the full sequence',\
                'A and C bases of the ROI part, predicted paired by RNAstructure for the full sequence but not for the ROI sequence'])
    plt.ylim([0,0.15])
    fig.tight_layout()


def correlation_2_tubes(df:pd.DataFrame, tubes:tuple((str,str)), constructs:intList, axs:plt.axes=None)->pd.DataFrame:
    """Plot the mutation rate of each paired-predicted base of the ROI for a tube vs the same base in another tube, and this for specific constructs.

    Args:
        df: dataframe of interest.
        tubes: tubes of interest.
        constructs: constructs of interest.
        axs: a plt.axes object to use - for example for subplotting.
    
    Returns:
        A single-lined Pandas dataframe with values for r_value and slope.
    """

    if axs is None:
        fig, axs = plt.subplots(1,1)

    paired = {True: '.',False:'x'}
    roi_structure_comparison_color = {'0':'b','1':'r'}
    x_all, y_all = [], []
    for construct in constructs:
        for is_paired in paired: 
            utils.get_roi_info(df, tubes[1], construct)
            for roi in roi_structure_comparison_color:
                try:
                    x, y = np.array(utils.get_roi_info(df, tubes[1], construct)['mut_rate'].xs((is_paired,roi), level=('paired','roi_structure_comparison')), dtype=float),\
                            np.array(utils.get_roi_info(df, tubes[0], construct)['mut_rate'].xs((is_paired,roi),level=('paired','roi_structure_comparison')), dtype=float)
                    axs.plot(x,y,f"{roi_structure_comparison_color[roi]}{paired[is_paired]}")
                    axs.tick_params(axis='x', labelrotation = 45)
                    x_all.extend(x), y_all.extend(y)
                except:
                    axs.plot()
                    continue
    result = linregress(x_all,y_all)
    p =  np.poly1d((result.slope,result.intercept))
    t = np.linspace(min(x_all),max(x_all))
    axs.plot(t,p(t),'g-')
    axs.grid()
    axs.set(xlabel=f"Mutation rate of tube {tubes[1]}", ylabel=f"Mutation rate of tube {tubes[0]}")
    anchored_text = AnchoredText(f"R = {round(result.rvalue,3)}, slope = {round(result.slope,3)}", loc=2)
    axs.add_artist(anchored_text)
    df_corr = pd.DataFrame({'tube_0':tubes[0], 'tube_1':tubes[1], 'r_value':result.rvalue, 'slope':result.slope}, index=[0])
    return df_corr


def correlation_n_tubes(df:pd.DataFrame, tubes:strList, constructs:intList)->pd.DataFrame:  
    """Plot correlation_2_tubes() for each possible pair in the tubes list, and this for specific constructs, in a single plot.

    Args:
        df: dataframe of interest.
        tubes: tubes of interest.
        constructs: constructs of interest.

    Returns:
        A Pandas dataframe with values for r_value and slope for each possible pair in the tubes list.
    """

    df_global_corr = pd.DataFrame(columns=['tube_0', 'tube_1', 'r_value', 'slope'])
    plt.figure(figsize=(30*len(tubes), 30*len(tubes)))
    fig, axs = plt.subplots(len(tubes)+1,len(tubes), figsize= (30,30), sharex=True, sharey=True)
    for x in range(1,len(tubes)+1):
        for y in range(0,len(tubes)):
            df_global_corr = pd.concat((df_global_corr, correlation_2_tubes(df, (tubes[x-1], tubes[y]), constructs, axs[x][y])),
                                        axis = 0,
                                        join="outer",
                                        ignore_index=True)
    axs[0,len(tubes)-1].plot(0,0,'b.',0,0,'r.',0,0,'bx',0,0,'rx',0,0,'g-')            
    axs[0,len(tubes)-1].legend(['Paired in full sequence RNAstructure, paired in ROI RNAstructure',
                'Paired in full sequence RNAstructure, not paired in ROI RNAstructure',
                'Not paired in full sequence RNAstructure, not paired in ROI RNAstructure',
                'Not paired in full sequence RNAstructure, paired in ROI RNAstructure',
                'Fit'])
    return df_global_corr

def mut_rate_along_study(df:pd.DataFrame, tubes:list[str], study:dict):
    """Plot the mean of the mutation rate of the ROI bases, for each tube of the study.

    Args:
        df (pd.DataFrame): dataframe of interest.
        tubes (list[str]): tubes of interest.
        study (dict): a dictionnary with the following informations about the study:
            'name': what condition changes with the study.
            'values': how this condition changes along the tubes.
            'unit': unit used for this condition.
            
            ex:
                {'name':'60 mM DMS kinestics',
                'tubes':['D8', 'E8', 'F8', 'G8', 'H8', 'A9'],
                'unit':'min',
                'values':[1, 3, 9, 27, 81] }
    """
    paired, unpaired = np.zeros(len(tubes)), np.zeros(len(tubes))
    for count, tube in enumerate(tubes):
        for construct in df.construct.unique():
            df_roi = utils.get_roi_info(df, tube, construct)
            paired[count] += df_roi.xs(True, level= 'paired')['mut_rate'].mean()/len( df.construct.unique())
            unpaired[count] += df_roi.xs(False, level= 'paired')['mut_rate'].mean()/len( df.construct.unique())
    plt.plot(study['values'], paired, 'r.-')
    plt.plot(study['values'], unpaired, 'b.-')
    plt.xlabel(f"{study['name']} for each tube [{study['unit']}]")
    plt.ylabel('Mean mutation rate for the ROI')
    plt.legend(['Paired-predicted bases','Unpaired-predicted bases'])
