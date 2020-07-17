from flask import render_template
from flask.views import MethodView
from gifs import Gifs
import random
from user import user_instance as user


class Index(MethodView):
    def get(self):
        # Choice allows for new random gif to be
        # periodically served to user.
        choice = random.randint(1, 5)

        # If the user hasn't liked any gif yet
        # It calls for a random gif to be delivered
        if not user.likes:
            url = Gifs().retrieve_rand()
        else:
            if choice > 2:
                url = Gifs().retrieve()
            else:
                url = Gifs().retrieve_rand()

        return render_template('index.html', url=url)
