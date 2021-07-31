# Paquetes usados:
import requests
from scrapy import Selector
import pandas as pd
import numpy as np
import time


# inicio y fin indican la cantidad de páginas de Phish Search a scrapear.
inicio = 10
fin = 11
urls = [0] * (fin - inicio + 1)

# Se crea una lista "urls" con las páginas a scrapear.
for i, page in enumerate(range(inicio,fin + 1)):
    url = 'https://www.phishtank.com/phish_search.php?page='+str(page)+'&valid=n&Search=Search'
    urls[i] = url

print('Listado de URLs a scrapear')
print(urls)

# Este diccionario tendrá los dataframes generados en cada URL scrapeado.
dict_df = {}


# Para cada url en la lista de urls se genera un Selector List con la información del html.
for n, url in enumerate(urls):
    # Obtenemos el html de la url con un request.
    html = requests.get(url).content
    # Creamos el Selector de Scrapy para acceder a los datos del html.
    selector = Selector(text = html)
    # path directamente va a la parte de las tablas del html, donde está el listado de links.
    path = '//table[@class="data"]/tr'
    # Creamos la lista de selectores con los elementos de la tabla.
    # Tenemos 21 elementos, 20 links y uno en blanco que es el primero.
    selector_list = selector.xpath(path)
    print(len(selector_list))

    df = pd.DataFrame(np.zeros((20,6)), columns=['ID', 'URL_esp', 'URL', 'Completo', 'Valid', 'Online'])

    '''
    Se omite la posición 0 por no tener información.
    Para cada elemento del selector se obtiene la siguiente información.
    * td[1] tiene la información del id del link de phishing analizado. 
      También se puede obtener el url específico de dicho link (sirve para links que no aparecen completos.)
    * td[2] tiene el link sospechoso de phishing (si termina en '...' está incompleto)
    * td[4] tiene el valor si es 'VALID' o 'INVALID'. Deberían ser todos 'INVALID' que son los confirmados NO phishing.
    * td[5] tiene el valor si está 'online' y 'offline'.
    '''
    for i in range(1,len(selector_list)):
        # Analizamos la información de un elemento particular.
        # El td[1] tiene info del id.
        iden = selector_list[i].xpath('./td[1]/a/text()').extract()[0]
        # Si necesitamos el url específico.
        url_esp = selector_list[i].xpath('./td[1]/a/@href').extract()[0]
        # Obtengo el link del sitio en cuestión.
        url = selector_list[i].xpath('./td[2]/text()').extract()[0]
        completo = int(1)
        # En caso de que el link obtenido termine en '...' debemos acceder al url_esp (o usando el id) para obtenerlo completo.
        if url[-3:] == '...':
            # Hacemos el request usando el id.
            #html_particular = requests.get('https://www.phishtank.com/phish_detail.php?phish_id='+str(iden)).content

            url = "REQUEST"
            completo = int(0)     
        
        valid = selector_list[i].xpath('./td[4]/strong/text()').extract()[0]
        online = selector_list[i].xpath('./td[5]/text()').extract()[0]

        df.iloc[i-1] = [iden, url_esp, url, completo, valid, online]

    dict_df['df_'+str(n)] = df

df_total = pd.concat(dict_df.values()).reset_index(drop = True)

df_total.to_csv('df_total.csv')