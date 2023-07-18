import pandas as pd

from taipy.gui import Gui, notify, Markdown

import taipy as tp

from algos.recommender_algos import process_title, give_recommendations
from algos.algos import dumb

#IMDB_top_1000 = pd.read_csv("data/IMDB_top_1000.csv")
#movies = pd.read_csv('data/augmented_small_movies.csv')
IMDB_top_1000 = pd.read_csv("../Downloads/ml-25m/IMDB_top_1000.csv")
movies = pd.read_csv('../Downloads/ml-25m/augmented_small_movies.csv')

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
<|🔄 Refresh|button|on_action=refresh_user|>

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

<|part|class_name=container|
#  Similar to the **movies you liked**{: .color_primary} 
<| Recommend|button|on_action=recommend_content_user|>
<|{selected_recommended_content}|selector|lov={content_selector}|width=fit_content|>
|>

|>
""")

def recommend_content_user(state):
    #movie_title = state.selected_user_liked[1]
    #movie_bagofwords = process_title(movie_title, movies)
    #recommended_movies = give_recommendations(movie_bagofwords, 7, IMDB_top_1000)
    user = tp.get(state.scenario_id)
    liked = user.liked.read()
    liked_titles = [movie[1] for movie in liked]
    disliked = user.disliked.read()
    disliked_titles = [movie[1] for movie in disliked]
    viewed = user.viewed.read()
    viewed_titles = [movie[1] for movie in viewed]
    recommended_movies = dumb(liked_titles, disliked_titles, viewed_titles)
    state.content_selector = recommended_movies


def refresh_user(state):
    user = tp.get(state.scenario_id)
    state.user_liked = user.liked.read()
    state.user_disliked = user.disliked.read()
    state.user_viewed = user.viewed.read()