
# Movie Recommendation System

This project involves creating a movie recommendation system. The goal is to provide personalized recommendations based on various criteria. Below are the phases of the project and the implemented functionalities on different movie data.

### Project Phases

1. **Extraction, Transformation, and Loading (ETL)**  
   An ETL process was carried out to prepare the necessary data for the recommendation system. This process included:
   - **Extraction**: Obtaining data from multiple sources (CSV and Parquet files).
   - **Transformation**: Cleaning and normalizing the data, including handling null values and converting data types.
   - **Loading**: Storing the transformed data in a suitable format for analysis (Parquet and CSV).

2. **Exploratory Data Analysis (EDA)**  
   EDA was conducted to better understand the data and extract relevant information. This included:
   - Analyzing the distributions of key variables.
   - Identifying patterns and relationships between different variables.
   - Data visualization to detect trends and anomalies.
   - Analysis and/or treatment of null, duplicate, and missing values.
   - Data type analysis.
   
   This was done through appropriate graphs and statistical approaches, whether bivariate or multivariate.

3. **Function Development**  
   Six key functions were developed:
   - **Monthly Film Count (`cantidad_filmaciones_mes`)**: This function receives the name of a month (e.g., 'January', 'February') and returns the number of films made in that month.
   - **Daily Film Count (`cantidad_filmaciones_dia`)**: This function receives the name of a day of the week (e.g., 'Monday', 'Tuesday') and returns the number of films made on that day.
   - **Movie Score by Title (`score_titulo`)**: This function receives the title of a movie and returns its popularity score, along with the release year and the movie title.
   - **Vote Count by Title (`votos_titulo`)**: This function receives the title of a movie and returns the number of votes and the average vote score. If the movie has fewer than 2000 votes, it returns a message indicating that it does not meet the requirement.
   - **Actor Information (`get_actor`)**: This function receives the name of an actor and returns the number of films they have participated in, the total return, and the average return per film.
   - **Director Information (`get_director`)**: This function receives the name of a director and returns a list of films directed by them, including the title, release date, individual return, cost, and revenue for each film.

4. **API Deployment**  
   The recommendation system was deployed as an API, allowing access and usage through a public URL. The API is designed to be accessible and easy to use, providing endpoints for each of the recommendation functions. FastAPI and Render.com were used for this purpose.

### Presentation Video

A presentation video was created to demonstrate the functionality and features of the movie recommendation system. This video explains the key functionalities and how to use the API to obtain personalized recommendations.

### Usage Instructions

1. **Clone the repository**:
   ```sh
   git clone https://github.com/tu-usuario/proyecto-recomendacion-peliculas.git
   cd proyecto-recomendacion-peliculas
   ```

2. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the API server**:
   ```sh
   uvicorn app:app --reload
   ```

4. **Access the API**: Once the server is running, you can access the API at `https://pi-henry-zco1.onrender.com`. The interactive documentation is available at `https://pi-henry-zco1.onrender.com/docs`.

### GitHub Repository Access

https://github.com/jessicasandagorda/PIHENRY
