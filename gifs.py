"""
Purpose: Contains functions that query the database
for urls and tags.
"""
import dbmodel
from user import user_instance as user


class Gifs:
    def __init__(self):
        """
        Works with file in JSON
        self.filename = './scrape/url_data.json'
        f = open(self.filename)
        self.data = json.load(f)
        """
        self.model = dbmodel.get_model()
        self.user = user
        self.max_tries = 5

    # Gets all tags of current gif from database
    def get_tags(self, url):
        tags = self.model.select_tags(url)
        return tags

    def retrieve(self):
        """
        Retrieves a tag from the user.
        Queries the database URL that corresponds with that tag.
        If not entry is returned, it tries.
        After 5 tries, calls for random query.
        """
        current_try = 0
        tag = user.get_tag()
        output = self.model.select_with_tag(tag)
        if not self.user.search_visited(output[1]):
            output = False

        while not output:
            tag = user.get_tag()
            gif_data = self.model.select_with_tag(tag)
            # Checks to see if url has been visited first
            if self.user.search_visited(gif_data[1]):
                output = gif_data
            current_try += 1
            if current_try >= self.max_tries:
                output = self.retrieve_rand()

        # If a gifid failed to return
        if output[1] == 't':
            # Try again to get the gifid
            return output
        else:
            self.user.add_visited(output[1])
            return output[0]

    # Retrieves a random gif from the DB
    def retrieve_rand(self):
        output = self.model.select_rand()
        visit = self.user.search_visited(output[1])

        # Searches until find a gif that hasn't been shown to the user.
        while not visit:
            output = self.model.select_rand()
            visit = self.user.search_visited(output[1])

        self.user.add_visited(output[1])
        return output[0]


if __name__ == '__main__':
    Gifs()

