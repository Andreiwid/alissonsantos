
# Importando bibliotecas
import urllib3
import gc
import json
import mysql.connector
import os
import sys

#argumentos recebidos do arquivo manipulacao_frases_indexacao.py
received_parameters = sys.argv[:]

# assinaturas das plataformas de disponibilização de dados abertos
ckan_sig = '/api/action/site_read'
socrata_sig = '/api/catalog/v1'
arcgis_sig__odsoft_sig = '/api/v2'

path_step_2 = "datasets/step_2/"
path_step_3 = "datasets/step_3/"
path_index_fraction_uncompressed = '/indexing/indexing current uncompressed.txt'


lista_assinaturas = [ckan_sig, socrata_sig, arcgis_sig__odsoft_sig]

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="TCC"
    )


def saveUrlGov(url):
    mycursor = mydb.cursor()
    sql = "INSERT INTO url_gov_sigla(nome, fracao) VALUES (%s,%s)"
    val = (url,received_parameters[1],)
    mycursor.execute(sql, val)
    mydb.commit()


# essa parte é responsável por retornar cada da URL encontrada
def get_url(line):
    start_index_link = line.find("WARC-Target-URI")
    if start_index_link == -1:
        return None
    start_adress = line.find(":",start_index_link)
    end_adress = line.find("," , start_index_link + 1)
    url = line[start_adress + 1 : end_adress]
    return filter_url_GOV(url)

# aqui as URLs que tiverem o .GOV e sinônimos serão separadas
# É PRECISO MELHORAR ESSA PARTE POIS PARECE QUE SOMENTE OS .gov ESTÃO SENDO FILTRADOS
def filter_url_GOV(url):
    if '.gov' or '.de' or '.at' or '.be' or '.bg' or '.cy' or '.va' or '.hr' or '.dn' or '.sk' or '.si' or '.es' or '.ee' or '.fi' or '.fr' or '.el' or '.hu' or '.ie' or '.it' or '.lv' or '.lt' or '.lu' or '.mt' or '.nl' or '.pl' or '.pt' or '.uk' or '.cz' or '.ro' or '.se' or '.al' or 'ad' or '.am' or '.az' or '.by' or '.ba' or '.kz' or '.ge' or '.is' or '.li' or '.md' or '.mc' or '.me' or '.no' or '.ru' or '.sm' or '.ch' or '.rs' or '.tr' or '.ua' in url:
        return url
    else:
        return None

# Salva URLs que tenham .gov em um arquivo
with open(path_step_3 + 'URLs_.gov.txt', 'w') as out:
    with open(path_step_2 + path_index_fraction_uncompressed, 'r') as f:
        cole_set = set()
        for line in f:
            url = get_url(line)
            if url != None:
                cole_set.add(url.strip())
        for line in cole_set:
            out.write(line.replace('\"', ""))
            out.write('\n')

http = urllib3.PoolManager()
list_set_domi = set()
count = 0

# esse bloco de código verifica se há alguma sigla na lista de URLs que tenham .gov
with open(path_step_3 + "list_acronyms.txt", "r") as f_list_sigla:
    with open(path_step_3 + "URLs_.gov.txt", "r") as f_gov:
        for line_acronyms in f_list_sigla.readlines():
            for line_url in f_gov.readlines():
                if line_acronyms in line_url:
                    domi = line_url.find(".gov")
                    domain = line_url[:domi + 7]
                    list_set_domi.add(domain.strip())
                    print(domain.strip())

        for line in list_set_domi:
            print("\nElemento dentro da lista de dominios .GOV + sigla", line)
            count += 1
            saveUrlGov(line)

#os.path.isfile()
os.remove(path_step_2 + path_index_fraction_uncompressed)
gc.collect()
