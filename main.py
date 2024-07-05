from fastapi import FastAPI
from pandas import DataFrame as pd
from pandas import lower as pd

app= FastAPI()
df_final=pd.DataFrame("Datasets\movies_FINAL.csv")
df_credit_cast = pd.DataFrame("Datasets\cast.parquet")
df_credit_crew = pd.DataFrame("Datasets\crew.parquet")

@app.get("/")
def estrenos_por_mes(mes):
    
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

    # Convertir el mes ingresado a minúsculas para asegurar coincidencia
    mes = mes.lower()
    
    # Obtener el número del mes correspondiente
    mes_num = meses.get(mes)
    
    if mes_num is None:
        return ValueError(f"Mes '{mes}' no reconocido. Por favor ingresa un mes válido.")
    
    # Filtrar el DataFrame por el mes
    filmaciones_mes = df_final[df_final['release_date'].dt.month == mes_num]
    
    # Devolver la cantidad de películas
    return len(filmaciones_mes)


@app.get("/estrenos_por_dia/{id}")
def estrenos_por_dia(dia):
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

   
    # Obtener el número del mes correspondiente
    dia_num = dias_semana.get(dia)
    
    if dia_num is None:
        return ValueError(f"Día '{dia}' no reconocido. Por favor ingresa un mes válido.")
    
    # Filtrar el DataFrame por el mes
    filmaciones_dia = df_final[df_final['release_date'].dt.day == dia_num]
    
    # Devolver la cantidad de películas
    return len(filmaciones_dia)


@app.get("/obtener_informacion_pelicula/{id}")



# Convertir la columna release_date a datetime
df_final['release_date'] = pd.to_datetime(df_final['release_date'], errors='coerce')

# Verificar la conversión
print(df_final['release_date'])

# Función para obtener información de la película
def obtener_informacion_pelicula(titulo):
    # Filtrar el DataFrame por el título
    pelicula = df_final[df_final['title'].str.lower() == titulo.lower()]

    # Verificar si la película existe
    if pelicula.empty:
        return f"No se encontró ninguna película con el título '{titulo}'."
    
    # Obtener la información de la película
    titulo_pelicula = pelicula.iloc[0]['title']
    año_estreno = pelicula.iloc[0]['release_date'].year
    popularity = pelicula.iloc[0]['popularity']
    
    return {
        'Título': titulo_pelicula,
        'Año de Estreno': año_estreno,
        'Score': popularity
    }


@app.get("/obtener_informacion_pelicula_promedio_votaciones/{id}")
def obtener_informacion_pelicula_promedio_votaciones(titulo):
    
    # Filtrar el DataFrame por el título
    pelicula = df_final[df_final['title'].str.lower() == titulo.lower()]

    # Verificar si la película existe
    if pelicula.empty:
        return f"No se encontró ninguna película con el título '{titulo}'."
    
    # Obtener la información de la película
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
        # Filtrar el DataFrame df_credit_cast para obtener las películas en las que ha participado el actor
        df_actor = df_credit_cast[df_credit_cast['cast_name'] == nombre_actor]
        
        # Verificar si df_actor está vacío
        if df_actor.empty:
            return f"El actor {nombre_actor} no se encontró en el dataset."

        # Asegurarnos de que la columna común se llama 'movie_id' en ambos DataFrames
        if 'movie_id' not in df_actor.columns or 'movie_id' not in df_final.columns:
            return "Error: La columna común 'movie_id' no existe en uno de los DataFrames."
        
        # Unir con df_movies usando la columna 'movie_id'
        df_actor_movies = pd.merge(df_actor, df_final, on='movie_id')
        
        # Eliminar duplicados basándonos en el título de la película
        df_actor_movies = df_actor_movies.drop_duplicates(subset=['title'])
        
        # Calcular el éxito del actor medido a través del retorno
        total_retorno = df_actor_movies['return'].sum()
        cantidad_peliculas = len(df_actor_movies)
        promedio_retorno = df_actor_movies['return'].mean()
        
        # Preparar el mensaje de resultado
        mensaje = (f"El actor {nombre_actor} ha participado de {cantidad_peliculas} filmaciones, "
                   f"con un retorno total de {total_retorno} y un promedio de {promedio_retorno:.2f} por filmación.")
        
        return mensaje
    except KeyError as e:
        return f"Error: La columna {e} no existe en el DataFrame."
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/get_director/{id}")
def get_director(nombre_director):
    # Filtrar el DataFrame df_credit_crew para obtener las películas dirigidas por el director
    df_director = df_credit_crew[(df_credit_crew['crew_job'] == 'Director') & 
                                 (df_credit_crew['crew_name'] == nombre_director)]
    
    # Unir con df_movies usando la columna 'id'
    df_director_movies = pd.merge(df_director, df_final, on='movie_id')
    
    # Calcular el retorno (revenue - budget) y agregarlo al DataFrame
    df_director_movies['return'] = df_director_movies['revenue'] - df_director_movies['budget']
    
    # Eliminar duplicados basándonos en el título de la película
    df_director_movies = df_director_movies.drop_duplicates(subset=['title'])
    
    # Preparar el resultado
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

