import taipy.gui.builder as tgb
import ast
from api import fetch_api_film, transform_tmdb_id_to_movie_id


def on_click(state, id, payload):
    state.movie_id = transform_tmdb_id_to_movie_id(id)

    state.selected_film = fetch_api_film(id)
    state.film_selector = []


def create_cards(film_selector, image_size="w500", prerender=False):
    with tgb.Page() as film_selector_page:
        with tgb.layout("1 1 1 1 1"):
            for film in film_selector:
                with tgb.part("card include-image"): 
                    if film["poster_path"] is not None and not prerender:
                        tgb.image(f"http://image.tmdb.org/t/p/{image_size}{film['poster_path']}",
                                  class_name="card-image",
                                  on_action=on_click,
                                  id=film["id"],
                                  hover_text=film["original_title"] + " \n-\n " + film["overview"])
                    else:
                        tgb.text(film["original_title"], class_name="h2")
                        tgb.text(film["overview"])

    return film_selector_page