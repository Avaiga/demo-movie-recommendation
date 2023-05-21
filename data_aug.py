import sys
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


MOVIE_FILE = '../Downloads/ml-25m/xsmall_movies.csv'
LINKS_FILE = '../Downloads/ml-25m/links.csv'
OUTPUT_FILE = '../Downloads/ml-25m/augmented_movies.csv'


def get_imdb_movie_data(imdb_id):
    '''given a single movie IMDB id this function gets its description, director and lead cast from IMDB'''
    web_address = 'https://www.imdb.com/title/tt{0:07d}/'.format(imdb_id)
    res = requests.get(web_address, headers={'User-Agent': 'Mozilla/5.0'})
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        description = soup.find("span", {"data-testid": "plot-xs_to_m"}).getText()
        if not description:
            print(f'{imdb_id} description not found')
        metadata = soup.find_all("li", {"data-testid": "title-pc-principal-credit"})
        if len(metadata) == 0:
            print(f'{imdb_id} metadata not found')
        director = []
        lead_cast = []
        for element in metadata:
            if 'Director' in element.contents[0].getText():
                for item in element.contents[1].contents[0]:
                    if item.getText() not in director:
                        director.append(item.getText())
            if 'Stars' in element.contents[0].getText():
                for item in element.contents[1].contents[0]:
                    lead_cast.append(item.getText())
        if (len(director) == 0) or (len(lead_cast) == 0):
            print(f'{imdb_id} info is missing')
        return description, director, lead_cast
    else:
        print(f"problem finding website for movie {imdb_id}") 
        return None, None, None  
    

def get_all_movies_imdb_data(df):
    '''collect IMDB data for ALL movies in the dataframe'''
    descriptions = []
    directors = []
    lead_casts = []
    for i, row in df.iterrows():
        imdb_id = links_df.loc[links_df.movieId == row.movieId].imdbId.values[0]
        x, y, z = get_imdb_movie_data(imdb_id)
        descriptions.append(x)
        directors.append(y)
        lead_casts.append(z)

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

if __name__ == '__main__': 
    if len(sys.argv) != 4:
        print("Usage: function requires a movie file, links file, and the output file name")
        sys.exit()

    MOVIE_FILE = sys.argv[1]
    LINKS_FILE = sys.argv[2]
    OUTPUT_FILE = sys.argv[3]
    df = pd.read_csv(MOVIE_FILE)
    links_df = pd.read_csv(LINKS_FILE)
    augmented_data = augment_data(df)
    augmented_data.to_csv(OUTPUT_FILE)

