"""
Contains list of dicts of 'liked' tags.
(sorted by highest count)
Ex.
[{"tag":"funny", "count":2},{"tag":"political", "count":1}]
Minimum count is 1, because it has to be liked at least once
to get added to the list.
"""
import random


class User:
    def __init__(self):
        self.likes = []
        self.visited = []

    # Returns list of dicts of liked tags
    def get_likes(self):
        return self.likes

    # Initiates add tag process
    def new_liked(self, like_list):
        for tag in like_list:
            if not self.tag_exist(tag[0]):
                self.add_tag(tag[0])
        self.sort()

    # Checks if a tag exists. Increments counter if it does.
    def tag_exist(self, tag):
        for item in self.likes:
            if item['tag'] == tag:
                item['count'] += 1
                return True
        return False

    # Adds new tag
    def add_tag(self, tag):
        self.likes.append({"tag": tag, "count": 1})

    # Gets a tag from the users liked
    def get_tag(self):
        random.seed()
        index = random.randint(0, (len(self.likes) - 1))
        output = self.likes[index]['tag'].split()[0]  # Splits after the first word
        return output

    # Sorts by count (greatest to least)
    def sort(self):
        self.likes = sorted(self.likes, key=lambda i: i['count'], reverse=True)

    # Tracks which gifs have been delivered to the user
    def add_visited(self, gifid):
        self.visited.append(gifid)
        self.visited = sorted(self.visited)

    # Searches to see if a gif has been visited
    def search_visited(self, gifid):
        # No url's have been added
        if not self.visited:
            return True
        if self.visited[-1] < gifid:
            # URL hasn't been visited
            return True

        last_index = len(self.visited) - 1
        return self.binary_search(gifid, 0, last_index)

    # Standard binary search for visited list
    def binary_search(self, key, lo, hi):
        mid = lo + (hi - lo) // 2
        if hi >= lo:
            if self.visited[mid] == key:
                # Link has been shown
                return False
            if self.visited[mid] < key:
                return self.binary_search(key, (mid + 1), hi)
            else:
                return self.binary_search(key, lo, (mid - 1))
        else:
            # Wasn't found. Link hasn't been shown.
            return True


# Creates a global instance that is passed between modules.
user_instance = User()
