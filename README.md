# Entrez Programming Utilities (API Usage)
Repository where it will house codes related to Entrez Programming Utilities in Python.

# Prerequisites

Before using this module, ensure you have the required dependencies installed. You can install them using:

```bash
pip install -r requirements.txt
```


# Modules
## Utilities

This module provides utility functions for common tasks, including creating directory structures and loading environment variables.

### Usage
#### Initialization

```python
import os
from modules.utilities import prepare_data_filesystem, load_env, datetimestamp
```
#### prepare_data_filesystem - Create Data Directory Structure

```python
# Create the directory structure for housing data
prepare_data_filesystem()
```

#### load_env - Load Environment Variables

```python
# Load environment variables for a specific group
env_vars = load_env(group='ncbi')
print(env_vars)
```

#### datetimestamp - Get Current Date and Time

```python
# Get the current date and time
timestamp = datetimestamp()
print(timestamp)
```

### Documentation

#### prepare_data_filesystem - Create Data Directory Structure

```python
def prepare_data_filesystem() -> NoReturn:
    """
    Method to create the directory structure for housing data.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
```

#### load_env - Load Environment Variables

```python
def load_env(group: Literal['ncbi', 'einfo', 'esearch', 'efetch']) -> dict:
    """
    Description
    -----------
    Load a set of environment variables from the .env file.

    Parameters
    ----------
    group: Name of the environment variables group to be loaded.

    Raises
    ------
    KeyError: If the group does not exist.

    Return
    ------
    A dictionary containing the loaded environment variables.
    """
```

#### datetimestamp - Get Current Date and Time

```python
def datetimestamp() -> str:
    """
    Returns the current date and time in the format 'dd/mm/yyyy - HH:MM:SS'.

    Parameters
    ----------
    None

    Returns
    -------
    str
        A string representing the current date and time.
    """
```

## NCBI

This module provides functions for interacting with the National Center for Biotechnology Information (NCBI) Entrez Programming Utilities (E-utilities) API. It includes functionalities for obtaining information about Entrez databases, performing searches, and retrieving records.

### Usage

#### Initialization

```python
import os
from modules.ncbi import einfo, esearch, efetch

# Set up NCBI API base URLs
BASE_URL = load_env(group='ncbi')['BASE_URL']
BASE_URL_EINFO = load_env(group='einfo')['BASE_URL']
BASE_URL_ESEARCH = load_env(group='esearch')['BASE_URL']
BASE_URL_EFETCH = load_env(group='efetch')['BASE_URL']
```

#### einfo - Retrieve Entrez Database Information

```python
# Get information about a specific Entrez database
response = einfo(entrez_database='pubmed', retmode='json')
print(response.json())
```

#### esearch - Perform Entrez Database Search

```python
# Perform a search in the PubMed database
response = esearch(database='pubmed', term='covid-19', retmax=10)
print(response.text)
```

#### efetch - Retrieve Records from Entrez Database

```python
# Retrieve records from the PubMed database using UIDs
response = efetch(database='pubmed', id=[123456, 789012], retmode='xml')
print(response.text)
```

### Documentation

#### einfo - Retrieve Entrez Database Information

```python
def einfo(entrez_database: str = None,
          retmode: Literal['xml', 'json'] = 'xml',
          save_in: str = None) -> Optional[requests.Response]:
    """
    Functions
    ---------
    - Provides a list of the names of all valid Entrez databases.
    - Provides statistics for a single database, including lists of indexing fields and available link names.

    Parameters
    -----------
    entrez_database: str or None
        The name of the Entrez database for which to retrieve statistics. If None, retrieves a list of all valid databases.
    retmode: str or None, optional
        The format of the returned data (default is 'xml'). Valid values: 'xml', 'json', etc.
    save_in: str or None, optional
        If specified, the response content will be saved to a file at the specified path.

    Returns
    -------
    bytes or None
        If save_in is None, returns the response. If save_in is specified, saves the content to the specified path and returns None.
    """
```

#### esearch - Perform Entrez Database Search

```python
def esearch(database: str,
            term: str,
            use_history: bool = False,
            WebEnv: str = None,
            query_key: int = None,
            retstart: int = None,
            retmax: int = 20,
            rettype: Literal['uilist', 'count'] = 'uilist',
            retmode: str = 'xml',
            sort: Literal['pub_date', 'Author', 'JournalName', 'relevance'] = None,
            field: str = None,
            idtype: str = None,
            datetype: str = None,
            reldate: int = None,
            mindate: str = None,
            maxdate: str = None) -> requests.Response | None:
    """
    Functions
    ---------
    - Provides a list of UIDs matching a text query.
    - Posts the results of a search on the History server.
    - Downloads all UIDs from a dataset stored on the History server.
    - Combines or limits UID datasets stored on the History server.
    - Sorts sets of UIDs.

    ...
    """
```

#### efetch - Retrieve Records from Entrez Database

```python
def efetch(database: str,
           id: list,
           query_key: int = None,
           WebEnv: str = None,
           retmode: str = None,
           rettype: str = None,
           retstart: int = None,
           retmax: int = None,
           strand: int = None,
           seq_start: int = None,
           seq_stop: int = None,
           save_in: int = None):
    """
    Functions
    ---------
    - Returns formatted data records for a list of input UIDs
    - Returns formatted data records for a set of UIDs stored on the Entrez History server

    ...
    """
```