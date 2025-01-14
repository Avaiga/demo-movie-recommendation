from taipy.gui import Gui, Markdown, notify, invoke_long_callback
from pages.search import (
    page_search,
    film_selector,
    selected_film,
    recommend_films,
    film_recommended_selector,
    movie_id,
)
from pages.user import (
    page_user,
    user_disliked,
    user_liked,
    user_viewed,
    content_selector,
    refresh_user,
    update_state_after_recommendation,
    asynchroneous_recommend_content_user,
)

from cards import create_cards, on_click

import taipy as tp
from taipy import Config

import uuid

# from config.recommender_config import scenario_cfg


def on_navigate(state, page_name):
    print(page_name)
    if page_name == "user":
        state.content_selector_partial.update_content(
            state, "Profile fetched! Waiting for recommendations..."
        )

        refresh_user(state)

        invoke_long_callback(
            state,
            asynchroneous_recommend_content_user,
            [state.scenario_id],
            update_state_after_recommendation,
            [],
        )
    return page_name


Config.load("config/config.toml")
scenario_cfg = Config.scenarios["user"]
scenario_id = ""
user = ""

pages = {
    "/": "<center>\n<|navbar|>\n</center>\n<|toggle|theme|>",
    "search": page_search,
    "user": page_user,
}


def on_init(state):
    state.user = str(uuid.uuid4())
    scenario = tp.create_scenario(scenario_cfg, name=state.user)
    state.scenario_id = scenario.id


def on_change(state, var_name, var_value):
    if var_name == "film_selector":
        state.film_selector_partial.update_content(
            state, create_cards(state.film_selector, "w342")
        )
    if var_name == "selected_film":
        state.content_selector_partial.update_content(
            state, "Film selected! Waiting for recommendations..."
        )

        recommend_films(state)


if __name__ == "__main__":
    gui = Gui(pages=pages)
    film_selector_partial = gui.add_partial("")
    recommended_film_selector_partial = gui.add_partial("")
    content_selector_partial = gui.add_partial("")

    gui.run(
        port=5006, debug=True, title="Movie Recommender"
    )  # (port=5006, use_reloader=True)
