from flask import render_template
from flask.views import MethodView
from gifs import Gifs
import random
from user import User


app_user = User()
db_gifs = Gifs(app_user)


class Index(MethodView):
    def __init__(self):
        self.user = app_user
        self.gifs = db_gifs

    def get(self):
        # Choice allows for new random gif to be
        # periodically served to user.
        choice = random.randint(1, 20)

        # If the user hasn't liked any gif yet
        # It calls for a random gif to be delivered
        if not self.user.likes:
            url = self.gifs.retrieve_rand()
        else:
            if choice > 5:
                url = self.gifs.retrieve()
            else:
                url = self.gifs.retrieve_rand()

        if self.user.likes:
            self.gifs.liked_range()  # Adjusts the user's liked list

        return render_template('index.html', url=url)
