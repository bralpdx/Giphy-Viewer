# Giphy-Viewer
### A [Giphy](https://giphy.com/) gif discovery tool.
This gif viewer uses a [Flask](https://flask.palletsprojects.com/en/1.1.x/) backend, 
in conjunction with a [MySQL](https://www.mysql.com/) database to display gifs to the user.

There is a rating function for the viewer, where the user can choose to either 'like' or 'dislike' the current gif being shown.
In the event that the user 'likes' the gif, the corresponding image-tags are then recorded, which are then used to later query 
the database for similar content to be displayed. Essentially, the longer the user uses it, the more the system begins to deliver 
content that the user finds appealing.

A record of previously shown gifs is kept, as a way to keep the user from seeing repeat content; however, the data for this app
has been collected via the [Giphy-Viewer Webscraper](https://github.com/bralpdx/Giphy-Viewer/tree/master/scrape), so it is subject to showing
repeated gifs, due to [Giphy's](https://giphy.com/) gif viewer occasionally showing duplicate content under different URLs.

![](https://github.com/bralpdx/Giphy-Viewer/blob/master/demo/17-07-2020%20demo.gif "Gif Discovery Demo") 

Author: Jonathan Bral
