import pandas as pd
from api import search_api_film, fetch_api_film, transform_movie_id_to_tmdb_id, fetch_api_in_parallel
from cards import create_cards

from taipy.gui import Markdown

import taipy as tp
import time

from algos.recommender_algos import process_title, give_recommendations
from algos.algos import recommend_films_to_user


movies = pd.read_parquet('data/augmented_movies.parquet')
movies.index = movies.movieId

selected_user_liked = None
user_liked = []

selected_user_disliked = None
user_disliked = []

selected_user_viewed = None
user_viewed = []

selected_recommended_content = ""
content_selector = []

page_user = Markdown("""
<|part|class_name=container|
#  Similar to the **movies you liked**{: .color-primary} 
<|part|partial={content_selector_partial}|>

<|layout|columns=1 1 1|
<liked|
## ♥️ Liked

<|{selected_user_liked}|selector|lov={user_liked}|width=fit-content|>
|liked>

<disliked|
## 👎 Disliked

<|{selected_user_disliked}|selector|lov={user_disliked}|width=fit-content|>
|disliked>

<viewed|
## 📽️ Viewed

<|{selected_user_viewed}|selector|lov={user_viewed}|width=fit-content|>
|viewed>
|>


|>
""")


def asynchroneous_recommend_content_user(scenario_id):
    start = time.time()
    user = tp.get(scenario_id)
    
    # Read liked, disliked, and viewed movies from the user data
    liked = user.liked.read()
    liked_titles = [movie[1] for movie in liked]
    
    disliked = user.disliked.read()
    disliked_titles = [movie[1] for movie in disliked]
    
    viewed = user.viewed.read()
    viewed_titles = [movie[1] for movie in viewed]
    
    # Get recommended movies based on liked, disliked, and viewed titles
    recommended_movies = recommend_films_to_user(liked_titles, disliked_titles, viewed_titles)
    
    # Filter out already liked, disliked, or viewed movies
    liked_ids = {movie[0] for movie in liked}
    disliked_ids = {movie[0] for movie in disliked}
    viewed_ids = {movie[0] for movie in viewed}
    
    # Create a list of (movie_id, movie_title) tuples for recommended movies
    tmdb_ids = [transform_movie_id_to_tmdb_id(movie_id) for movie_id in recommended_movies]
    tmdb_ids = [tmdb_id for tmdb_id in tmdb_ids 
                        if tmdb_id not in liked_ids and tmdb_id not in disliked_ids and tmdb_id not in viewed_ids]
    return_statement = fetch_api_in_parallel(tmdb_ids)
    print(f"Execution time for asynchroneous_recommend_content_user: {time.time() - start}")
    return return_statement
    
def update_state_after_recommendation(state, status, result):
    # Update the state with the new content selector list
    state.content_selector = result
    state.content_selector_partial.update_content(state, create_cards(state.content_selector, "w342", prerender=True))

    state.content_selector_partial.update_content(state, create_cards(state.content_selector, "w342"))




def refresh_user(state):
    user = tp.get(state.scenario_id)
    state.user_liked = user.liked.read()
    state.user_disliked = user.disliked.read()
    state.user_viewed = user.viewed.read()