import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from os.path import exists, dirname
import os, sys
sys.path.append(os.path.abspath(""))
from dreem_nap import *

strList = list[str]
def connect(verbose:bool = True)->None:
    """Initiate connection with the database.

    Args:
        verbose: print when connection was already set.
    """

    cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "dreem-542b7",
    "private_key_id": "510f9fa7da38e277c2e9673e6550426ae9183267",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCgExvQjKxHwVuw\nt1O6t8R4IoAdpl7CqcvtxuMw/jIfGvAnITpzJoB+O+AeIxwlSBO1bRCmoCq7T8Uj\nkJdzaYxo9fT/UTFWc3Uo3M2fmGY5YgVQpzHSIdWDD9r2bwgwkXS9bPxk41yYADsH\n1b62lN62akrbNp6MTB2Vib+qWJqX/F34BhEDxGa7g31yPSk8fc7NyEgHHoii14Xl\ncV9JZ0KsqiDr9PJKJ6Jl8zpr9R9X3mCYi50vJYcRUKCJ6bxtWN933lHhnq7rusuo\nIdOUA83RTXM7RoGAQALQm5cyBPiO9xMW20OBVOGN/kfWsIs9/GQerRtLGAnRN0t0\ns9WWnpdHAgMBAAECggEADu6pZhNxUMJDTOFVILJa1AAX5mwqI8uWF+i5Mc1MnKU1\nKNlLLAm3686nEfihfALUv9RcPMbtJYsD71TiI+SBMhtbjuOikBd2IukyD0S2qHyx\n1Tu7hIgedDrq6Jkj8O/orXD4vGqPLSi8WPdB8qNBgU+6Cuf18014ZwYyCHB6f1no\nH3IMzsKQL10p/2vfA5PmYDOOhWekLV34sqiPerPYnuyiWmclgM4L+smpTOo1k1h8\neK1t/uf0SZQgQvXraibgTVs38MDd2mAo/JSicmVU+5PK22zdMfptvia2cfx2HGP/\n8ZRd8pDJi20lUgNr1yI9kUNDBPp/umVK6XwUftJjAQKBgQDLl7ckNupKV2d2aCdo\nKUs6NQZHiV1nRA6lbLQU51lzDKVhtTGLM75EojiUTPmOq9AWQGeHm9iUmv7UaLtg\nDeCB11AAbKFAxyxwjxE0E1d/ii8kh2ZYTAUh64viU/5dWLX+ZT2g8P9r92xOYEle\nt1bMs953qpFRXYf9GpCBCe0rAQKBgQDJR6hr1aarmuNAXLAgnSgn2CNEZHSUi7sT\nkvaG/EOl7XnLq4fMV5uwA1n/r/5pufn9KaS3MnJlUpqqcBtlmnAzvi5pvtKmpHC8\nQfimE15smUkgfCb8l+LesWk1lM/kpSeAn0L/FqL26KLnApa/4VKhLIFI+sPen/y4\nHZZ3FEmqRwKBgHUnSGu+bfN5eD/aj1KQ8Ij+Gi7wDJ9vuj3W34ln10Es9b3T1j6T\n99jmwEgWQ0Sl+YfUZ77RHz/kMN9ppOkREy+kBpU37VKpShk7OlsNBjyN97K9d1c3\n53wtXsFONADjG1bYSy5hf5lRNzGilpW6Smhg2JNjw1texvIOZzjZzXABAoGAYK0w\ncgr+sPIGMQXT+vZBMVIZLmJptGehBXfTPWaxP2Ne2rqa0UVLHDGf6rWnpzSSpEx6\nNxvd4ljYvQB3yEdzmQbB2Dy1hSD6nRG60ln/Qn4lp5q6RxzU9U2VUQ0XBaVl4dud\nHFTNFXcLt5WAvs0FGTD9MAZySd3iTrS3bp6p+0UCgYBnwQ3JTz5SyNkR7WqYlVgK\n2OIeslo7hCqGnn7pyuggNDr/YrE/P8i3cly+6BJ0twJMVi+qg1WqOKiy5AQhHt+5\nXk68ZQu1911T/saO76lafCGqZkdGlsi7k1uv3lh8/SyqXcXKGy9L1KJKTI7YXfbK\nvV2Ga5Uce124cBoekQc9Dw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ejldl@dreem-542b7.iam.gserviceaccount.com",
    "client_id": "111801627848439891468",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ejldl%40dreem-542b7.iam.gserviceaccount.com"
    })
    # Initialize the app with a service account, granting admin privileges
    # As an admin, the app has access to read and write all data, regradless of Security Rules

    try:
        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL':'https://dreem-542b7-default-rtdb.firebaseio.com/'
            })
    except:
        if verbose: print('Re-used the previous Firebase connection')

def push(dict_df:pd.DataFrame, folder:str, ref:str, verbose:bool = True)->None:
    """Push a dictionary to the database, in a given folder, for a given reference.
    
    Args:
        dict_df: the dictionary you want to push
        folder: string, root folder in the database. Corresponds to a user, a version, a project, etc.
        ref: string, path to w
    """

    connect(verbose = verbose)
    ref_obj = db.reference(f"{folder}/{ref}")
    ref_obj.set(dict_df)


def load(folder:str, tubes:strList, verbose:bool = True)->pd.DataFrame:
    """Download a Pandas dataframe from the database.
    
    Args:
        folder: string, root folder in the database. Corresponds to a user, a version, a project, etc.
        tubes: list of the tubes that you want to use.
        verbose: print relevant information.
    
    Returns:
        Dataframe of the targeted tubes.
    """
    
    if verbose: print('Load data from database')
    connect()
    df = {}
    missed_tubes = []
    for tube in tubes:
        try:
            ref = db.reference(f"{folder}/{tube}")
            df[tube] = pd.DataFrame.from_dict(ref.get('/')[0], orient='index')
            if verbose: print(tube, end=' ')
        except:
            if verbose: print(f"\nTube {tube} not found on database")
            missed_tubes.append(tube)

    if missed_tubes != []:
        if verbose: print(f"Tubes {missed_tubes} couldn't be loaded from database")

    df = pd.concat(df)
    df = df.reset_index().rename(columns={'level_0':'tube', 'level_1':'construct'})
    if verbose: print('Done!')
    return df