import concurrent.futures
import requests
from bs4 import BeautifulSoup
import ast
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from rake_nltk import Rake



MOVIE_FILE = 'data/movies.csv'
LINKS_FILE = 'data/links.csv'
OUTPUT_FILE = 'data/augmented_movies.csv'
ratings = pd.read_csv('data/ratings.csv')


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



def get_imdb_movie_data(imdb_id):
    '''given a single movie IMDB id this function gets its description, director and lead cast from IMDB'''
    web_address = 'https://www.imdb.com/title/tt{0:07d}/'.format(imdb_id)
    description = ''
    director = ''
    lead_cast = ''
    try:
        res = requests.get(web_address, headers={'User-Agent': 'Mozilla/5.0'})
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            description = soup.find("span", {"data-testid": "plot-xs_to_m"}).getText()
            metadata = soup.find_all("li", {"data-testid": "title-pc-principal-credit"})
            
            director = []
            lead_cast = []
            for element in metadata:
                if 'Director' in element.contents[0].getText():
                    for item in element.contents[1].contents[0]:
                        if item.getText() not in director:
                            director.append(item.getText())
                if 'Stars' in element.contents[0].getText():
                    for item in element.contents[1].contents[0]:
                        if item.getText() not in lead_cast:
                            lead_cast.append(item.getText())
            # if no director or lead cast the function returns them as emty lists which 
            # works for the current content recommender, so we might not need next if statement
            if len(metadata) == 0:
                print(f'{imdb_id} metadata not found')
            if (len(director) == 0) or (len(lead_cast) == 0):
                print(f'{imdb_id} info is missing') 
    except Exception as err:
        print(f"{imdb_id} error", err)
        description = ''
        director = []
        lead_cast = []
    
    return description, director, lead_cast

def get_all_movies_imdb_data(df):
    '''collect IMDB data for ALL movies in the dataframe'''
    descriptions = []
    directors = []
    lead_casts = []

    def process_row(row):
        print(f"| {row.movieId} |")
        imdb_id = links_df.loc[links_df.movieId == row.movieId, 'imdbId'].iloc[0]
        x, y, z = get_imdb_movie_data(imdb_id)
        return x, y, z

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_row, df.itertuples()))

    descriptions, directors, lead_casts = zip(*results)
    return descriptions, directors, lead_casts


def augment_data(df):
    '''add IMDB data to the dataframe'''
    arr1, arr2, arr3 = get_all_movies_imdb_data(df)
    description = pd.Series(arr1)
    directors = pd.Series(arr2)
    lead_cast = pd.Series(arr3)
    new_df = pd.concat([df, description, directors, lead_cast], axis=1)
    new_df.rename(columns={0: 'description', 1: 'directors', 2: 'leadCast'}, inplace=True)

    return new_df


def extract_keywords(text):
    '''this function extracts keywords from movie description using nltk Rake'''
    r = Rake()

    r.extract_keywords_from_text(text)

    # getting the dictionary whith key words as keys and their scores as values
    key_words_dict_scores = r.get_word_degrees()
   
    key_words = list(key_words_dict_scores.keys())
    return key_words


def transform_df(old_df):
    '''this function transforms the dataframe into a dataframe with 2 columns: movie title and bag of words'''
    new_df = old_df.copy()
    new_df['genres'] = new_df['genres'].map(lambda x: x.split('|'))
    new_df["description"] = new_df['description'].fillna("")
    new_df['keywords'] = new_df['description'].map(extract_keywords)
    new_df['directors'] = new_df['directors'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) or not np.isnan(x) else [])
    new_df['leadCast'] = new_df['leadCast'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) or not np.isnan(x) else [])
    new_df['Bagofwords'] = new_df.genres + new_df.directors + new_df.leadCast + new_df.keywords
    new_df['Bagofwords'] = new_df['Bagofwords'].map(lambda x: ' '.join(x) if isinstance(x, list) else x)    
    return new_df


if __name__ == '__main__': 
    df = pd.read_csv(MOVIE_FILE)
    links_df = pd.read_csv(LINKS_FILE)
    #augmented_data = augment_data(df)
    #augmented_data.to_csv('temp.csv', index=False)
    #augmented_data = pd.read_csv('temp.csv')
    #augmented_data = transform_df(augmented_data)
    #augmented_data.to_csv(OUTPUT_FILE, index=False)
    #augmented_data = pd.read_csv(OUTPUT_FILE)
    #ratings['Nb ratings'] = [1] * len(ratings)
    #nb_ratings = ratings.groupby('movieId')['Nb ratings'].sum().reset_index()
    #mean_ratings = ratings.groupby('movieId')['rating'].mean().reset_index()

    #augmented_data = pd.merge(augmented_data, mean_ratings, on='movieId')
    #augmented_data = pd.merge(augmented_data, nb_ratings, on='movieId')
    #augmented_data.to_csv("temp.csv", index=False)
    #pd.read_csv('data/augmented_movies.csv').to_parquet('data/augmented_movies.parquet')
    import dask.dataframe as da

    save_dir = 'data/ratings'
    ratings = pd.read_csv('data/ratings.csv')
    ddf = da.from_pandas(ratings, chunksize=5000000)
    ddf.to_parquet(save_dir)
    print("finished")




