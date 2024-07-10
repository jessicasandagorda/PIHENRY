::: {.cell .markdown}
# Sistema de Recomendación de Películas
:::

::: {.cell .markdown}
Este proyecto consiste en la creación de un sistema de recomendación de
películas. El objetivo es proporcionar recomendaciones personalizadas
basadas en diversos criterios. A continuación se detallan las fases del
proyecto y las funcionalidades implementadas sobre diferentes datos
acerca de películas.
:::

::: {.cell .markdown}
### Fases del Proyecto
:::

::: {.cell .markdown}
1.  Extracción, Transformación y Carga (ETL) Se realizó un proceso ETL
    para preparar los datos necesarios para el sistema de recomendación.
    Este proceso incluyó:

-   Extracción: Obtención de datos de múltiples fuentes (archivos CSV y
    Parquet).
-   Transformación: Limpieza y normalización de los datos, incluyendo el
    manejo de valores nulos y la conversión de tipos de datos.
-   Carga: Almacenamiento de los datos transformados en un formato
    adecuado para su análisis (Parquet y CSV).

1.  Análisis Exploratorio de Datos (EDA) Se llevó a cabo un EDA para
    comprender mejor los datos y extraer información relevante. Esto
    incluyó:

-   Análisis de las distribuciones de las variables clave.
-   Identificación de patrones y relaciones entre diferentes variables.
-   Visualización de datos para detectar tendencias y anomalías.
-   Análisis y/o tratamiento de valores nulos, duplicados y faltantes.
-   Análisis de tipo de datos.

A través de gráficas y abordajes estadísticos pertinentes ya sean bi o
multivariados.

1.  Desarrollo de Funciones Se desarrollaron seis funciones:

-   cantidad_filmaciones_mes: Esta función recibe el nombre de un mes
    (por ejemplo, \'enero\', \'febrero\') y devuelve la cantidad de
    filmaciones realizadas en ese mes.

-   cantidad_filmaciones_dia: Esta función recibe el nombre de un día de
    la semana (por ejemplo, \'lunes\', \'martes\') y devuelve la
    cantidad de filmaciones realizadas en ese día.

-   score_titulo: Esta función recibe el título de una película y
    devuelve su popularidad (score), junto con el año de estreno y el
    título de la película.

-   votos_titulo: Esta función recibe el título de una película y
    devuelve la cantidad de votos y el promedio de votos. Si la película
    tiene menos de 2000 votos, se devuelve un mensaje indicando que no
    cumple con el requisito.

-   get_actor : Esta función recibe el nombre de un actor y devuelve la
    cantidad de filmaciones en las que ha participado, el retorno total
    y el promedio de retorno por filmación.

-   get_director: Esta función recibe el nombre de un director y
    devuelve una lista de las películas dirigidas por él, incluyendo el
    título, fecha de lanzamiento, retorno individual, costo y ganancia
    de cada película.
:::

::: {.cell .markdown}
### Despliegue de la API
:::

::: {.cell .markdown}
El sistema de recomendación se desplegó como una API, lo que permite su
acceso y uso a través de una URL pública. La API está diseñada para ser
accesible y fácil de usar, proporcionando endpoints para cada una de las
funciones de recomendación. Se utilizó FastAPI y Render.com para este
fin
:::

::: {.cell .markdown}
### Video de presentación
:::

::: {.cell .markdown}
Se elaboró un video de presentación para mostrar el funcionamiento y las
características del sistema de recomendación de películas. Este video
explica las funcionalidades clave y cómo utilizar la API para obtener
recomendaciones personalizadas.
:::

::: {.cell .markdown}
### Instrucciones de Uso
:::

::: {.cell .markdown}
1.  Clona el repositorio: git clone
    <https://github.com/tu-usuario/proyecto-recomendacion-peliculas.git>
    cd proyecto-recomendacion-peliculas

2.  Instala las dependencias: pip install -r requirements.txt

3.  Ejecuta el servidor de la API: uvicorn app:app \--reload

4.  Accede a la API: Una vez que el servidor esté en funcionamiento,
    puedes acceder a la API en <https://pi-henry-zco1.onrender.com>. La
    documentación interactiva está disponible en
    <https://pi-henry-zco1.onrender.com/docs>.
:::

::: {.cell .markdown}
### Acceso al repositorio en GitHub
:::

::: {.cell .markdown}
<https://github.com/jessicasandagorda/PIHENRY>
:::
