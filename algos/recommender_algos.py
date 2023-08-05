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
    movie_bag = movie_df[movie_df.title == title]['Bagofwords'].values[0]
    return movie_bag

def give_recommendations(movie_bagofwords, num_rec, movie_df):
    '''given a movie bag_of_words and the desired number of recommendations, this function returns an array of recommended movie titles'''
    

    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(movie_df['Bagofwords'])
    count_array = count_matrix.toarray()
    count_df = pd.DataFrame(data=count_array,columns = vectorizer.get_feature_names_out())

    v = vectorizer.transform([movie_bagofwords])
    cos_sim = cosine_similarity(count_df,v)
    cos_sim  = cos_sim.flatten()
    sorted_cos_sim = np.argsort(cos_sim)
    reverse_sorted = sorted_cos_sim[::-1]
    rec_indices = reverse_sorted[:int(num_rec)]
    idx = list(count_df.iloc[rec_indices,0].index)
    recommendations = movie_df.iloc[idx,:].reset_index(drop=True)
    recommendations = [recommendations['movieId'][i] for i in range(len(recommendations))]
    return recommendations


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        print("Usage: function requires a movie title, number of desired recommendations, movie database file name, and the top 1000 IMDB movie file")
        sys.exit()

    
    MOVIE_TITLE = sys.argv[1]
    NUM_REC = sys.argv[2]
    MOVIE_FILE = sys.argv[3]
    TOP_1000_FILE = sys.argv[4]


    movie_df = pd.read_csv(MOVIE_FILE)
    movie_recommendations = give_recommendations(MOVIE_TITLE, NUM_REC)#
    print(movie_recommendations)