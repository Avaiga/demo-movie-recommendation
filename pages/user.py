from taipy.gui import Gui, notify, Markdown

import taipy as tp

selected_user_liked = None
user_liked = []

selected_user_disliked = None
user_disliked = []

selected_user_viewed = None
user_viewed = []

page_user = Markdown("""
<|part|class_name=container|
<|🔄 Refresh|button|on_action=refresh_user|>

<|layout|columns=1 1 1|
<liked|
## ♥️ Liked

<|{selected_user_liked}|selector|lov={user_liked}|label=Liked|width=fit-content|>
|liked>

<disliked|
## 👎 Disliked

<|{selected_user_disliked}|selector|lov={user_disliked}|label=Disliked|width=fit-content|>
|disliked>

<viewed|
## 📽️ Viewed

<|{selected_user_viewed}|selector|lov={user_viewed}|label=Viewed|width=fit-content|>
|viewed>
|>
|>
""")


def refresh_user(state):
    user = tp.get(state.scenario_id)
    state.user_liked = user.liked.read()
    state.user_disliked = user.disliked.read()
    state.user_viewed = user.viewed.read()