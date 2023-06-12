import pandas as pd
from fastapi import FastAPI
import numpy as np
import pickle

app = FastAPI()

movies = pd.read_csv("movies_clean.csv") # Se carga el dataset moviel_clean.csv a un dataframe.
movies['release_date'] = pd.to_datetime(movies['release_date'])
movies_ML = pd.read_csv("movies_ML.csv") # Se carga el dataset movies_ML.csv a un dataframe.

with open('model_similarity.pkl', 'rb') as archivo: 
    similarity = pickle.load(archivo) # Se carga el archivo model_similarity.pkl.

# fastapi-env\Scripts\activate.bat
# uvicorn main:app --reload
# http://127.0.0.1:8000/docs

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes_es: str):
    '''Se ingresa el mes y la funcion retorna 
        la cantidad de peliculas que se estrenaron 
        en ese mes historicamente.'''
    
    mes = mes_es.lower()
    
    if mes == "enero":
        mes = "January"
    if mes == "febrero":
        mes = "February"
    if mes == "marzo":
        mes = "March"
    if mes == "abril":
        mes = "April"
    if mes == "mayo":
        mes = "May"
    if mes == "junio":
        mes = "June"
    if mes == "julio":
        mes = "July"
    if mes == "agosto":
        mes = "August"
    if mes == "septiembre":
        mes = "September"
    if mes == "octubre":
        mes = "October"
    if mes == "noviembre":
        mes = "November"
    if mes == "diciembre":
        mes = "December"

    peliculas = movies[movies['release_date'].dt.strftime('%B') == mes]
    return {"mes": mes_es.lower(), "cantidad": len(peliculas)}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia_es: str):
    '''Se ingresa el día y la funcion retorna 
        la cantidad de peliculas que se estrenaron 
        en ese dia historicamente.'''
    
    dia_es = dia_es.lower()
    dia = dia_es

    if dia_es == "miercoles":
        dia_es = "miércoles"
    if dia_es == "sabado":
        dia_es = "sábado"

    if dia == "lunes":
        dia = "Monday"
    if dia == "martes":
        dia = "Tuesday"
    if dia == "miercoles" or dia == "miércoles":
        dia = "Wednesday"
    if dia == "jueves":
        dia = "Thursday"
    if dia == "viernes":
        dia = "Friday"
    if dia == "sabado" or dia == "sábado":
        dia = "Saturday"
    if dia == "domingo":
        dia = "Sunday"
        
    peliculas = movies[movies['release_date'].dt.strftime('%A') == dia]
    return {"mes": dia_es, "cantidad": len(peliculas)}

@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    ''' Se ingresa el título de una filmación 
        y la función retorna el título, el año del estreno 
        y el score de esta misma.'''
    
    pelicula = movies[['release_year', 'popularity']][movies['title'] == titulo_de_la_filmacion]
    lista_anio = []
    lista_score = []
    lista_resultados = []

    for i in range(0, len(pelicula)):
        lista_anio.append(pelicula.values[i][0])
        lista_score.append(pelicula.values[i][1])


    for i in range(0, len(pelicula)):
        lista_resultados.append({"titulo": titulo_de_la_filmacion, "anio": int(lista_anio[i]), "popularidad": round(lista_score[i], 2)})

    return lista_resultados

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    '''Se ingresa el título de una filmación y la función retorna el título, 
        la cantidad de votos y el valor promedio de las votaciones de esta misma pelicula 
        siempre y cuando la cantidad de votos sea mayor a 2000, de lo contrario devolverá 
        un mensaje avisando que no cumple con esta condición.'''

    pelicula = movies[['release_year','vote_count', 'vote_average']][movies['title'] == titulo_de_la_filmacion]
    
    lista_resultado = []
    dict_menor_2000 = {}
    for i in range(0, len(pelicula)):
        if pelicula.values[i][1] < 2000:
            dict_menor_2000.update({"message": f"No hay ninguna pelicula de {titulo_de_la_filmacion} donde la cantidad de votos sea mayor a 2000, por ende, no se devuelve ningun valor."})
        else:
            lista_resultado.append({"titulo": titulo_de_la_filmacion, 
                                    "año": int(pelicula.values[i][0]), 
                                    "voto_total": int(pelicula.values[i][1]), 
                                    "voto_promedio": round(pelicula.values[i][2], 2) })

    if len(lista_resultado) > 0:
        return lista_resultado
    else:
        return dict_menor_2000

@app.get("/get_actor/{nombre_actor}")    
def get_actor(nombre_actor: str):
    '''Se ingresa el nombre de un actor y la función devuelve 
        el éxito de este mismo medido a través del retorno, 
        la cantidad de peliculas en las que ha participado y 
        el promedio de retorno.'''

    actores_filtro = [nombre_actor]
    movies_filtrado = movies[movies['cast'].apply(lambda x: any(actor in x for actor in actores_filtro))]
    cantidad_peliculas = int(movies_filtrado.title.value_counts().sum())
    retorno = round(float(movies_filtrado['return'].values.sum()), 2)
    promedio_retorno = round(retorno/cantidad_peliculas, 2)

    return {"actor": nombre_actor, "cantidad_filmaciones": cantidad_peliculas, "retorno_total": retorno, "retorno_promedio": promedio_retorno}


@app.get("/get_director/{nombre_director}") 
def get_director(nombre_director: str):
    '''Se ingresa el nombre de un director de cine y la función 
        retorna el nombre y el retorno total de este mismo, 
        así como las peliculas que ha dirigido, con sus respectivas 
        fechas de estreno, retornos, presupuestos y ganancias. '''
    
    directores_filtro = [nombre_director]
    movies_filtrado = movies[movies["director"].apply(lambda x: any(director in x for director in directores_filtro))]
    lista_peliculas = [movies_filtrado["title"].values[i] for i in range(0, len(movies_filtrado["title"].values))]
    lista_anio = [np.datetime_as_string(movies_filtrado["release_date"].values[i], unit='D') for i in range(0, len(movies_filtrado["release_date"].values))]
    lista_retorno = [float(movies_filtrado["return"].values[i]) for i in range(0, len(movies_filtrado["return"].values))]
    lista_budget = [int(movies_filtrado["budget"].values[i]) for i in range(0, len(movies_filtrado["budget"].values))]
    lista_ganancia = [int(movies_filtrado["revenue"].values[i]) for i in range(0, len(movies_filtrado["revenue"].values))]
    retorno_total_director = float(round(movies_filtrado["return"].sum(), 2))

    return {'director': nombre_director, 
            'retorno_total_director': retorno_total_director, 
            'peliculas': lista_peliculas, 'anio': lista_anio, 
            'retorno_pelicula': lista_retorno, 
            'budget_pelicula': lista_budget, 
            'revenue_pelicula': lista_ganancia}


@app.get("/recomendacion/{titulo}") 
def recomendacion(movie: str):
    '''Se ingresa una película y a partir de esta la función retorna 
        una recomendación de 5 películas en forma de lista. '''
    
    id_movie = movies_ML[movies_ML['title']==movie].index[0]
    distancias = similarity[id_movie]
    movie_list = sorted(list(enumerate(distancias)), reverse=True, key=lambda x:x[1])[1:6]
    lista_recomendacion = []

    for movie_id in movie_list:
        lista_recomendacion.append(movies_ML.iloc[movie_id[0]].title)
        
    return {'lista_recomendada': lista_recomendacion}