from modules.ncbi import esearch

print(esearch(database='pubmed',term='asthma',use_history=True,retmax=3).text)