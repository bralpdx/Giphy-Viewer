# Giphy-Viewer Webscraper 
### **A Giphy Webscraper Written in Python3**
This is a webscraper for [**Giphy**](https://giphy.com/).
Its purpose is to scrape the urls and tags that correspond with gifs from [**the trending gif section of Giphy**](https://giphy.com/trending-gifs).

The webscraper functions as a bot, that takes advantage of Giphy's built in feature that allows users to browse gifs by selecting a 'next' arrow.
The bot automates the processes of copying a gifs embedded url, and tags, and then selecting the 'next' arrow/button to load the next gif.
All of the collected data is then written to a JSON file in the working directory.

The automation process uses [**selenium**](https://www.selenium.dev/) and Mozilla's [**Geckodriver**](https://github.com/mozilla/geckodriver).
