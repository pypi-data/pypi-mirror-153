import pandas as pd
import pickle
import json
import numpy as np
from os.path import dirname
import sys, os

sys.path.append(f"{os.path.abspath('')}/../libs/dreem")

sys.path.append(f"{os.path.abspath('')}/libs/dreem")
from dreem_nap import utils, database
from dreem.bit_vector import MutationHistogram

strList = list[str]

def json_dump(df:pd.DataFrame, json_file:str, verbose:bool=True)->None:
    """A simple function to dump a Pandas dataframe into a (tube, construct)-wise indexed json file.
    
    Args:
        df: the Pandas dataframe that you want to dump into a json.
        json_file: a string containing the relative path + name of the json to dump.
        verbose: print relevant information

    Returns:
        None
    """
    if verbose: print(f"Dumping df as a dict to a JSON file {json_file}")
    with open(json_file, 'w') as outfile:
        this_dict = df.set_index(['tube', 'construct']).groupby(level=0)\
            .apply(lambda d: d.reset_index().set_index('construct').to_dict(orient='index')).to_dict()
        json.dump(this_dict , outfile)
    if verbose: print("Done!")


def json_load(json_file:str, verbose:bool = True)->pd.DataFrame:
    """A simple function to load data from a (tube, construct)-wise indexed json file.
    
    Args:
        json_file: a string containing the relative path + name of the json to load.
        verbose: print relevant information

    Returns:
        Loaded Pandas dataframe.
    """
    if verbose: print("Load from dict-type JSON file")
    with open(json_file) as file:
        dictionary = json.load(file)
    # dictionary = pd.DataFrame.from_dict(my_json, orient='columns')
        df = pd.DataFrame.from_dict({(i,j): dictionary[i][j] 
                                for i in dictionary.keys() 
                                for j in dictionary[i].keys()},
                            orient='columns').transpose()\
                            .drop(columns='tube')\
                            .dropna()\
                            .reset_index()\
                            .rename({'level_0': 'tube', 'level_1': 'construct'}, axis=1)
    if verbose: print("Done!")
    return df


def mhs2dict(mhs:MutationHistogram, drop_attribute:strList)->dict:
    """Turns the output of Prof. Joe Yesselman's DREEM into a construct-wise index dictionary.

    Args:
        mhs: one tube's content under DREEM's MutationHistogram class format. 
        drop_attribute: a list of attributes from MutationHistogram class that you don't want into your dictionary
    
    Returns:
        A dictionary form of the MutationHistogram class.
    """
    tube_dict = {}
    for construct in mhs:
        tube_dict[construct] = mhs[construct].__dict__
        for attribute in drop_attribute:
            del tube_dict[construct][attribute]

        np_arrays = ['mut_bases', 'info_bases', 'del_bases', 'ins_bases',
                    'cov_bases']
        for array in np_arrays:
            tube_dict[construct][array] = tuple(tube_dict[construct][array])
        
        np_bases_arrays = ['A', 'C', 'G', 'T']
        for array in np_bases_arrays:
            tube_dict[construct]['mod_bases_'+array] = tuple(tube_dict[construct]['mod_bases'][array])
        del tube_dict[construct]['mod_bases']

        skips = ['low_mapq', 'short_read', 'too_many_muts']
        for sk in skips:
            tube_dict[construct]['skips_'+sk] = tube_dict[construct]['skips'][sk]
        del tube_dict[construct]['skips']
    return tube_dict


def push_tubes_to_firebase(pickles:dict, RNAstructureFile:str, min_bases_cov:int, folder:str, verbose:bool=True, print_end:str=' ')->None:
    """Pushes new tubes to Firebase.

    DREEM module outputs MutationHistogram objects, compressed under the pickle format. 
    For each pickle in pickles, this function turns it into dictionaries, filters out unvalid constructs and pushes the resulting (tube, construct)-wise indexed dictionary to the Firebase.
    The construct high-pass filter filters out a construct if which at least one base in its Region of Interest (ROI) doesn't reach `min_bases_cov` of base coverage.
    
    Args:
        pickles: a dictionary with names of the tubes and location of their pickle file: {'name of the tube': 'path to the file'}
        RNAstructureFile: string containing the name of a csv file with additional content. Its columns are: ['construct','roi_sequence','full_sequence','roi_start_index','roi_end_index','roi_deltaG','full_deltaG','roi_structure_comparison','full_structure','flank','sub-library']
        min_bases_cov: int type. Mutation rates of bases below this threshold will be considered irrelevant.
        firebase_folder: where to push the data in the firebase.
        verbose: print relevant information

    Returns:
        None
    """
    
    # Load additional content
    df_additional_content = pd.read_csv(RNAstructureFile)
    df_additional_content.construct = df_additional_content.construct.astype(int).astype(str)
    df_additional_content.full_sequence = df_additional_content.full_sequence.apply(lambda seq: seq.replace('U','T'))

    if verbose: print('Push pickles to firebase!')
    for count, tube in enumerate(pickles):
        # Load a tube from a pickle file
        mhs = pickle.load(open(pickles[tube], "rb"))

        df_tube = pd.DataFrame.from_dict(mhs2dict(mhs, drop_attribute = ['structure','_MutationHistogram__bases','sequence']),
                orient='index').rename(columns={'name':'construct'})

        # Merge with additional content (excel sheet content) and check the data sanity by sequences comparison
        df_temp = pd.merge(df_additional_content, df_tube, how='inner', on='construct').reset_index()
        #  assert not df_temp.apply(lambda row: not (str(row['full_sequence']).replace('U','T') in str(row['sequence'])) ,axis=1).sum(), "A sequence didn't match in the fusion"          
        df_temp = df_temp.drop(columns='index')

        # Count base coverage in the ROI and in the second half            
        df_temp['cov_bases_roi'] = df_temp.apply(lambda row: np.array(np.array(row['cov_bases'])[int(row['roi_start_index']):int(row['roi_end_index'])]).min(), axis=1)
        df_temp['cov_bases_sec_half'] = df_temp.apply(lambda row: np.array(np.array(row['cov_bases'])[int(len(row['cov_bases'])/2):]).min(), axis=1)

        # Filter out the constructs that don't reach 1000 reads for each base of the ROI 
        df_temp = df_temp[df_temp['cov_bases_roi'] >= min_bases_cov]
        df_temp['min_bases_cov'] = min_bases_cov

        df_temp = df_temp.astype(dtype={'construct':int, 'roi_sequence':str, 'full_sequence':str, 'roi_start_index':int,
        'roi_end_index':int, 'roi_structure_comparison':str, 'full_structure':str, 'data_type':str,
        'num_reads':int, 'num_aligned':int, 'num_of_mutations':object, 'mut_bases':object,
        'info_bases':object, 'del_bases':object, 'ins_bases':object, 'cov_bases':object, 'start':int, 'end':int,
        'mod_bases_A':object, 'mod_bases_C':object, 'mod_bases_G':object, 'mod_bases_T':object,
        'skips_low_mapq':int, 'skips_short_read':int, 'skips_too_many_muts':int,
        'cov_bases_roi':int, 'cov_bases_sec_half':int, 'sub-library':str, 'flank':str, 'min_bases_cov':int})

        df_temp = df_temp.set_index('construct')

        # Push this tube to firebase
        database.push(df_temp.to_dict(orient='index'), ref=tube, folder=folder, verbose= not bool(count))

        # Give yourself hope to wait by showing the progress
        print(tube, end=print_end)
    print('Done!')


def clean_dataset(df_database:pd.DataFrame, tubes:strList, verbose:bool = True)-> tuple[pd.DataFrame, pd.DataFrame]:
    """Process the content of the Firebase into Pandas dataframes.

    Args:
        df_database: the dataframe downloaded from the Firebase.
        tubes: the tubes that you will use. Under the form of a list, ex: ['A1','B3']).
        verbose: print relevant information

    Returns:
        A subset of df_database, in which every construct had a good-enough reading quality for each tube.
        The same content as df_database, with an additional 'tubes_covered' column, corresponding to the amount of tubes for containing this construct.
    """

    # Only keep desired pickle files
    df_full = df_database[df_database['tube'].isin(tubes)]

    # Check how many tubes reach 1000 reads on each base for a given construct
    df_full['tubes_covered'] = pd.Series(dtype=int)
    for construct in df_full.groupby('construct'):
        df_full['tubes_covered'].loc[construct[1].index] = construct[1]['full_sequence'].count()

    # Only keep constructs that reach 1000 reads in every tube    
    df = df_full[df_full['tubes_covered'] == len(tubes)].reset_index().drop(columns='index')

    number_of_void_dropped = (utils.get_construct_attribute(df, 'roi_deltaG' )=='void').apply(int).sum()
    if verbose: print(f"{number_of_void_dropped} constructs were dropped because deltaG was 'void'")
    df = df[df['roi_deltaG'] != 'void']

    df = df.astype(dtype={'tube': str, 'construct':int, 'roi_sequence':str, 'full_sequence':str, 'roi_start_index':int,
    'roi_end_index':int, 'roi_deltaG':float, 'full_deltaG':float,
    'roi_structure_comparison':str, 'full_structure':str, 'data_type':str,
    'num_reads':int, 'num_aligned':int, 'num_of_mutations':object, 'mut_bases':object,
    'info_bases':object, 'del_bases':object, 'ins_bases':object, 'cov_bases':object, 'start':int, 'end':int,
    'mod_bases_A':object, 'mod_bases_C':object, 'mod_bases_G':object, 'mod_bases_T':object,
    'skips_low_mapq':int, 'skips_short_read':int, 'skips_too_many_muts':int,
    'cov_bases_roi':int, 'cov_bases_sec_half':int, 'tubes_covered':int,
    'sub-library':str, 'flank':str})

    return df, df_full
