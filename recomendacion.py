# recomendacion.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

# Ruta del dataset
DATASET_PATH = r'C:\Users\edwar\Documents\PROYETO_DTA_01_SISTEMA_DE_RECOMENDACION\DATASET\movies_dataset.csv'

def cargar_datos():
    """Cargar los datos desde el archivo CSV."""
    return pd.read_csv(DATASET_PATH)

def recomendacion(titulo):
    """Recomendar películas similares basadas en el título dado."""
    # Cargar el dataset
    movies_df = cargar_datos()
    
    # Verificar si el título está en el DataFrame
    if titulo not in movies_df['title'].values:
        return "Título no encontrado en el dataset."

    # Crear una matriz de TF-IDF para los títulos de las películas
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['title'])
    
    # Calcular la similitud del coseno entre las películas
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # Encontrar el índice del título dado
    idx = movies_df.index[movies_df['title'] == titulo].tolist()[0]
    
    # Obtener las similitudes del título dado con todas las demás películas
    sim_scores = list(enumerate(cosine_similarities[idx]))
    
    # Ordenar las películas basadas en la similitud y seleccionar las 5 principales
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Excluir la primera película que es la misma película

    # Obtener los índices de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]
    
    # Obtener los títulos de las películas recomendadas
    return movies_df['title'].iloc[movie_indices].tolist()
