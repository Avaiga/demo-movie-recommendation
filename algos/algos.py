import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from algos.recommender_algos import process_title, give_recommendations

def dumb(a,b,c):
    recommended_content = []
    if len(a) > 0:
        all_film_bag = ''
        for film in a:
            film_bag = process_title(film, movies)
            all_film_bag = all_film_bag + ' ' + film_bag

        recs = give_recommendations(all_film_bag, 30, IMDB_top_1000)
        for rec in recs:
            if (b.count(rec) == 0) and (c.count(rec) == 0):
                recommended_content.append(rec)
            if len(recommended_content) >= 10:
                break
    return recommended_content

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

def search(title):
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    print(results)
    return results

def get_rating(movie_id):
    try:
        if int(movie_id) in ratings["movieId"].unique():
            return {"Ratings" : list(ratings[ratings["movieId"] == int(movie_id)]["rating"])}
        else:
            return {"Ratings" : [0,1,2]}
    except Exception as e:
        print(movie_id, e)
        return  {"Ratings" : [0,1,2]}


def mean_rating(selected_film):
    return float(np.mean(get_rating(selected_film)['Ratings']))

def find_similar_movies(movie_id):
    similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
    similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]


vectorizer = TfidfVectorizer(ngram_range=(1,2))
#movie_id = 89745

ratings = pd.read_csv('../Downloads/ml-25m/ratings.csv')
IMDB_top_1000 = pd.read_csv("../Downloads/ml-25m/IMDB_top_1000.csv")

movies = pd.read_csv('../Downloads/ml-25m/augmented_small_movies.csv')

#ratings = pd.read_csv('data/ratings.csv')
#IMDB_top_1000 = pd.read_csv("data/IMDB_top_1000.csv")

#movies = pd.read_csv('data/augmented_small_movies.csv')
movies["clean_title"] = movies["title"].apply(clean_title)
tfidf = vectorizer.fit_transform(movies["clean_title"])

#print(search('Avengers'))
#start=time.time()
#print(find_similar_movies(movie_id))
#print(time.time()-start)
