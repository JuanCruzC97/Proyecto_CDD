import pandas as pd
import numpy as np
from urllib.parse import urlparse
import tldextract
import jellyfish
from joblib import load

class DetectarPhishing:

    def __init__(self):
        self.modelo = 0

        self.metric_domains = [
            'amazon', 
            'instagram', 
            'google', 
            'whatsapp',  
            'twitter',
            'facebook',
            'yahoo', 
            'wikipedia',
            'baidu',
            'paypal', 
            'mail', 
            'sfexpress' ,
            'onedrive',
            'excel', 
            'square', 
            'mail', 
            'office365', 
            'irs', 
            'tencent', 
            'creditagrecole s.a.',
            'microsoft',
            'blogspot',
            'onedrive',
            'payment',
            'hsbc',
            'secure',
            'help',
            'banco',
            'bank',
            'support',
            'rakuten',
            'steam',
            'olx']
    
        print('Instancia del detector fue creada')

    def obtenerMetricDomains(self):
        return self.metric_domains

    def prepararInput(self, data_urls):

        # Descomposición del URL.

        data_urls['scheme'] = data_urls['url'].apply(lambda x: urlparse(x).scheme)

        data_urls['domain_complete'] = data_urls['url'].apply(lambda x: urlparse(x).netloc)
        data_urls['domain_complete'] = data_urls['domain_complete'].str.replace('www.', '')
        data_urls['domain_complete'] = data_urls['domain_complete'].str.replace('www', '')

        data_urls['domain'] = data_urls['domain_complete'].apply(lambda x: tldextract.extract(x).domain)
        data_urls['subdomain'] = data_urls['domain_complete'].apply(lambda x: tldextract.extract(x).subdomain)
        data_urls['suffix'] = data_urls['domain_complete'].apply(lambda x: tldextract.extract(x).suffix)

        data_urls['subdomain'] = data_urls['subdomain'] + '.'
        data_urls['subdomain'] = data_urls['subdomain'].replace('.', '')

        data_urls['domain_subdomain'] = data_urls['subdomain'] + data_urls['domain']

        data_urls['path'] = data_urls['url'].apply(lambda x: urlparse(x).path)

        # Creación de Variables.

        # Variables del dominio
        # Cuenta los puntos
        data_urls['dom_n_puntos'] = data_urls['domain_subdomain'].str.count('\\.')
        data_urls['dom_n_guion'] = data_urls['domain_subdomain'].str.count('\\-')
        data_urls['dom_n_guionbajo'] = data_urls['domain_subdomain'].str.count('\\_')

        # Cuenta el largo total del dominio + subdominio
        data_urls['dom_len_tot'] = data_urls['domain_subdomain'].str.len()
        # Cuenta el largo del dominio y subdominio por separado
        data_urls['dom_len'] = data_urls['domain'].str.len()
        data_urls['dom_len_sub'] = data_urls['subdomain'].str.len()
        data_urls['url_len'] = data_urls['url'].str.len()
        # Cuenta vocales
        data_urls['dom_vocales'] = data_urls['domain_subdomain'].str.lower().str.count(r'[aeiou]')
        # Cuenta consonantes
        data_urls['dom_cons'] = data_urls['domain_subdomain'].str.lower().str.count(r'[a-z]') - data_urls['dom_vocales']
        # Cuenta números
        data_urls['dom_num'] = data_urls['domain_subdomain'].str.count('\d')
        # Cuenta cantidad de caracteres diferentes
        data_urls['dom_car_dif'] = data_urls['domain_subdomain'].apply(set).apply(len)

        def dummy_ip(columna):
            if columna == '':
                return 1
            else:
                return 0

        # Dominio es IP
        data_urls['dom_ip'] = data_urls['suffix'].apply(dummy_ip)

        #ip_dummies = pd.get_dummies(data_urls['suffix'] == '')
        #if ip_dummies.shape[1] == 2:
        #    data_urls['dom_ip'] = pd.get_dummies(data_urls['suffix'] == '', drop_first=True)
        #elif ip_dummies.shape[1] == 1:
        #    if ip_dummies.columns[0] == False:
        #        data_urls['dom_ip'] = pd.get_dummies(data_urls['suffix'] == '').replace(1,0)
        #    else:
        #        data_urls['dom_ip'] = pd.get_dummies(data_urls['suffix'] == '')
            
        # Variable dummy Scheme
        def dummy_http(columna):
            if columna == 'http':
                return 1
            else:
                return 0 
        def dummy_https(columna):
            if columna == 'https':
                return 1
            else:
                return 0 
        
        data_urls['sch_http'] = data_urls['scheme'].apply(dummy_http)
        data_urls['sch_https'] = data_urls['scheme'].apply(dummy_https)

        #sch_dummies = pd.get_dummies(data_urls['scheme'], prefix='sch')
        #data_urls = pd.concat([data_urls, sch_dummies], axis = 1)

        # Variables de Suffix
        data_urls['suf_len'] = data_urls['suffix'].str.len()

        # Creamos e imprimimos una lista con el top 5 de sufijos.
        top_suf_list = ['com', 'net', 'org', 'ru', 'xyz']
        
        def dummy_com(columna):
            if columna == 'com':
                return 1
            else:
                return 0        
        def dummy_net(columna):
            if columna == 'com':
                return 1
            else:
                return 0
        def dummy_org(columna):
            if columna == 'com':
                return 1
            else:
                return 0
        def dummy_ru(columna):
            if columna == 'com':
                return 1
            else:
                return 0
        def dummy_xyz(columna):
            if columna == 'com':
                return 1
            else:
                return 0
        def dummy_other(columna):
            if columna == 'other':
                return 1
            else:
                return 0

        data_urls['suffix2'] = data_urls['suffix']
        # Asignamos categoría 'other' a todas las clases que no pertenezcan a top_suf_list.
        data_urls.loc[data_urls['suffix2'].isin(top_suf_list).apply(np.bitwise_not), 'suffix2'] = 'other'
        # Armamos las columnas dummy.
        data_urls['suf_com'] = data_urls['suffix2'].apply(dummy_com)
        data_urls['suf_net'] = data_urls['suffix2'].apply(dummy_net)
        data_urls['suf_org'] = data_urls['suffix2'].apply(dummy_org)
        data_urls['suf_ru'] = data_urls['suffix2'].apply(dummy_ru)
        data_urls['suf_xyz'] = data_urls['suffix2'].apply(dummy_xyz)
        data_urls['suf_other'] = data_urls['suffix2'].apply(dummy_other)
        
        #suf_dummies = pd.get_dummies(data_urls['suffix2'], prefix='suf')
        #data_urls = pd.concat([data_urls, suf_dummies], axis = 1)

        for domain in self.metric_domains:
            data_urls['metric_ds_'+domain] = data_urls['domain_subdomain'].apply(lambda x: jellyfish.jaro_winkler(x, domain))
            data_urls['metric_d_'+domain] = data_urls['domain'].apply(lambda x: jellyfish.jaro_winkler(x, domain))
            data_urls['metric_s_'+domain] = data_urls['subdomain'].apply(lambda x: jellyfish.jaro_winkler(x, domain))
            data_urls['metric_p_'+domain] = data_urls['path'].apply(lambda x: jellyfish.jaro_winkler(x, domain))


        self.data = data_urls.copy()
        self.data.drop_duplicates(subset=['domain_complete'], inplace = True)
        self.data.drop(['url', 'scheme', 'domain_complete', 'domain', 'subdomain','suffix', 'domain_subdomain', 'suffix2', 'path'], axis = 1, inplace = True)
        return self.data

    def obtenerDataProcesada(self):
        return self.data

    def importarModelo(self, direccion = 'trained_rf.joblib'):
        self.modelo = load(direccion)

    def calcularProbabilidad(self, data_urls, direccion = 'trained_rf.joblib'):
        
        self.prepararInput(data_urls)
        
        if self.modelo == 0:
            self.importarModelo(direccion)
        
        self.prediccion = self.modelo.predict_proba(self.data)

        return self.prediccion