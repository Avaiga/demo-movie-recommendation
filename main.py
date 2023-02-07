from taipy.gui import Gui, Markdown, notify
from pages.search import page_search
from pages.user import page_user


pages = {"/":"<|navbar|>",
         "search":page_search,
         "user":page_user}

if __name__ == "__main__":
    gui = Gui(pages=pages)
    gui.run(port=5006)