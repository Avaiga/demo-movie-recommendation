import sys
import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

import nltk
from rake_nltk import Rake

OUTPUT_FILE = '../Downloads/ml-25m/IMDB_top_1000.csv'

WEB_ADDRESS_0 = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'
WEB_ADDRESS_1 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=101&ref_=adv_nxt'
WEB_ADDRESS_2 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=201&ref_=adv_nxt'
WEB_ADDRESS_3 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=301&ref_=adv_nxt'
WEB_ADDRESS_4 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=401&ref_=adv_nxt'
WEB_ADDRESS_5 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=501&ref_=adv_nxt'
WEB_ADDRESS_6 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=601&ref_=adv_nxt'
WEB_ADDRESS_7 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=701&ref_=adv_nxt'
WEB_ADDRESS_8 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=801&ref_=adv_nxt'
WEB_ADDRESS_9 = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=901&ref_=adv_nxt'
WEB_ADDRESSES = [WEB_ADDRESS_0,WEB_ADDRESS_1,WEB_ADDRESS_2,WEB_ADDRESS_3,WEB_ADDRESS_4,WEB_ADDRESS_5,WEB_ADDRESS_6,
                 WEB_ADDRESS_7,WEB_ADDRESS_8,WEB_ADDRESS_9]

def get_100(web_address):
    '''this function takes an IMDB top 1000 web address, and for each movie scrapes title, genre, description, director and cast. It outputs 5 arrays with this information for 100 movies on the page'''
    titles = []
    genres = []
    directors = []
    casts = []
    descriptions = []
    try:
        res = requests.get(web_address, headers={'User-Agent': 'Mozilla/5.0'})
    except requests.exceptions.RequestException as err:
        print("requests exception found", err)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        one_100 = soup.find_all("div", {"class": "lister-item-content"})
        for item in one_100:
            title = item.h3.getText().strip().split('\n')
            title = title[1:]
            title = ' '.join(title)
            titles.append(title)
            genre = item.find("span", {"class": "genre"}).getText().strip().replace('\n', '')
            genres.append(genre)
            description = item.find_all("p")[1].getText().replace('\n', '')
            descriptions.append(description)
            data = item.find("p", {"class": ""}).getText()
            director, cast = data.split('|')
            director = director.split(':')[1].replace('\n', '')
            cast = cast.split(':')[1].replace('\n', '')
            directors.append(director)
            casts.append(cast)
            
        return titles, genres, descriptions, directors, casts

def build_df(web_addresses):
    '''this function concatenates the information from 10 webpages into one pandas dataframe'''
    data = []
    for i in range(len(WEB_ADDRESSES)):
        titles, genres, descriptions, directors, casts = get_100(web_addresses[i])
        titles = pd.Series(titles)
        genres = pd.Series(genres)
        descriptions = pd.Series(descriptions)
        directors = pd.Series(directors)
        cast = pd.Series(casts)
        dataframe = pd.concat([titles, genres, descriptions, directors, cast], axis=1)
        dataframe.rename(columns={0: 'Title', 1: 'Genre', 2: 'Description', 3: 'Director', 4: 'Cast'}, inplace=True)
        data.append(dataframe)
        
    dataframe = pd.concat(data, ignore_index=True)
    return dataframe

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
    old_df['Genre'] = old_df['Genre'].map(lambda x: x.replace(' ',''))
    old_df['Genre'] = old_df['Genre'].map(lambda x: x.lower().split(','))
    old_df['Director'] = old_df['Director'].map(lambda x: x.replace(' ',''))
    old_df['Director'] = old_df['Director'].map(lambda x: x.lower().split(','))
    old_df['Cast'] = old_df['Cast'].map(lambda x: x.replace(' ',''))
    old_df['Cast'] = old_df['Cast'].map(lambda x: x.lower().split(','))
    old_df['Keywords'] = old_df['Description'].map(extract_keywords)
    old_df['Bagofwords'] = old_df.Genre + old_df.Director + old_df.Cast + old_df.Keywords
    old_df['Bagofwords'] = old_df['Bagofwords'].map(lambda x: ' '.join(x))
    new_df = old_df.drop(columns=['Genre', 'Description', 'Director', 'Cast', 'Keywords'])
    
    return new_df
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: function requires an output file name")
        sys.exit()
    df = build_df(WEB_ADDRESSES)
    transformed_df = transform_df(df)
    transformed_df.to_csv(OUTPUT_FILE, index=False)
             