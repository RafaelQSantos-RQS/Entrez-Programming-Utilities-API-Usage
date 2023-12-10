import requests
import re
import xml.dom.minidom as minidom
from html import unescape
from modules.utilities import Utilities

BASE_URL = Utilities.load_env(group='ncbi')['NCBI_API_BASE_URL']

class Ncbi:
    '''
    '''

    @staticmethod
    def basic_search(filename:str,database:str,query:str,use_history:str=None):
        '''
        Método para extração de dados 
        '''
        full_url = f"{BASE_URL}esearch.fcgi?db={database}&term={query}"
        use_history = True if use_history == 'y' else False
        full_url = full_url + "&usehistory=y" if use_history else full_url

        try:
            response = requests.get(url=full_url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise SystemExit(e)

        text = ''.join(line.strip() for line in response.text.splitlines())
        dom  = minidom.parseString(string=text)
        xml = dom.toprettyxml(indent="    ")
        xml_decodificado = unescape(xml)
        with open(filename,"w", encoding="utf-8") as file:
            file.write(xml_decodificado)

    @staticmethod
    def download_all_records(database:str,query:str,filename:str,use_history:str=None):
        '''
        Método para extração de dados 
        '''
        url_search = f'{BASE_URL}esearch.fcgi?db={database}&term={query}'
        use_history = True if use_history == 'y' else False
        url_search = url_search + "&usehistory=y" if use_history else url_search

        try:
            # Enviar a solicitação esearch
            response_esearch = requests.get(url_search)
            response_esearch.raise_for_status()  # Verifica se houve um erro na solicitação
            output = response_esearch.text

            # Parse WebEnv, QueryKey and Count (# records retrieved)
            match_web = re.search(r'<WebEnv>(\S+)<\/WebEnv>', output)
            web = match_web.group(1) if match_web else None
            match_key = re.search(r'<QueryKey>(\d+)<\/QueryKey>', output)
            key = match_key.group(1) if match_key else None
            match_count = re.search(r'<Count>(\d+)<\/Count>', output)
            count = match_count.group(1) if match_count else None

            print(f"web: {web} | Key: {key} | count: {count}")

            # Abrir o arquivo de saída para escrita
            try:
                with open(filename, 'w') as file:
                    # Recuperar os dados em lotes de 500
                    retmax = 500
                    for retstart in range(0, int(count), retmax):
                        # Montar a URL para efetch com rettype=xml
                        url_efetch = f'{BASE_URL}efetch.fcgi?db={database}&WebEnv={web}&query_key={key}'
                        url_efetch += f'&retstart={retstart}&retmax={retmax}&rettype=xml&retmode=text'
                        
                        # Enviar a solicitação efetch
                        response_efetch = requests.get(url_efetch)
                        response_efetch.raise_for_status()  # Verifica se houve um erro na solicitação
                        efetch_out = response_efetch.text
                        
                        # Escrever os resultados no arquivo
                        file.write(efetch_out)
            except IOError as e:
                print(f"Não foi possível abrir o arquivo! Error: {e}")
                raise

        except requests.exceptions.RequestException as e:
            print(f'Erro na solicitação: {e}')
            raise