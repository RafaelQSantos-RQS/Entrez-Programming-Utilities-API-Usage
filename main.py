from modules.ncbi import esearch,efetch

#response_esearch = esearch(database='pubmed',term='cancer',reldate=60,datetype='edat',retmax=100, use_history=True).text
response_efetch = efetch(database='pubmed',id='38146690')
with open('teste.txt','wb') as file:
    file.write(response_efetch.content)