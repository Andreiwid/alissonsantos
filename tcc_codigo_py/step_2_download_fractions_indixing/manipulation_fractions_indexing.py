import os
import requests
import gc
from bs4 import BeautifulSoup
from bs4.element import Tag
import gzip
import shutil
from urllib.request import urlretrieve
import sys
import subprocess
from datetime import datetime
import mysql.connector

path_dataset_step_1 = "datasets/step_1"
path_dataset_step_2 = "datasets/step_2"
path_indexes_fractions_indexing = "/indexes_fractions_indexing/"
path_index_fraction_compacted = path_dataset_step_2+"/indexing/indexing current.gz"
path_index_fraction_uncompressed = path_dataset_step_2+"/indexing/indexing current uncompressed.txt"

path_url = 'https://commoncrawl.s3.amazonaws.com'

mydb = mysql.connector.connect(
        host="localhost",
        user="",
        passwd="",
        database="TCC"
    )

# este método serve para sempre retornar a ultima indexação gravada no banco
def get_last_insert_DB():
    last_insert = 0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT fracao FROM url_gov_sigla ORDER BY fracao DESC LIMIT 1")
    myresult = mycursor.fetchall()
    return myresult[0][0]

with open(path_dataset_step_1+"/types the file.html","r") as f_read_file_type:
    soup_file_type = BeautifulSoup(f_read_file_type,'html5lib')

# Usa-se uma URL semelhante a esta
# https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2018-17/wat.paths.gz
# para baixar o file .WAT, oque muda é o title, por isso vou pega-lo agora
title = soup_file_type.title.get_text()
start = title.find("(")
fim = title.find(")",title.find("(")+1)
name_indexing = title[start+1:fim]

file = requests.get(path_url+"/crawl-data/"+name_indexing+"/wat.paths.gz")

# Salva no diretório /datasets/indices de fracoes da indexacao/ o pacote
with open(path_dataset_step_2 + path_indexes_fractions_indexing +name_indexing+\
 ".wat.paths.gz","wb") as f_index_fraction:
    f_index_fraction.write(file.content)

# extrair files de pacotes
with gzip.open(path_dataset_step_2 + path_indexes_fractions_indexing \
          +name_indexing+".wat.paths.gz","rb") as f_read_bina:
    with open(path_dataset_step_2 + path_indexes_fractions_indexing \
          +name_indexing+".txt","wb") as f_write_bina:
        shutil.copyfileobj(f_read_bina, f_write_bina)
os.remove(path_dataset_step_2 + path_indexes_fractions_indexing \
          +name_indexing+".wat.paths.gz")

with open(path_dataset_step_2 + path_indexes_fractions_indexing \
          +name_indexing+".txt","r") as f_read_indice_fracao_txt:
    list_fractions = []
    for line in f_read_indice_fracao_txt.readlines():
        list_fractions.append(line)

# baixar o file compactado que descompactado tem mais de 60 mil linha que guarda os índices para localizar
# as frações da indexação

# aqui chamo o método que retorna a ultima indexação guardada no banco
index_fraction = get_last_insert_DB()

# aqui acrescento mais uma posição ao indice para que baixe a próxima indexação
index_fraction += 1

while index_fraction < len(list_fractions):
    print("\n*************************\n")
    print("Esta baixando a fração numero ", index_fraction, "de um total de {0}, \
    que corresponde a {1:8.2f} %".format(len(list_fractions), ((100 * index_fraction)/len(list_fractions))))
    print("\n*************************\n")

    try:
        urlretrieve(path_url + "/" + list_fractions[index_fraction], path_index_fraction_compacted)
        data_current = datetime.now()
        data_formated = data_current.strftime("%d/%m/%Y %H:%M:%S")
        print("\nA data e hora do erro é {}".format(data_formated))
    except ValueError:
        print("Oops!  Não foi possível baixar este file"+path_url + "/" + list_fractions[index_fraction], path_index_fraction_compacted)


    # descompactar o file com as frações da indexação que tem mais ou menos 1,3 Gigas de tamanho
    # e ápos descompactadas tem em média 6,5 GigaBites
    with open(path_index_fraction_uncompressed, 'wb') as f_write_ind_fra_descompac, \
            gzip.open(path_index_fraction_compacted, 'rb') as f_read_ind_fra_compac:
        shutil.copyfileobj(f_read_ind_fra_compac, f_write_ind_fra_descompac)

    # aqui esta faltando verificar o tamanho do file para só então remove-lo
    os.remove(path_index_fraction_compacted)

    gc.collect()
    # step_3_filter_URLs
    subprocess.call([sys.executable, 'step_3_filter_URLs/Filter_URLs.py', str(index_fraction)])
    index_fraction += 1
