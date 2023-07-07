import taipy as tp 
from taipy import Config, Scope

from recommender_algos import process_title, give_recommendations

# Data Node configuration
augmented_movie_cfg = Config.configure_data_node(id="augmented_movies_dataset",
storage_type="csv",
path="../Downloads/ml-25m/augmented_small_movies.csv",
scope=Scope.GLOBAL)

imdb_top_1000_cfg = Config.configure_data_node(id="imdb_top_1000", storage_type="csv",
path="../Downloads/ml-25m/IMDB_top_1000.csv",
scope=Scope.GLOBAL)

movie_title_cfg = Config.configure_data_node(id="movie_title", default_data="Toy Story")

movie_bag_cfg = Config.configure_data_node(id="movie_bagofwords")

num_rec_cfg = Config.configure_data_node(id="number_of_rec", default_data=10)

recommendations_cfg = Config.configure_data_node(id="recommendations")

# Task configuration

process_title_cfg = Config.configure_task(id="process_title",
function=process_title,
input=[movie_title_cfg, augmented_movie_cfg],
output=movie_bag_cfg)

give_recommendations_cfg = Config.configure_task(id="give_rcommendations",
function=give_recommendations,
input=[movie_bag_cfg, num_rec_cfg, imdb_top_1000_cfg],
output=recommendations_cfg)

# Pipeline configuration

pipeline_cfg = Config.configure_pipeline(id="pipeline",
task_configs=[process_title_cfg, give_recommendations_cfg])

# Scenario configuration

scenario_cfg = Config.configure_scenario(id="scenario",
pipeline_configs=pipeline_cfg)
