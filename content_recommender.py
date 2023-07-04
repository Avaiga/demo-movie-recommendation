import sys
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from rake_nltk import Rake

MOVIES_FILE = '../Downloads/ml-25m/augmented_small_movies.csv'
TOP_1000_FILE = '../Downloads/ml-25/IMDB_top_1000.csv'
#movie_title = 'Waiting to Exhale'
#num_rec = 10
def extract_keywords(text):
    '''this function extracts keywords from movie description using nltk Rake'''
    r = Rake()

    r.extract_keywords_from_text(text)

    # getting the dictionary whith key words as keys and their scores as values
    key_words_dict_scores = r.get_word_degrees()
   
    key_words = list(key_words_dict_scores.keys())
    
    return key_words
    
def process_title(title):
    '''this function, given a movie title, retrieves movie info from the movie database file, and outputs it as a string to be processed by the vectorizer '''
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

def give_recommendations(title, num_rec):
    '''given a movie title and the desired number of recommendations, this function returns an array of recommended movie titles'''
    idx = movie_df['title'].str.contains(title, case=False)
    if max(idx.values):
        title = movie_df['title'][idx].values[0]
        movie_bagofwords = process_title(title)
    else:
      print('Please give a different movie title')

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

if __name__ == '__main__': 
    if len(sys.argv) != 5:
        print("Usage: function requires a movie title, number of desired recommendations, movie database file name, and the top 1000 IMDB movie file")
        sys.exit()

    
    MOVIE_TITLE = sys.argv[1]
    NUM_REC = sys.argv[2]
    MOVIE_FILE = sys.argv[3]
    TOP_1000_FILE = sys.argv[4]

    movie_df = pd.read_csv(MOVIE_FILE)
    top_1000_df = pd.read_csv(TOP_1000_FILE)
    movie_recommendations = give_recommendations(MOVIE_TITLE, NUM_REC)#
    print(movie_recommendations)
