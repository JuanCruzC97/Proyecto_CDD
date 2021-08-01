# Paquetes usados:
import requests
from scrapy import Selector
import pandas as pd
import numpy as np
import time


# Se crea una lista "urls" con las páginas a scrapear.
def listarURL(inicio, fin):
    urls = [0] * (fin - inicio + 1)
    for i, page in enumerate(range(inicio,fin + 1)):
        url = 'https://www.phishtank.com/phish_search.php?page='+str(page)+'&valid=n&Search=Search'
        urls[i] = url

    print('Listado de URLs a scrapear')
    print(urls)

    return urls


def scrapearPrincipal(urls, inicio, fin, sleep_mu = 1, sleep_sd = 0.5):

    # Este diccionario tendrá los dataframes generados en cada URL scrapeado.
    dict_df = {}

    # Para cada url en la lista de urls se genera un Selector List con la información del html.
    for n, url in enumerate(urls):

        inicio_page = time.time()

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

        df = pd.DataFrame(np.zeros((20,5)), columns=['ID', 'URL', 'Completo', 'Valid', 'Online'])

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
            inicio_row = time.time()

            # Analizamos la información de un elemento particular.
            # El td[1] tiene info del id.
            iden = selector_list[i].xpath('./td[1]/a/text()').extract()[0]
            # Obtengo el link del sitio en cuestión.
            url = selector_list[i].xpath('./td[2]/text()').extract()[0]
            completo = int(1)
            # En caso de que el link obtenido termine en '...' debemos acceder al url_esp (o usando el id) para obtenerlo completo.
            if url[-3:] == '...':
                # Hacemos el request usando el id.

                url = scrapearParticular(iden, sleep_mu, sleep_sd)
                completo = int(0)     
            
            valid = selector_list[i].xpath('./td[4]/strong/text()').extract()[0]
            online = selector_list[i].xpath('./td[5]/text()').extract()[0]

            df.iloc[i-1] = [iden, url, completo, valid, online]

            fin_row = time.time()
            print(f'Página número {inicio + n} fila número {i} scrapeada - tiempo {round(fin_row - inicio_row,5)} segundos.')

        fin_page = time.time()
        print(f'Página número {inicio + n} scrapeada')
        print(f'Tiempo transcurrido {round(fin_page - inicio_page,5)} segundos')
        print('----------------------------------------')

        dict_df['df_'+str(n)] = df
        
        pausa = np.random.normal(sleep_mu * k, 2)
        if pausa < 0:
            pausa = 4
        time.sleep(pausa)
        
        print(f'Tiempo en pausa {pausa} segundos.')
        print('----------------------------------------')
        
    df_total = pd.concat(dict_df.values()).reset_index(drop = True)
    df_total.index = np.arange((inicio-1)*20 + 1, fin * 20 + 1)
    df_total

    return df_total


def scrapearParticular(identificador, sleep_mu = 1, sleep_sd = 0.5):
    cookies = {
        'PHPSESSID': 'ar40cv5km3vtbe5s0qk3pkr2so0g6hbn',
        'cf_clearance': '3cbfd7809556f0cc6e51182e0536dfda54ff67a7-1627699354-0-250',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.phishtank.com/phish_search.php?page=9&valid=n&Search=Search',
        'Alt-Used': 'www.phishtank.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

    params = (
        ('phish_id', identificador),
    )

    sleep_sec = np.random.normal(sleep_mu, sleep_sd)
    time.sleep(sleep_sec)
    
    response = requests.get('https://www.phishtank.com/phish_detail.php', headers=headers, params=params, cookies=cookies)

    html_particular = response.content
    selector_particular = Selector(text = html_particular)
    selector_particular_list = selector_particular.xpath('//div[@class="padded"]/div[3]/span/b/text()')
                
    url_particular = selector_particular_list.extract()[0]

    return url_particular
    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.get('https://www.phishtank.com/phish_detail.php?phish_id=7096325', headers=headers, cookies=cookies)




# inicio y fin indican la cantidad de páginas de Phish Search a scrapear.
inicio = 10
fin = 11

urls = listarURL(inicio, fin)

df_completo = scrapearPrincipal(urls, inicio, fin, sleep_mu= 1.5, sleep_sd = 0.5, k = 10)

df_completo.to_csv(f'Dataset_Phishing_{inicio}a{fin}.csv')
