import os
import requests
import gc
from bs4 import BeautifulSoup
import sys
import subprocess
from sys import argv

# paths padrões
path_web_scraping = "datasets/step_1/"
path_url = 'https://commoncrawl.s3.amazonaws.com'
path_url_page_links_indexes = '/cc-index/collections/index.html'
file_pag_indexes_HTML = "page HTML de indexing.html"
file_pag_types = "types the file.html"

# aqui será pego todo o conteúdo da página HTML
# https://commoncrawl.s3.amazonaws.com/cc-index/collections/index.html
# para pegar toda a lista de indexações feitas até então
list_indexing = requests.get(path_url+path_url_page_links_indexes)
with open(path_web_scraping + file_pag_indexes_HTML,'w') as f:
    f.write(list_indexing.text)

# aqui é preciso acessar o arquivo "pagina HTML de indices.html" e colocar em uma lista todos os links
with open(path_web_scraping+file_pag_indexes_HTML,'r') as f:
    soup = BeautifulSoup(f,'lxml')

# cria uma lista somente com coutéudo das tags a
list_tags_a = soup.find_all('a')

# deve imprimir a 6ª em diante por que as anteriores tem lixo
print(list_tags_a[5])

# este metodo recebe um elemento da lista de conteúdos HTML
# ele filtra somente os links das URLs
def filter_url(element_list):
    start_link = element_list.find('a href=')
    if start_link == -1:
        return None, 0
    start_adress = element_list.find('"', start_link)
    end_adress = element_list.find('"',start_adress + 1)
    url = element_list[start_adress + 1 : end_adress]

    return url, end_adress

# este método chama o filter_url
def get_URL(element_list):
    url, end_adress = filter_url(element_list)
    return url

# cria uma lista somente com as URLs para acessar os indices
list_URL_acess_index_monthly = []
for element in list_tags_a:
    if 'gz' not in element:
        list_URL_acess_index_monthly.append(get_URL(str(element)))

# As primeiras 5 linhas não são de links e a linha 6 corresponde a um mês valido
count_indix = 5

# Atraves de cada linha do arquivo de indices de indexações vamos para uma pagina onde é possivel escolher
# o tipo de arquivo https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2018-17/index.html
# https://commoncrawl.s3.amazonaws.com/
if count_indix < len(list_URL_acess_index_monthly)-6:
    types_files = requests.get(path_url+list_URL_acess_index_monthly[count_indix])
    print(path_url+list_URL_acess_index_monthly[count_indix])

with open(path_web_scraping+file_pag_types,"w") as f_file_type:
    f_file_type.write(types_files.text)

gc.collect()
subprocess.call([sys.executable, 'step_2_download_fractions_indixing/manipulation_fractions_indexing.py'])
