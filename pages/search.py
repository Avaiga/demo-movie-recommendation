from taipy.gui import Gui, notify, Markdown

from algos.algos import clean_title, search, find_similar_movies, ratings

from algos.recommender_algos import process_title, give_recommendations

from concurrent.futures import ThreadPoolExecutor


from algos.recommender_algos import process_title, give_recommendations

from pages.user import refresh_user

import numpy as np
import pandas as pd
import taipy as tp


movies = pd.read_parquet('data/augmented_movies.parquet')
movies["clean_title"] = movies["title"].apply(clean_title)
movies.index = movies.movieId
movies_for_recommendation = movies[movies['Nb ratings']>=5_000]


searched_film = ""
selected_film = ("","")
film_selector = [('','')]

recommended_film = ""
film_recommended_selector = [('','')]

options = {"nbinsx": 10}

search_films_md = """
<|container|

<|layout|columns=1 3 1|
<Search|
## Search **films**{: .color-primary}
<|{searched_film}|input|on_change=search_film|label=Search films...|>
<|{selected_film}|selector|lov={film_selector}|on_change=recommend_films|>
|Search>

<Description|part|render={selected_film[0]!=""}|
# **Description**{: .color-primary} of films
<|ca#rd|
<|layout|columns=1 1|
<ratings|
<br/>
**Overall**{: .color-primary} ratings: <|{mean_rating(selected_film[0])}|text|format=%.2f|>/5 <|{int(mean_rating(selected_film[0])) * '⭐'}|>

Number of **reviews**{: .color-primary}: <|{get_nb_rating(selected_film[0])}|text|format=%d|>

<br/>
|ratings>

<button|
<br/>
<| ♥️  Like|button|on_action=on_like|>
<| 👎  Dislike|button|on_action=on_dislike|>
<| 📽️  Viewed|button|on_action=on_viewed|>
<br/>
|button>
|>

**Description**

<|{get_description(selected_film[0])}|text|>

**Genres**

<|{get_genres(selected_film[0])}|text|>


<|{get_rating(selected_film[0])}|chart|type=histogram|x=Ratings|options={options}|>
|>
|Description>


<|part|
## **Recommended**{: .color-primary} films
<|{recommended_film}|selector|lov={film_recommended_selector}|value_by_id|on_change=recommend_films|width=fit_content|>
|>
|>
|>
"""

page_search = Markdown(search_films_md)


def search_film(state):
    titles_df = search(state.searched_film).reset_index(drop=True)
    film_selector = [(str(titles_df['movieId'][i]), str(titles_df['title'][i])) for i in range(len(titles_df))]
    state.film_selector = film_selector


def recommend_films(state):
    movie_id = int(state.selected_film[0])

    # Define a function to get similar movies with ratings
    def get_similar_movies_with_ratings(movie_id):
        similar_movies_with_ratings = find_similar_movies(movie_id)
        return [row['movieId'] for _, row in similar_movies_with_ratings.iterrows()]

    # Define a function to get similar movies with bags of words
    def get_similar_movies_with_bags(movie_title):
        movie_bagofwords = process_title(movie_title, movies)
        return list(give_recommendations(movie_bagofwords, 5, movies_for_recommendation))

    # Process similar movies with ratings and bags of words concurrently
    with ThreadPoolExecutor() as executor:
        future_ratings = executor.submit(get_similar_movies_with_ratings, movie_id)
        future_bags = executor.submit(get_similar_movies_with_bags, state.selected_film[1])
        
        # Wait for the results of both futures
        similar_movies_with_ratings = future_ratings.result()
        similar_movies_with_bags = future_bags.result()
        
    # Combine the results from both processes
    similar_movies = list(set(similar_movies_with_ratings + similar_movies_with_bags))

    # Prepare the state.film_recommended_selector
    state.film_recommended_selector = [(str(movie_id), movies.loc[movie_id, "title"]) for movie_id in similar_movies]


def on_like(state):
    notify(state, 'info', f'♥️ {state.selected_film[1]} liked!')
    user = tp.get(state.scenario_id)
    liked_films = user.liked.read()
    user.liked.write(liked_films+[state.selected_film])
    refresh_user(state)


def on_dislike(state):
    notify(state, 'info', f'👎 {state.selected_film[1]} disliked!')
    user = tp.get(state.scenario_id)
    disliked_films = user.disliked.read()
    user.disliked.write(disliked_films+[state.selected_film])
    refresh_user(state)

def on_viewed(state):
    notify(state, 'info', f'📽 {state.selected_film[1]} viewed!')
    user = tp.get(state.scenario_id)
    viewed_films = user.viewed.read()
    user.viewed.write(viewed_films+[state.selected_film])
    refresh_user(state)



def get_rating(movie_id):
    try:
        if int(movie_id) in ratings["movieId"].unique():
            return {"Ratings" : list(ratings[ratings["movieId"] == int(movie_id)]["rating"])}
        else:
            return {"Ratings" : [0,1,2]}
    except Exception as e:
        print(movie_id, e)
        return  {"Ratings" : [0,1,2]}

def get_nb_rating(selected_film):
    try:
        return int(movies.loc[int(selected_film), 'Nb ratings'])
    except:
        return 0

def mean_rating(selected_film):
    try:
        return movies.loc[int(selected_film), 'rating']
    except:
        return 0
    
def get_description(selected_film):
    try:
        return movies.loc[int(selected_film), 'description']
    except:
        return ''
    
def get_genres(selected_film):
    try:
        return movies.loc[int(selected_film), 'genres']
    except:
        return ''