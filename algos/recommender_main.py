import pandas as pd

import taipy as tp 
from taipy import Config

### recommender_data
MOVIES_FILE = 'data/augmented_small_movies.csv'
TOP_1000_FILE = 'data/IMDB_top_1000.csv'

movie_df = pd.read_csv(MOVIES_FILE)
top_1000_df = pd.read_csv(TOP_1000_FILE)

Config.load("config/config_recommender.toml")
scenario_cfg = Config.scenarios['scenario']

if __name__ == "__main__":
    # run Taipy Core
    tp.Core().run()

    # create my scenario
    scenario = tp.create_scenario(scenario_cfg)
    tp.submit(scenario)
    print("We recommend:", scenario.recommendations.read())