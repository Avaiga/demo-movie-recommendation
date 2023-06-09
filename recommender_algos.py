import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from rake_nltk import Rake

def extract_keywords(text):
    '''this function extracts keywords from movie description using nltk Rake'''
    r = Rake()

    r.extract_keywords_from_text(text)

    # getting the dictionary whith key words as keys and their scores as values
    key_words_dict_scores = r.get_word_degrees()
   
    key_words = list(key_words_dict_scores.keys())
    
    return key_words

def process_title(title, movie_df):
    '''this function, given a movie title, retrieves movie info from the movie database, and outputs it as a string to be processed by the vectorizer '''
    idx = movie_df['title'].str.contains(title, case=False)
    if max(idx.values):
        title = movie_df['title'][idx].values[0]
    else:
      print('Please give a different movie title')

    genre = movie_df[movie_df.title == title]['genres'].values[0].replace('|', ' ').lower()

    director = movie_df[movie_df.title == title]['directors'].values[0].replace('[', '').replace(']', '').lower()
    director = director.split(',')
    new_dir = []
    for el in director:
        el = el.replace("'", '')
        el = el.replace(' ', '')
        new_dir.append(el)
    director = ' '.join(new_dir)
    
    cast = movie_df[movie_df.title == title]['leadCast'].values[0].replace('[','').replace(']', '').lower()
    cast = cast.split(',')
    new_cast = []
    for el in cast:
        el = el.replace("'", '')
        el = el.replace(' ','')
        new_cast.append(el)
    cast = ' '.join(new_cast)

    keywords = extract_keywords(movie_df[movie_df.title == title]['description'].values[0].lower())
    keywords = ' '.join(keywords)

    movie_bag = genre + director + cast + keywords

    return movie_bag

def give_recommendations(movie_bagofwords, num_rec, top_1000_df):
    '''given a movie bag_of_words and the desired number of recommendations, this function returns an array of recommended movie titles'''
    

    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(top_1000_df['Bagofwords'])
    count_array = count_matrix.toarray()
    count_df = pd.DataFrame(data=count_array,columns = vectorizer.get_feature_names_out())
    count_df.insert(0, 'Title', top_1000_df['Title'])

    v = vectorizer.transform([movie_bagofwords])
    cos_sim = cosine_similarity(count_df.iloc[:,1:],v)
    cos_sim  = cos_sim.flatten()
    sorted_cos_sim = np.argsort(cos_sim)
    reverse_sorted = sorted_cos_sim[::-1]
    rec_indices = reverse_sorted[:int(num_rec)]
    recommendations = count_df.iloc[rec_indices,0]

    return recommendations