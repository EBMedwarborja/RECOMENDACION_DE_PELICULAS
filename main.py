from fastapi import FastAPI
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import List
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from recomendacion import recomendacion


import pandas as pd
import calendar

# Crear la app de FastAPI
app = FastAPI()

# Cargar los datasets desde la ruta local
ruta_base = r'C:\Users\edwar\Documents\PROYETO_DTA_01_SISTEMA_DE_RECOMENDACION\rpeliculas\DATASET'

movies_df = pd.read_csv(f'{ruta_base}\\movies_dataset.csv')
cast_df = pd.read_csv(f'{ruta_base}\\cast_data.csv')
crew_df = pd.read_csv(f'{ruta_base}\\crew_data.csv')

# Preprocesar los datos para facilitar las consultas
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'], errors='coerce')

# Mapeo de meses en español a números
meses = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
}

# Función: cantidad_filmaciones_mes
@app.get("/cantidad_filmaciones_mes/")
def cantidad_filmaciones_mes(mes: str):
    mes = mes.lower()
    if mes in meses:
        mes_num = meses[mes]
        cantidad = movies_df[movies_df['release_date'].dt.month == mes_num].shape[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"
    else:
        return "Mes no válido. Por favor ingrese un mes en español."

# Función: cantidad_filmaciones_dia
@app.get("/cantidad_filmaciones_dia/")
def cantidad_filmaciones_dia(dia: str):
    dia = dia.capitalize()
    try:
        day_num = list(calendar.day_name).index(dia)
        cantidad = movies_df[movies_df['release_date'].dt.dayofweek == day_num].shape[0]
        return f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}"
    except ValueError:
        return "Día no válido. Por favor ingrese un día de la semana en español."

# Función: score_titulo
@app.get("/score_titulo/")
def score_titulo(titulo: str):
    pelicula = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    if not pelicula.empty:
        titulo = pelicula.iloc[0]['title']
        estreno = pelicula.iloc[0]['release_year']
        score = pelicula.iloc[0]['vote_average']
        return f"La película {titulo} fue estrenada en el año {int(estreno)} con un score/popularidad de {score}"
    else:
        return "Película no encontrada."

# Función: votos_titulo
@app.get("/votos_titulo/")
def votos_titulo(titulo: str):
    pelicula = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    if not pelicula.empty:
        votos = pelicula.iloc[0]['vote_count']
        promedio_votos = pelicula.iloc[0]['vote_average']
        titulo = pelicula.iloc[0]['title']
        estreno = pelicula.iloc[0]['release_year']
        if votos >= 2000:
            return f"La película {titulo} fue estrenada en el año {int(estreno)}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}"
        else:
            return "La película no cuenta con al menos 2000 valoraciones."
    else:
        return "Película no encontrada."

# Función: get_actor
@app.get("/get_actor/")
def get_actor(nombre_actor: str):
    actor_peliculas = cast_df[cast_df['name'].str.lower() == nombre_actor.lower()]
    if not actor_peliculas.empty:
        actor_id = actor_peliculas.iloc[0]['id']
        peliculas_actor = movies_df[movies_df['id'].isin(actor_peliculas['id'])]
        total_retorno = peliculas_actor['return'].sum()
        promedio_retorno = peliculas_actor['return'].mean()
        cantidad_peliculas = peliculas_actor.shape[0]
        return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} filmaciones, obteniendo un retorno total de {total_retorno:.2f} y un promedio de {promedio_retorno:.2f} por filmación."
    else:
        return "Actor no encontrado."

# Función: get_director
@app.get("/get_director/")
def get_director(nombre_director: str):
    director_info = crew_df[(crew_df['name'].str.lower() == nombre_director.lower()) & (crew_df['job'] == "Director")]
    if not director_info.empty:
        director_peliculas = movies_df[movies_df['id'].isin(director_info['id'])]
        retorno_total = director_peliculas['return'].sum()
        peliculas_info = director_peliculas[['title', 'release_date', 'budget', 'revenue', 'return']].to_dict(orient='records')
        return {
            "director": nombre_director,
            "peliculas": peliculas_info,
            "retorno_total": retorno_total,
            "cantidad_peliculas": director_peliculas.shape[0]
        }
    else:
        return "Director no encontrado."



@app.get("/recomendacion/{titulo}")
def get_recomendacion(titulo: str):
    """Endpoint para obtener recomendaciones de películas basadas en un título."""
    return {"recomendaciones": recomendacion(titulo)}














