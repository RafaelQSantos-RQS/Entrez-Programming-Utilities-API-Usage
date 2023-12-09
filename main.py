from modules.utilities import Utilities
from modules.ncbi import Ncbi

Utilities.prepare_data_filesystem()
Ncbi.basic_search(filename='data/raw/data.xml',database="pubmed",query='science[journal]+AND+breast+cancer+AND+2008[pdat]',use_history='y')
Ncbi.download_all_records(database='nucleotide',query='chimpanzee[orgn]+AND+biomol+mrna[prop]',filename='data/raw/chimp.xml')