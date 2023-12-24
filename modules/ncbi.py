import os
import re
import requests,logging,json
import xml.dom.minidom as minidom
from html import unescape
from modules.utilities import datetimestamp,load_env

BASE_URL = load_env(group='ncbi')['BASE_URL']
BASE_URL_EINFO = load_env(group='einfo')['BASE_URL']
BASE_URL_ESEARCH = load_env(group='esearch')['BASE_URL']
logging.basicConfig(level=logging.INFO,format=f'{datetimestamp()} (%(funcName)s) %(levelname)s: %(message)s')

def einfo(entrez_database:str=None,retmode:str='xml',save_in:str=None):
    '''
    Functions
    ---------
    - Provides a list of the names of all valid Entrez databases.
    - Provides statistics for a single database, including lists of indexing fields and available link names.

    Parameters
    -----------
    entrez_database: str or None
        The name of the Entrez database for which to retrieve statistics. If None, retrieves a list of all valid databases.
    retmode: str, optional
        The format of the returned data (default is 'xml'). Valid values: 'xml', 'json', etc.
    save_in: str or None, optional
        If specified, the response content will be saved to a file at the specified path.

    Returns
    -------
    bytes or None
        If save_in is None, returns the response. If save_in is specified, saves the content to the specified path and returns None.
    '''
    retmode = retmode.lower()
    possible_retmode = ['xml','json']

    if retmode not in possible_retmode:
        logging.error("This retmode isn't possible")
        return

    if save_in != None:
        if not (os.path.isdir(save_in) and os.access(save_in, os.W_OK)):
            logging.error(f'The specified path "{save_in}" is not a valid directory or does not have write permissions.')
            raise

    if entrez_database is None:
        url = f'{BASE_URL_EINFO}?retmode={retmode}'
    else:
        url = f'{BASE_URL_EINFO}/?db={entrez_database.lower()}&retmode={retmode}'
    
    try:

        response = requests.get(url=url)
        response.raise_for_status()
        logging.info("Resquest successfull!!")

        if save_in is not None:
            full_path = os.path.join(save_in,f'einfo.{retmode}')
            
            match(retmode):
                case 'json':
                    data = json.loads(response.content)
                    with open(full_path,'w+',encoding='utf-8') as file:
                        json.dump(data,file,ensure_ascii=False,indent=2)
                case 'xml':
                    with open(full_path,'w+') as file:
                        file.write(response.text)

            logging.info(f"The response was saved in {full_path}!!")
            return None
        else:
            return response

    except Exception as e:

        logging.error(f"An error occurred: {e}")
        return

def esearch(database:str,term:str,use_history:bool=False,WebEnv:str=None,query_key:str=None,retmax:int=20):
    '''
    Functions
    ---------
    - Provides a list of UIDs matching a text query.
    - Posts the results of a search on the History server.
    - Downloads all UIDs from a dataset stored on the History server.
    - Combines or limits UID datasets stored on the History server.
    - Sorts sets of UIDs.

    Required parameters
    -------------------
    database: str
        Database to search. 
        Value must be a valid Entrez database name (default = pubmed).
    term: str
        Entrez text query.
        All special characters must be URL encoded.
        Spaces may be replaced by '+' signs.
    
    Optional parameters - History Server
    ------------------------------------
    use_history: Bool, default False
        When use_history is True,  ESearch will post the UIDs 
        resulting from the search operation onto the History server 
        so that they can be used directly in a subsequent E-utility call.
        Also, usehistory must be set to True for ESearch to interpret 
        query key values included in term or to accept a WebEnv as input.
    Optional parameters - Retrievial
    --------------------------------
    retmax: int, default 20
        Total number of UIDs from the retrieved set to be shown in the XML output.
    rettype:
    '''
    list_of_valid_databases = dict(json.loads(einfo(retmode='json').content)).get('einforesult').get('dblist')
    logging.info("Checking if the database is valid")
    if database not in list_of_valid_databases:
        logging.error(f"The {database} is not a valid database!!")
        raise ValueError(f"The {database} is not a valid database!!")
    
    # Necessary url
    url = f'{BASE_URL_ESEARCH}?db={database.lower()}&term={term}'

    # Oprtional url
    if WebEnv != None:
        url += f'&WebEnv={WebEnv}'
    if query_key != None:
        url += f'&query_key={query_key}'
    if retmax != 20 and retmax <= 10000:
        url += f'&retmax={retmax}'
    if use_history:
        url += '&usehistory=y'
    
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        logging.info("Resquest successfull!!")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None