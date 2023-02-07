from taipy.gui import Gui, notify, Markdown

from algos.algos import clean_title, search

import pandas as pd

searched_film = ""
selected_film = ""
film_selector = [('','')]

page_search = Markdown("""
""")

