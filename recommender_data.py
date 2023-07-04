import pandas as pd

MOVIES_FILE = '../Downloads/ml-25m/augmented_small_movies.csv'
TOP_1000_FILE = '../Downloads/ml-25m/IMDB_top_1000.csv'

movie_df = pd.read_csv(MOVIES_FILE)
top_1000_df = pd.read_csv(TOP_1000_FILE)
