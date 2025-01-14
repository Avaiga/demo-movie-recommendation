from taipy.gui import Gui, notify, Markdown, invoke_long_callback
from concurrent.futures import ThreadPoolExecutor

from algos.algos import clean_title, search, find_similar_movies, ratings
from algos.recommender_algos import process_title, give_recommendations

from pages.user import refresh_user

from cards import create_cards

import ast
import numpy as np
import pandas as pd
import taipy as tp
import time
from api import search_api_film, fetch_api_film, transform_movie_id_to_tmdb_id, fetch_api_in_parallel

movies = pd.read_parquet('data/augmented_movies.parquet')
movies["clean_title"] = movies["title"].apply(clean_title)
movies.index = movies.movieId
movies_for_recommendation = movies[movies['Nb ratings']>=5_000]



searched_film = ""
selected_film = ""
film_selector = []

movie_id = ""

recommended_film = ""
film_recommended_selector = []

options = {"nbinsx": 10}

search_films_md = """
<|container|
<|layout|columns=15px 1fr|
<|image/search.svg|image|width=15px|height=15px|>

<|{searched_film}|input|on_action=search_film|change_delay=-1|label=Search films...|class_name=fullwidth|>
|>

<|part|partial={film_selector_partial}|>

<br/>

<film|part|render={selected_film!=""}|
<|layout|columns=3 7|gap=20px|
<image|
<|{get_poster(selected_film)}|image|width=100%|>

<|Like|button|on_action=on_like|class_name=fullwidth plain|active={movie_id != -1}|>

<|Dislike|button|on_action=on_dislike|class_name=fullwidth plain error|active={movie_id != -1}|>

<|Viewed|button|on_action=on_viewed|class_name=fullwidth plain secondary|active={movie_id != -1}|>
|image>

<description|
<|{get_title(selected_film)}|text|class_name=h2|>

<|{get_description(selected_film)}|text|>

<|part|render={movie_id != -1}|
<br/>
*Unable to find data on the film. This film is not in the database as it is surely too recent.*
|>

<br/>
<|layout|columns=1 1|class_name=text-center|
**Overall**{: .color-primary} ratings: <|{mean_rating(movie_id)}|text|format=%.2f|>/5 <|{int(mean_rating(movie_id)) * '⭐'}|>

Number of **reviews**{: .color-primary}: <|{get_nb_rating(movie_id)}|text|format=%d|>
|>
<br/>

<|{get_rating(movie_id)}|chart|type=histogram|x=Ratings|options={options}|>

<|1 1 1|layout|gap=10px|
<genres|
**Genres**

<|{get_genres(movie_id)}|text|>
|genres>

<Cast|
**Cast**

<|{get_cast(movie_id)}|text|>
|Cast>

<Directors|
**Directors**

<|{get_directors(movie_id)}|text|>
|Directors>
|>

|description>
|>
|film>



## **Recommendation**{: .color-primary}

<|part|partial={recommended_film_selector_partial}|>
|>
"""

page_search = Markdown(search_films_md)


    
def search_film(state):
    query = state.searched_film.replace(" ", "+")
    state.film_selector = search_api_film(query)

"""def search_film(state):
    titles_df = search(state.searched_film).reset_index(drop=True)
    film_selector = [(str(titles_df['movieId'][i]), str(titles_df['title'][i])) for i in range(len(titles_df))]
    state.film_selector = film_selector"""


def recommend_films(state):
    if state.movie_id == "" or state.movie_id is None:
        print("Movie id", state.movie_id, " not found")
        return

    movie_id = int(state.movie_id)
    invoke_long_callback(state,
                         asynchroneous_recommend_films,
                         [movie_id],
                         update_state_after_recommendation,
                         [])


def asynchroneous_recommend_films(movie_id):
    if movie_id == -1:
        print("Movie id", movie_id, " not found")
        return []  

    start = time.time()
    # Define a function to get similar movies with ratings
    def get_similar_movies_with_ratings(movie_id):
        similar_movies_with_ratings = find_similar_movies(movie_id,num_rec=5)
        return [row['movieId'] for _, row in similar_movies_with_ratings.iterrows()]

    # Define a function to get similar movies with bags of words
    def get_similar_movies_with_bags(movie_title):
        movie_bagofwords = process_title(movie_title, movies)
        return list(give_recommendations(movie_bagofwords, 5, movies_for_recommendation))

    # Process similar movies with ratings and bags of words concurrently
    with ThreadPoolExecutor() as executor:
        future_ratings = executor.submit(get_similar_movies_with_ratings, movie_id)
        future_bags = executor.submit(get_similar_movies_with_bags, get_title_from_movie_id(movie_id))
        
        # Wait for the results of both futures
        similar_movies_with_ratings = future_ratings.result()
        similar_movies_with_bags = future_bags.result()
        
    # Combine the results from both processes
    similar_movies = list(set(similar_movies_with_ratings + similar_movies_with_bags))
    similar_movies = similar_movies[:5]

    
    tmdb_ids = [transform_movie_id_to_tmdb_id(id) for id in similar_movies if movie_id != id]
    film_recommended_selector = fetch_api_in_parallel(tmdb_ids)
    print("Time taken for asynchroneous_recommend_films:", time.time() - start)
    return film_recommended_selector

def update_state_after_recommendation(state, status, result):
    # Prepare the state.film_recommended_selector
    state.film_recommended_selector = result
    state.recommended_film_selector_partial.update_content(state, create_cards(state.film_recommended_selector, "w342"))



def get_title_from_movie_id(movie_id):
    return movies.loc[int(movie_id), "title"]

def on_like(state):
    notify(state, 'info', f'♥️ {state.selected_film["original_title"]} liked!')
    user = tp.get(state.scenario_id)
    liked_films = user.liked.read()
    user.liked.write(liked_films+[(state.movie_id, get_title_from_movie_id(state.movie_id))])
    refresh_user(state)


def on_dislike(state):
    notify(state, 'info', f'👎 {state.selected_film["original_title"]} disliked!')
    user = tp.get(state.scenario_id)
    disliked_films = user.disliked.read()
    user.disliked.write(disliked_films+[(state.movie_id, get_title_from_movie_id(state.movie_id))])
    refresh_user(state)

def on_viewed(state):
    notify(state, 'info', f'📽 {state.selected_film["original_title"]} viewed!')
    user = tp.get(state.scenario_id)
    viewed_films = user.viewed.read()
    user.viewed.write(viewed_films+[(state.movie_id, get_title_from_movie_id(state.movie_id))])
    refresh_user(state)

def get_title(selected_film):
    return selected_film["original_title"] if selected_film and "original_title" in list(selected_film.keys()) is not None else ''

def get_poster(selected_film):
    try:
        return "http://image.tmdb.org/t/p/w500" + selected_film["poster_path"] if selected_film and "poster_path" in list(selected_film.keys()) is not None else ''
    except:
        return ''

def get_rating(movie_id):
    try:
        if int(movie_id) in ratings["movieId"].unique():
            return {"Ratings" : list(ratings[ratings["movieId"] == int(movie_id)]["rating"])}
        else:
            return {"Ratings" : [0,1,2]}
    except Exception as e:
        print(movie_id, e)
        return  {"Ratings" : [0,1,2]}

def get_nb_rating(movie_id):
    try:
        return int(movies.loc[int(movie_id), 'Nb ratings'])
    except:
        return 0

def mean_rating(movie_id):
    try:
        return movies.loc[int(movie_id), 'rating']
    except:
        return 0
    
def get_description(selected_film):
    try:
        return selected_film["overview"] if "overview" in list(selected_film.keys()) is not None else ''
    except:
        return ''
    
def get_genres(movie_id):
    try:
        genres = movies.loc[int(movie_id), 'genres']
        if isinstance(genres, str):
            return ', '.join(ast.literal_eval(genres))
        else:
            return ', '.join(genres)
    except:
        return ''
    
def get_cast(movie_id):
    try:
        cast = movies.loc[int(movie_id), 'leadCast']
        if isinstance(cast, str):
            return ', '.join(ast.literal_eval(cast))
        else:
            return ', '.join(cast)
    except:
        return ''
    
def get_directors(movie_id):
    try:
        directors = movies.loc[int(movie_id), 'directors']
        if isinstance(directors, str):
            return ', '.join(ast.literal_eval(directors))
        else:
            return ', '.join(directors)
    except:
        return ''