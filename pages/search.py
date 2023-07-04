from taipy.gui import Gui, notify, Markdown

from algos.algos import clean_title, search, find_similar_movies, get_rating, mean_rating

from pages.user import refresh_user

import numpy as np
import pandas as pd
import taipy as tp

#movies = pd.read_csv("data/movies.csv")
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
<|{searched_film}|input|on_change=search_film|label=Search films...|width=fit_content|>

<|{selected_film}|selector|lov={film_selector}|on_change=recommend_films|width=fit_content|>
|>
|>
"""

description_films_md = """
<|part|class_name=container|
<Description|part|render={selected_film[0]!=""}|
## **Description**{: .color_primary} of films
<card|part|class_name=card|
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
|card>
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
    recommended_movies = find_similar_movies(movie_id)
    state.film_recommended_selector = list(recommended_movies['title'])[:5]


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