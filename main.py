from taipy.gui import Gui, Markdown, notify
from pages.search import page_search
from pages.user import page_user, user_disliked, user_liked, user_viewed

import taipy as tp 
from taipy.config import Config

import uuid


Config.load('config/config.toml')
scenario_cfg = Config.scenarios['user']
scenario_id = ""
user = ""

pages = {"/":"<center> <|navbar|> </center> <|toggle|theme|>",
         "search":page_search,
         "user":page_user}

def on_init(state):
    state.user = str(uuid.uuid4())
    scenario = tp.create_scenario(scenario_cfg, name=state.user)
    state.scenario_id = scenario.id

if __name__ == "__main__":
    gui = Gui(pages=pages)
    gui.run(port=5006)#(port=5006, use_reloader=True)
