import os
from dotenv import load_dotenv
from datetime import datetime

def prepare_data_filesystem():
    '''
    Método para criar a estrutura de arquivos que abrigará os dados.

    Parameters
    ----------
        None

    Retorn
    -------
        None
    '''
    list_of_paths = ['data/raw','data/analysis','data/processed']
    for path in list_of_paths:
        try:
            os.makedirs(path)
            print(f'Diretório {path} criado com sucesso!!')
        except FileExistsError as error:
            print(f"O diretório {path} já existe!!")
        except Exception as error:
            print(f"Erro ao criar o diretório {path}: ",error)


def load_env(group:str) -> dict:
    """
    Description
    -----------
    Carrega um conjunto de variáveis de ambiente do arquivo .env.

    Parameters
    ----------
        group: Nome do grupo de variáveis de ambiente a serem carregadas.

    Raises
    ------
        KeyError: Se o grupo não existir.

    Return
    ------
        Um dicionário contendo as variáveis de ambiente carregadas.
    """
    load_dotenv()

    env_vars = {
        'ncbi':{
            'BASE_URL':os.getenv('NCBI_API_BASE_URL')
        },
        'einfo':{
            'BASE_URL':os.getenv('EINFO_API_BASE_URL')
        },
        'esearch':{
            'BASE_URL':os.getenv('ESEARCH_API_BASE_URL')
        },
        'efetch':{
            'BASE_URL':os.getenv('EFETCH_API_BASE_URL')
        }
    }

    if group not in env_vars.keys():
        raise KeyError(f"O group '{group}' não existe.")
    
    return env_vars.get(group)

def datetimestamp():
    return datetime.now().strftime('%d/%m/%Y - %H:%M:%S')