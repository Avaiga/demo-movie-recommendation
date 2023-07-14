from taipy.gui import Gui, notify, Markdown

from algos.algos import clean_title, search, find_similar_movies, get_rating, mean_rating

from algos.recommender_algos import process_title, give_recommendations

from pages.user import refresh_user

import numpy as np
import pandas as pd
import taipy as tp

#movies = pd.read_csv("data/movies.csv")
#movies = pd.read_csv('data/augmented_small_movies.csv')
IMDB_top_1000 = pd.read_csv('../Downloads/ml-25m/IMDB_top_1000.csv')
movies = pd.read_csv('../Downloads/ml-25m/augmented_small_movies.csv')
movies["clean_title"] = movies["title"].apply(clean_title)


searched_film = ""
selected_film = ("","")
film_selector = [('','')]

recommended_film = ""
film_recommended_selector = [('','')]

options = {"nbinsx": 10}

search_films_md = """
<|part|class_name=container|
# Search **films**{: .color_primary}

<|layout|columns=1 1|
<|{searched_film}|input|on_change=search_film|label=Search films...|>

<|{selected_film}|selector|lov={film_selector}|on_change=recommend_films|>
|>
|>
"""

description_films_md = """
<|container|
<Description|part|render={selected_film[0]!=""}|
## **Description**{: .color_primary} of films
<|card|
<|layout|columns=1 1|
<ratings|
<br/>
**Overall**{: .color_primary} ratings: <|{mean_rating(selected_film[0])}|text|format=%.2f|>/5 <|{round(mean_rating(selected_film[0])) * '⭐'}|>

Number of **reviews**{: .color_primary}: <|{len(get_rating(selected_film[0])['Ratings'])}|text|format=%d|>

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

<|{get_rating(selected_film[0])}|chart|type=histogram|x=Ratings|options={options}|>
|>
|Description>
|>
"""

recommend_films_md = """
<|part|class_name=container|
# **Recommended**{: .color_primary} films
<|{recommended_film}|selector|lov={film_recommended_selector}|value_by_id|on_change=recommend_films|width=fit_content|>
|>
"""

page_search = Markdown(search_films_md+description_films_md+recommend_films_md)


def search_film(state):
    titles_df = search(state.searched_film).reset_index(drop=True)
    film_selector = [(str(titles_df['movieId'][i]), str(titles_df['title'][i])) for i in range(len(titles_df))]
    state.film_selector = film_selector


def recommend_films(state):
    movie_id = int(state.selected_film[0])
    recommended_movies_1 = find_similar_movies(movie_id)
    all_recommended_movies = list(recommended_movies_1['title'])[:5]
    movie_title = state.selected_film[1]
    movie_bagofwords = process_title(movie_title, movies)
    recommended_movies_2 = list(give_recommendations(movie_bagofwords, 7, IMDB_top_1000))
    for movie in recommended_movies_2:
        if movie not in all_recommended_movies:
            all_recommended_movies.append(movie)
    
    state.film_recommended_selector = all_recommended_movies


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