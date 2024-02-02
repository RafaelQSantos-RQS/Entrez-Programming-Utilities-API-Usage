import os
from dotenv import load_dotenv
from datetime import datetime
from logging import error,info
from typing import Literal,NoReturn

def prepare_data_filesystem() -> NoReturn:
    '''
    Method to create the directory structure for housing data.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    # Define the list of paths to be created
    list_of_paths = ['data/raw', 'data/analysis', 'data/processed']

    # Iterate over each path
    for path in list_of_paths:
        try:
            os.makedirs(path)  # Create the directory
            info(f"Directory '{path}' created successfully!")  # Inform user about successful creation
        except FileExistsError:
            error(f"Directory '{path}' already exists.")  # Handle the case when the directory already exists
        except Exception as e:
            error(f"Error creating directory '{path}': {e}")  # Handle other errors


def load_env(group:Literal['ncbi', 'einfo', 'esearch', 'efetch']) -> dict:
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
    load_dotenv()

    env_vars = {
        'ncbi': {'BASE_URL': os.getenv('NCBI_API_BASE_URL')},
        'einfo': {'BASE_URL': os.getenv('EINFO_API_BASE_URL')},
        'esearch': {'BASE_URL': os.getenv('ESEARCH_API_BASE_URL')},
        'efetch': {'BASE_URL': os.getenv('EFETCH_API_BASE_URL')}
    }

    if group not in env_vars.keys():
         error(f"Invalid group: {group}. Allowed values: 'ncbi', 'einfo', 'esearch', 'efetch'")
         raise ValueError(f"Invalid group: {group}. Allowed values: 'ncbi', 'einfo', 'esearch', 'efetch'")   
     
    return env_vars.get(group, {})

def datetimestamp() -> str: # Defased, isn't more in use
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
    return datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
