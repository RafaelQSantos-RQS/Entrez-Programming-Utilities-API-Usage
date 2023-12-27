import os
import requests,logging,json
from modules.utilities import datetimestamp,load_env

BASE_URL = load_env(group='ncbi')['BASE_URL']
BASE_URL_EINFO = load_env(group='einfo')['BASE_URL']
BASE_URL_ESEARCH = load_env(group='esearch')['BASE_URL']
BASE_URL_EFETCH = load_env(group='efetch')['BASE_URL']
logging.basicConfig(level=logging.INFO,format=f'{datetimestamp()} (%(funcName)s) %(levelname)s: %(message)s')

def einfo(entrez_database:str=None,
          retmode:str='xml',
          save_in:str=None):
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

def esearch(database:str,
            term:str,
            use_history:bool=False,
            WebEnv:str=None,
            query_key:int=None,
            retstart:int=None,
            retmax:int=20,
            rettype:str='uilist',
            retmode:str='xml',
            sort:str=None,
            field:str=None,
            idtype:str=None,
            datetype:str=None,
            reldate:int=None,
            mindate:str=None,
            maxdate:str=None):
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

    WebEnv: str, default None
        Web environment string returned from a previous ESearch, EPost or ELink call.

    query_key: int, default None
        Integer query key returned by a previous ESearch, EPost or ELink call.

    Optional parameters - Retrievial
    --------------------------------
    retstart: int, default None
        Sequential index of the first UID in the retrieved set to be shown in the XML output.
    retmax: int, default 20
        Total number of UIDs from the retrieved set to be shown in the XML output.
    rettype: str, default uilist
        There are two allowed values for ESearch: 'uilist' (default), 
        which displays the standard XML output, and 'count', which displays only the <Count> tag.
    retmode: str, default xml
        Determines the format of the returned output. 
        The default value is xml for ESearch XML, but json is also supported to return output in JSON format.
    sort: str, default relevance
        Specifies the method used to sort UIDs in the ESearch output.
        The available values vary by database (db) and may be found in the Display Settings menu on an Entrez search results page.
        Values of sort for PubMed are as follows:
            - pub_date – descending sort by publication date
            - Author – ascending sort by first author
            - JournalName – ascending sort by journal name
            - relevance – default sort order, (“Best Match”) on web PubMed
    field: str, default None
        Search field. If used, the entire search term will be limited to the specified Entrez field.
        You can use this method or use in term, the following two URLs are equivalent:
            - &term=asthma&field=title
            - &term=asthma[title]
    idtype: str, default None
        Specifies the type of identifier to return for sequence databases (nuccore, popset, protein). 
        By default, ESearch returns GI numbers in its output. 
        If idtype is set to acc, ESearch will return accession.version identifiers rather than GI numbers.
    Optional parameters - Dates
    ---------------------------
    datetype: str, default None
        Type of date used to limit a search.
        The allowed values vary between Entrez databases, but common values are:
            - 'mdat' (modification date).
            - 'pdat' (publication date).
            - 'edat' (Entrez date).
    reldate: str, default None
        When reldate is set to an integer n, 
        the search returns only those items that have a date specified by datetype within the last n days.
    mindate, maxdate: str, default None
        Date range used to limit a search result by the date specified by datetype.
        These two parameters (mindate, maxdate) must be used together to specify an arbitrary date range.
        The general date format is YYYY/MM/DD, and these variants are also allowed: YYYY, YYYY/MM.
    '''
    # Validations
    list_of_valid_databases = dict(json.loads(einfo(retmode='json').content)).get('einforesult').get('dblist')
    logging.info("Checking if the database is valid")
    if database not in list_of_valid_databases:
        msg = f"The {database} is not a valid database!!"
        logging.error(msg=msg)
        raise ValueError(msg=msg)
    
    
    # Necessary url
    url = f'{BASE_URL_ESEARCH}?db={database.lower()}&term={term}'

    # Oprtional url
    if WebEnv != None:
        url += f'&WebEnv={WebEnv}'
    if query_key != None:
        url += f'&query_key={query_key}'
    if retstart != None:
        url += f'&retstart={retstart}'
    if retmax != 20 and retmax <= 10000:
        url += f'&retmax={retmax}'
    if rettype != None:
        list_of_rettype = ['uilist','count']
        if rettype not in list_of_rettype:
            msg = f"The {rettype} is not a valid rettype!!"
            logging.error(msg=msg)
            raise ValueError(msg)
        url += f"&rettype={rettype}"
    if retmode != None:
        url += f"&retmode={retmode}"
    if sort != None:
        list_of_sort_methods = ['pub_date','Author','JournalName','relevance',None]
        if sort not in list_of_sort_methods:
            msg = f"The {sort} is not a valid sort method!!"
            logging.error(msg=msg)
            raise ValueError(msg)
        url += f"&sort={sort}"
    if field != None:
        url += f"&field={field}"
    if idtype != None:
        url += f"&idtype={idtype}"
    if datetype != None:
        logging.info("Checking if the datetype is valid")
        request_for_datetype = dict(json.loads(einfo(entrez_database='pubmed',retmode='json').content)).get("einforesult").get("dbinfo")[0].get("fieldlist")
        list_of_datetype = [dicionario.get("name").lower() for dicionario in request_for_datetype]
        if datetype != None and datetype not in list_of_datetype:
            msg = f"The {datetype} is not a valid datetype!!"
            logging.error(msg=msg)
            raise ValueError(msg)
        url += f"&datetype={datetype}"
    if reldate != None:
        url += f"&reldate={reldate}"
    if mindate != None:
        url += f"&mindate={mindate}"
    if maxdate != None:
        url += f"&maxdate={maxdate}"
    if use_history:
        url += '&usehistory=y'
    
    # Request
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        logging.info("Resquest successfull!!")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None
    
def efetch(database:str,
           id:str,
           query_key:int=None,
           WebEnv:str=None,
           retmode:str=None,
           rettype:str=None,
           retstart:int=None,
           retmax:int=None,
           strand:int=None,
           seq_start:int=None,
           seq_stop:int=None,
           save_in:int=None):
    '''
    Functions
    ---------
    - Returns formatted data records for a list of input UIDs
    - Returns formatted data records for a set of UIDs stored on the Entrez History server

    Required Parameters
    -------------------
    database: str
        Database from which to retrieve records. 
        The value must be a valid Entrez database name (default = pubmed).
    
    Required Parameter - Used only when input is from a UID list
    ------------------------------------------------------------
    id: str
        UID list. Either a single UID or a comma-delimited list of UIDs may be provided.
        All of the UIDs must be from the database specified by database.
        Max Id is 200.
    
    Required Parameters – Used only when input is from the Entrez History server
    ----------------------------------------------------------------------------
    query_key: int
        This integer specifies which of the UID lists attached to the given Web Environment will be used as input to EFetch.
        Query keys are obtained from the output of previous ESearch, EPost or ELInk calls.
        The query_key parameter must be used in conjunction with WebEnv.
    WebEnv: str
        This parameter specifies the Web Environment that contains the UID list to be provided as input to EFetch.
        Usually this WebEnv value is obtained from the output of a previous ESearch, EPost or ELink call. 
        he WebEnv parameter must be used in conjunction with query_key.
    
    Optional Parameters – Retrieval
    -------------------------------
    retmode: str
        This parameter specifies the data format of the records returned, such as plain text, HMTL or XML.
    rettype: str
        This parameter specifies the record view returned, such as Abstract or MEDLINE from PubMed, or GenPept or FASTA from protein.
    retstart: int
        Sequential index of the first record to be retrieved (default=0, corresponding to the first record of the entire set).
        This parameter can be used in conjunction with retmax to download an arbitrary subset of records from the input set.
    retmax: int
        Total number of records from the input set to be retrieved, up to a maximum of 10,000.

    Optional Parameters – Sequence Databases
    ----------------------------------------
    strand: int
        Strand of DNA to retrieve.
        Available values are "1" for the plus strand and "2" for the minus strand.
    seq_start: int
        First sequence base to retrieve. 
        The value should be the integer coordinate of the first desired base, with "1" representing the first base of the seqence.
    seq_stop: int
        Last sequence base to retrieve. 
        The value should be the integer coordinate of the last desired base, with "1" representing the first base of the seqence.
    complexity: int
        Data content to return.
        Many sequence records are part of a larger data structure or "blob", and the complexity parameter determines how much of that blob to return.
        For example, an mRNA may be stored together with its protein product.
        The available values are as follows:\n
        0 - Entire blob\n
        1 - bioseq\n
        2 - minimal bioseq-set\n
        3 - minimal nuc-prot\n
        4 - minimal pub-set
    '''
    logging.info("Building the essencial url")
    url = f'{BASE_URL_EFETCH}?db={database}&id={id}'

    logging.info("Building a optional features")
    if query_key != None:
        url += f"&query_key={query_key}"
    if WebEnv != None:
        url +=f"&WebEnv={WebEnv}"
    if retmode != None:
        url += f"&retmode={retmode}"
    if rettype != None:
        url += f"&rettype={rettype}"
    if retstart != None:
        url += f"&retstart={retstart}"
    if retmax != None:
        url += f"&retmax={retmax}"
    if strand != None:
        url += f"&strand={strand}"
    if seq_start != None:
        url += f"&seq_start={seq_start}"
    if seq_stop != None:
        url += f"&seq_stop={seq_stop}"

    # Request
    logging.info("Trying request")
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        logging.info("Resquest successfull!!")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None