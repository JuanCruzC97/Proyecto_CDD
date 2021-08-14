# Proyecto_CDD

A partir del análisis realizado sobre el dataset del Proyecto B surgen varias cuestiones:
	1. Pueden haber sesgos entre las observaciones, siendo las clases muy diferentes entre si.
	2. No conocemos los URLs utilizados.
	3. No podemos recrear las variables con URLs propios.
	
Teniendo en cuenta estos puntos decidimos armar nuestro propio dataset de URLs a partir del cual generamos las variables explicativas para los modelos. Como ventaja tenemos que las variables van a poder ser replicadas para cualquier URL y que incluímos en las observaciones no solo páginas benignas y maliciosas, sino que dentro de las benignas tenemos principalmente páginas que fueron sospechosas, pero no phishing.

Todos los datos fueron scrapeados de Phishtank, teniendo observaciones INVALID (sospechoso pero no phishing) y VALID (phishing). Además tenemos el top 1M de websites de el sitio Alexa obtenido por de Kaggle, sitio usualmente usado para obtener las ULR benignas.

## Pasos

### Generación de Datos
* Scrapear los datos.
* Armar dataset completo.
* Segmentar los URLs en partes (dominio, path, suffix, etc).

### Creación de Variables
* Calcular largos de partes del URL.
* Contar aparición 
