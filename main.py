from modules.ncbi import esearch,efetch

#response_esearch = esearch(database='pubmed',term='zika+virus[title]',reldate=60,datetype='edat',retmax=100, use_history=True).text
#print(response_esearch)

#response_efetch = efetch(database='nuccore',id='38149274',rettype='gbc',retmode='xml')
#with open('data/raw/teste.xml','w') as file:
#    file.write(response_efetch.text)
