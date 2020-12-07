"""
Adds/Increments tags that the user likes.
Computes range to pull tags from.
User list of dicts is sorted by highest count.
If user hasn't like anything yet, user list of dicts is empty.
check for this.
If not null, grab tags in range of highest count.
If null, call Gifs().retrieve_rand()
When user likes gif, add or increment tags to dict.
"""
from flask import redirect, url_for, request
from flask.views import MethodView
from index import db_gifs, app_user


# Adds or increments liked tags in user profile.
class Liked(MethodView):
    def post(self):
        url = request.form['url']  # Gets url of liked gif
        tags = db_gifs.get_tags(url)  # Gets tags that correspond with url
        app_user.new_liked(tags)  # Adds/increments those tags to user
        return redirect(url_for('index'))  # Loads next gif (reloads page)
