from modules.utilities import prepare_data_filesystem
from logging import basicConfig,INFO
from modules.ncbi import esearch,efetch,einfo

basicConfig(level=INFO, format=f'%(asctime)s: %(message)s',datefmt='%d/%m/%Y %H:%M:%S')

def main():
    prepare_data_filesystem()

    einfo(entrez_database='nuccore',retmode='json',save_in='.')

    response_efetch = efetch(database='nuccore',id=['38149274'],rettype='gbc',retmode='text')
    with open('data/raw/teste.txt','w') as file:
        file.write(response_efetch.text)

if __name__ == "__main__":
    main()
