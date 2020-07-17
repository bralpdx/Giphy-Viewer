"""
Creates and adds data to JSON file
"""
import os
import json

filename = './url_data.json'


class UrlData:
    def add(self, url, tags):
        if os.path.isfile(filename):
            # File already exists, return populated dict.
            with open(filename) as file:
                data = json.load(file)
                data.append({
                    'link': url,
                    'tags': tags
                })
        else:
            data = [{
                'link': url,
                'tags': tags
            }]
        with open(filename, 'w') as f:
            json.dump(data, f)
