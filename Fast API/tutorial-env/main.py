import fastapi

app = fastapi()

#http://127.0.0.1:8000

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
