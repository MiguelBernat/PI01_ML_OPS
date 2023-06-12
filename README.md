# Proyecto individual 1: "MLOps Engineer" (Data Engineer & Machine Learning)
### Por Miguel Vázquez Bernat
-----------------------------------------
## Introducción
Primer proyecto de la parte de Labs del Bootcamp SoyHenry.
Se realizó un proceso de extracción de archivos tipo csv con información sobre diversas peliculas en plataformas de streaming, que se encontraban almacenados en la web, para su transformación, su análisis exploratorio, su carga a un modelo de machine learning para un sistema de recomendación de títulos de películas y por último, la carga de los datos limpios a una API que permite al usuario realizar consultas sobre este dataset.

----------------------------------

## ETL y EDA
Primero se importaron los archivos movies_dataset.csv y credits.csv y se concatenaron para su utilización como dataframe. [Link hacia el repositorio](https://drive.google.com/drive/folders/1WzUxe32Lqeh8rccOvdSMt2o2PaNu1iN4?usp=sharing)

ETL (Extract, Transform and Load): Se desanidaron las columnas en donde el formato de sus valores eran JSON, se normalizaron las columnas del dataframe, se cambio el tipo de dato de las columnas, se eliminaron valores nulos y por último se eliminaron las columnas que no se utilizarían en este proyecto (Checar el notebook ETL.ipynb).

EDA (Exploratory Data Analysis): Se visualizaron múltiples gráficos para el entendimiento de los datos, como por ejemplo, que género de películas es el que mas se repite en el dataset (Checar el notebook EDA.ipynb).

-------------------
## Sistema de recomendación
Con los datos limpios y un análisis adecuado de la información que se obtuvo de los datasets, se creó un modelo de Machine Learning utilizando técnicas de procesamiento del lenguaje natural para que al ingresar el título de una película nos recomiende 5 películas de acuerdo a las palabras claves que se repitan dentro de la sinopsis de las películas, los actores, el género y los mismos títulos de estas.

NOTA: Dado que el archivo binario del modelo es muy pesado, se redujo la cantidad de filas a utilizar en este mismo a 4000.

---------------------------------------

## API
Para la creación de la API, se creó un entorno virtual de Python, que permite trabajar las consultas con el modulo de fastAPI. Este modulo permite crear una plataforma y/o servicio web, por medio del servidor Render, que trabaja bajo sistema HTTP simples. En este [enlace](https://proyecto-individual-ml-ops-awac.onrender.com/docs) podemos realizar las consultas siguientes:

* Cantidad de películas que se estrenaron un mes determinado historicamente (cantidad_filmaciones_mes).
* Cantidad de películas que se estrenaron un día determinado historicamente (cantidad_filmaciones_dia).
* Score de popularidad de una película determinada (score_titulo).
* Cantidad de votos y valor promedio de las votaciones para de una película (votos_titulo).
* Cantidad de películas en las que ha participado un actor determinado, su retorno total y retorno promedio (get_actor).
* Películas en las que ha participado un director determinado, así como su retorno por cada una y su retorno total (get_director)
* Por último, se puede realizar una consulta en la que se ingresa el título de una película y nos recomendará 5 películas similares gracias a nuestra implementación de Machine Learning.