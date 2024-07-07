from fastapi import FastAPI
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import hstack


app= FastAPI()

#Preparar los dataset para trabajar las funciones a partir de ellos.
base_dir = os.path.dirname(__file__)
movies_path = os.path.join(base_dir, 'Datasets', 'movies_FINAL.csv')
cast_path = os.path.join(base_dir, 'Datasets', 'cast.parquet')
crew_path = os.path.join(base_dir, 'Datasets', 'crew.parquet')

print("Ruta absoluta del archivo movies_FINAL.csv:", os.path.abspath(movies_path))
print("Ruta absoluta del archivo cast.parquet:", os.path.abspath(cast_path))
print("Ruta absoluta del archivo crew.parquet:", os.path.abspath(crew_path))

df_final = pd.read_csv(movies_path)
df_credit_cast = pd.read_parquet(cast_path)
df_credit_crew = pd.read_parquet(crew_path)

# Convertir la columna release_date a datetime
df_final['release_date'] = pd.to_datetime(df_final['release_date'], errors='coerce')



@app.get("/", tags =['Home'])
def Home():
    return "A continuación se presentarán 6 funciones en relación a datasets de películas y un Sistema de Recomendación"


@app.get("/cantidad_filmaciones_mes")
def cantidad_filmaciones_mes(mes):
    
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }

    mes = mes.lower()
    
    mes_num = meses.get(mes)
    
    if mes_num is None:
        return ValueError(f"Mes '{mes}' no reconocido. Por favor ingresa un mes válido.")
    
    filmaciones_mes = df_final[df_final['release_date'].dt.month == mes_num]
    
    return len(filmaciones_mes)


@app.get("/cantidad_filmaciones_dia/{id}")
def cantidad_filmaciones_dia(dia):
    dias_semana = {
        'lunes': 1,
        'martes': 2,
        'miercoles': 3,
        'miércoles':4,
        'jueves':5,
        'viernes':6,
        'sabado':7,
        'domingo':8
   
    }

   
    dia_num = dias_semana.get(dia)
    
    if dia_num is None:
        return ValueError(f"Día '{dia}' no reconocido. Por favor ingresa un mes válido.")
    
    filmaciones_dia = df_final[df_final['release_date'].dt.day == dia_num]
    
    return len(filmaciones_dia)


@app.get("/score_titulo/{id}")
def score_titulo(titulo):
    pelicula = df_final[df_final['title'].str.lower() == titulo.lower()]

    if pelicula.empty:
        return f"No se encontró ninguna película con el título '{titulo}'."
    
    titulo_pelicula = pelicula.iloc[0]['title']
    año_estreno = pelicula.iloc[0]['release_date'].year
    popularity = pelicula.iloc[0]['popularity']
    
    return {
        'Título': titulo_pelicula,
        'Año de Estreno': año_estreno,
        'Score': popularity
    }


@app.get("/votos_titulo/{id}")
def  votos_titulo(titulo):
    
    pelicula = df_final[df_final['title'].str.lower() == titulo.lower()]

    if pelicula.empty:
        return f"No se encontró ninguna película con el título '{titulo}'."
    
    titulo_pelicula = pelicula.iloc[0]['title']
    vote_count = pelicula.iloc[0]['vote_count']
    vote_average= pelicula.iloc[0]['vote_average']

    if vote_count < 2000:
        return f"La película '{titulo_pelicula}' no cumple con el requisito de al menos 2000 valoraciones."

    
    return {
        'Título': titulo_pelicula,
        'Votos': vote_count,
        'Votos Promedio': vote_average,
    }

    
@app.get("/get_actor/{id}")
def get_actor(nombre_actor):
    try:
        df_actor = df_credit_cast[df_credit_cast['cast_name'] == nombre_actor]
        
        if df_actor.empty:
            return f"El actor {nombre_actor} no se encontró en el dataset."

        if 'movie_id' not in df_actor.columns or 'movie_id' not in df_final.columns:
            return "Error: La columna común 'movie_id' no existe en uno de los DataFrames."
        
        df_actor_movies = pd.merge(df_actor, df_final, on='movie_id')
        
        df_actor_movies = df_actor_movies.drop_duplicates(subset=['title'])
        
        total_retorno = df_actor_movies['return'].sum()
        cantidad_peliculas = len(df_actor_movies)
        promedio_retorno = df_actor_movies['return'].mean()
        
        mensaje = (f"El actor {nombre_actor} ha participado de {cantidad_peliculas} filmaciones, "
                   f"con un retorno total de {total_retorno} y un promedio de {promedio_retorno:.2f} por filmación.")
        
        return mensaje
    except KeyError as e:
        return f"Error: La columna {e} no existe en el DataFrame."
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/get_director/{id}")
def get_director(nombre_director):
    df_director = df_credit_crew[(df_credit_crew['crew_job'] == 'Director') & 
                                 (df_credit_crew['crew_name'] == nombre_director)]
    
    df_director_movies = pd.merge(df_director, df_final, on='movie_id')
    
    df_director_movies['return'] = df_director_movies['revenue'] - df_director_movies['budget']
    
    df_director_movies = df_director_movies.drop_duplicates(subset=['title'])
    
    resultado = []
    for _, row in df_director_movies.iterrows():
        titulo = row['title']
        fecha_lanzamiento = row['release_date']
        retorno_individual = row['return']
        costo = row['budget']
        ganancia = row['revenue']
        
        resultado.append({
            'Título': titulo,
            'Fecha de Lanzamiento': fecha_lanzamiento,
            'Retorno Individual': retorno_individual,
            'Costo': costo,
            'Ganancia': ganancia
        })
    
    return resultado

#Preprocesamiento para el Sistema de Recomendación.
df_final['combined_features'] = df_final['title'] + ' ' + df_final['genres_names_array'].fillna('') + ' ' + df_final['overview'].fillna('')

sample_size = 1000  # Se ajustó en función de problemas de memoria
df_sampled = df_final.sample(n=sample_size, random_state=42)

tfidf = TfidfVectorizer(stop_words='english')

tfidf_matrix = tfidf.fit_transform(df_sampled['combined_features'])

cosine_sim_sampled = cosine_similarity(tfidf_matrix, tfidf_matrix)

cosine_sim_sampled_df = pd.DataFrame(cosine_sim_sampled, index=df_sampled['title'], columns=df_sampled['title'])


@app.get("/Recomendacion/{id}")
def recommend_movies(title):
    if title not in cosine_sim_sampled_df.index:
        return f"Movie titled '{title}' not found in the dataset."

    sim_scores = cosine_sim_sampled_df[title]

    sim_scores = sim_scores.sort_values(ascending=False)

    top_similar_movies = sim_scores.iloc[1:5].index

    return df_final[df_final['title'].isin(top_similar_movies)][['title', 'genres_names_array', 'overview']]
