# Proyecto_CDD

Links útiles:

* https://www.sciencedirect.com/science/article/pii/S2352340920313202#utbl0001
* https://data.mendeley.com/datasets/72ptz43s9v/1

# Pasos

## Entender los Datos:

0. Entender todas las variables (principalmente las finales)
1. Entender cómo fue generado el dataset (faltantes de urls dudosos).
2. Elegir mejor approach:
	a. Usar dataset con variables generadas
	b. Usar dataset con URLs para generar analisis propio y variables propias.

### Webscraping

* Resolver Captcha en links particulares.[Parcial]
* Eliminar la columna URL_esp (se consigue con id).[Listo]
* Agregar sleep aleatorio.[Listo]

## Preparación de Datos: 

1. Borrar duplicados 
2. Borrar variables que tengan solo un unico valor [LISTO]
3. Elegir corte de cantidad de -1 aceptables 
4. Definir que variables entran en el analisis  
5. Fijarse de las variables replicables, cuantas podemos construir nosotros desde un dataset de URL´s

## Creación de Variables:

* Variables dummy según composición del URL

## Análisis Exploratorio: 

* Árbol de Clasificación (variables importantes)
* Análisis de Correlaciones
* PCA (Ver dimensiones principales y plotear)
* Clustering (para ver si encontramos algo)

## Predicción: 

* **Modelos Regresión**:
	* Regresión logística
	* Regresión logística Ridge 
	* Regresión logística Lasso 
	* Regresión logística ElasticNet (regularizacion mas ratio)

* **Modelos KNN**:
	* KNN (k)
	
* **Modelos SVM**:
	* SVM Lineal (C)
	* SVM Kernel Poly (C, degree)
	* SVM Radial (C, gamma)
	
* **Modelos Árboles**:
	* Árbol de Clasificación
	* Random Forest (muchos) 
	* Modelos Boost
