import pandas as pd

import taipy as tp 
from taipy import Config, Scope

from recommender_config import scenario_cfg

# run Taipy Core
tp.Core().run()

# create my scenario
scenario = tp.create_scenario(scenario_cfg)
tp.submit(scenario)
print("We recommend:", scenario.recommendations.read())