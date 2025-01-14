import requests
import pandas as pd
import time
import concurrent.futures

api_key = "15d2ea6d0dc1d476efbca3eba2b9bbfb"

links_tmdbId = pd.read_csv('data/links.csv')
links_tmdbId.dropna(inplace=True)
links_tmdbId.index = links_tmdbId.tmdbId.astype(int)
links_movieId = pd.read_csv('data/links.csv')
links_movieId.index = links_movieId.movieId.astype(int)


def fetch_api_in_parallel(tmdb_ids):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_api_film, tmdb_ids)
        return list(results)

def fetch_api_film(tmdb_id):
    start = time.time()
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?language=en-US&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        if results:
            print(f"Data fetched in {time.time() - start:.2f} seconds.")
            return results
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def search_api_film(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        if results and 'results' in results:
            return results['results']
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None
    

def transform_tmdb_id_to_movie_id(tmdb_id):
    try:
        movie_id = links_tmdbId.loc[int(tmdb_id), 'movieId']
    except:
        movie_id = -1
    return str(int(movie_id))

def transform_movie_id_to_tmdb_id(movie_id):
    tmdb_id = links_movieId.loc[int(movie_id), 'tmdbId']
    return int(tmdb_id)

if __name__ == '__main__':
    tmdb_id = 8966
    movie_id = transform_tmdb_id_to_movie_id(tmdb_id)
    tmdb_id_retransformed = transform_movie_id_to_tmdb_id(movie_id)
    print(fetch_api_film(tmdb_id_retransformed))
    print(tmdb_id)
    print(movie_id)
    print(tmdb_id_retransformed)
