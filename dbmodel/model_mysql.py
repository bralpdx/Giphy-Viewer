from dbmodel.Model import Model
import mysql.connector
from mysql.connector import errorcode
import os
import json
import random

"""
giflist table schema Example:
------------------------------------------------------------
|  ID  |                        URL                        |
|------+---------------------------------------------------|
|   1  | 'https://giphy.com/gifs/RLWwOuPbqObupogOLB/html5' |
------------------------------------------------------------

taglist Table schema:
-------------------------
|  ID  |       TAG      |
|------|----------------|
|   1  |    "tagname"   | 
|------|----------------|
|   2  |  "other tag"   |
-------------------------

giftags Table schema:
------------------------
|  ID  | gifid | tagid |
|------|---------------|
|   1  |   1   |  1    |
|------|---------------|
|   2  |   1   |  3    |
------------------------
"""
# Changes to current directory (Likely will change later.)
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

DATA_FILEPATH = '../scrape/url_data.json'
DB_NAME = 'giphy_db'  # Database name

# Grabs 'secret' environment variables.
# corresponding to database username and password.
user = os.environ.get('DBUSER')
password = os.environ.get('DBPASS')


# SQL for creating tables.
tables = {}

tables['giflist'] = (
    "CREATE TABLE `giflist` ("
    " `gifid` int(11) NOT NULL AUTO_INCREMENT,"
    " `url` varchar(2083) NOT NULL,"
    " PRIMARY KEY (`gifid`)"
    ") ENGINE=InnoDB"
)

tables['taglist'] = (
    "CREATE TABLE `taglist` ("
    " `tagid` int(11) NOT NULL AUTO_INCREMENT,"
    " `tag` varchar(255) NOT NULL,"
    " PRIMARY KEY (`tagid`)"
    ") ENGINE=InnoDB"
)

tables['giftags'] = (
    "CREATE TABLE `giftags` ("
    " `id` int(11) NOT NULL AUTO_INCREMENT,"
    " `gifid` int(11) NOT NULL,"
    " `tagid` int(11) NOT NULL,"
    " FOREIGN KEY (`gifid`) REFERENCES `giflist` (`gifid`) ON DELETE RESTRICT ON UPDATE CASCADE,"
    " FOREIGN KEY (`tagid`) REFERENCES `taglist` (`tagid`) ON DELETE RESTRICT ON UPDATE CASCADE,"
    " PRIMARY KEY (`id`,`gifid`,`tagid`)"
    ") ENGINE=InnoDB"
)

query_table = {}
# Query to get tags of the current gif being displayed
# by passing in a string of the URL.
query_table['tags'] = (
    "SELECT taglist.tag, giftags.gifid"
    " FROM taglist INNER JOIN giftags"
    " ON giftags.tagid = taglist.tagid"
    " INNER JOIN giflist"
    " ON giftags.gifid = giflist.gifid"
    " WHERE giflist.url = '%s'"
)

query_table['tag_like'] = (
    "select giflist.url, giflist.gifid"
    " from giflist inner join giftags"
    " on giftags.gifid = giflist.gifid"
    " inner join taglist"
    " on giftags.tagid = taglist.tagid"
    " where taglist.tag like %s"
)


# Connects to the database.
def db_connect():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor()
    except mysql.connector.Error:
        # If the database does not exist, create the database.
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
        )
        cursor = connection.cursor()
        create_dbstr = "CREATE DATABASE " + DB_NAME
        cursor.execute(create_dbstr)
    cursor.close()


# Checks for tables existence
# If table does not exist, it gets created.
def create_tables():
    connection = mysql.connector.connect(
        host='localhost',
        user=user,
        password=password,
        database=DB_NAME
    )
    cursor = connection.cursor()

    for table_name in tables:
        try:
            table_description = tables[table_name]
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno != errorcode.ER_TABLE_EXISTS_ERROR:
                print(err.msg)

    cursor.close()


class model(Model):
    def __init__(self):
        # checks connection / creates DB if needed.
        db_connect()
        # checks for tables existence / creates tables if needed.
        create_tables()
        # populate tables from data file
        self.populate_tables(DATA_FILEPATH)

    def select_gifs(self):
        """
        Fetches all rows from giflist table
        Each row contains: ID, URL
        :return: list of lists containing all rows of table
        """
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM giflist")
        return cursor.fetchall()

    def select_tags(self, url):
        """
        Fetches all tags from taglist table
        that correspond with the passed in url
        :return: list containing all matching tags
        """
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(query_table['tags'] % url)
        return cursor.fetchall()

    def select_giftags(self):
        """
        Fetches all rows from giflist table
        Each row contains: ID, URL
        :return: list of lists containing all rows of table
        """
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM giftags")
        return cursor.fetchall()

    def insert(self, url, tags):
        """
        Inserts entry into tables
        :param url:
        :param tags:
        :return: True
        """
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor(buffered=True)

        # insert into giflist
        link = (url,)
        sql = "INSERT INTO giflist (url) VALUES (%s)"
        cursor.execute(sql, link)
        # insert into taglist
        for tag in tags:
            # Inserts new tag into taglist table
            tag_exist_sql = "SELECT 1 FROM taglist WHERE tag = '{}'".format(tag)
            cursor.execute(tag_exist_sql)
            num = len(cursor.fetchall())
            val = (tag,)

            if num < 1:
                cursor.execute("INSERT INTO taglist (tag) VALUES (%s)", val)

            # insert into giftags
            sql_gid = "SELECT gifid FROM giflist WHERE url='{}'".format(link[0])
            sql_tid = "SELECT tagid FROM taglist WHERE tag='{}'".format(val[0])
            cursor.execute(sql_gid)
            gid = cursor.fetchone()
            cursor.execute(sql_tid)
            tid = cursor.fetchone()
            sql = "INSERT INTO giftags (gifid, tagid) VALUES (%s, %s) "
            cursor.execute(sql, (gid[0], tid[0]))

        connection.commit()
        cursor.close()
        return True

    # Populates the database tables from the designated json file.
    def populate_tables(self, filepath):
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor()

        if os.path.isfile(filepath):
            with open(filepath) as file:
                data = json.load(file)
        else:
            print("ERROR. File 'url_data.json' not found.")
            print("Current directory:", end='')
            print(os.getcwd())
            return False
        for entry in data:
            # Check if entry has already been added
            sql = "SELECT 1 FROM giflist WHERE url = '{}'".format(entry['link'])
            cursor.execute(sql)
            num = len(cursor.fetchall())
            if num < 1:
                self.insert(entry['link'], entry['tags'])

        return True

    # Selects a random row from the giflist table and returns the url field
    def select_rand(self):
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor()

        cursor.execute(
            "SELECT url, gifid FROM giflist ORDER BY RAND() LIMIT 1"
        )
        output = cursor.fetchone()
        cursor.close()

        return output  # Returns gif data

    # Queries database for all results matching passed in tag. Returns random result.
    def select_with_tag(self, tag):
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=DB_NAME
        )
        cursor = connection.cursor()

        arg = "'%s" % tag + "%'"
        cursor.execute(query_table['tag_like'] % arg)

        output = cursor.fetchall()
        # Allows us to redo a different query
        # Prevents empty query being served.
        if not output:
            return False

        cursor.close()

        # Selects random returned index of matching tag query
        random.seed()
        index = random.randint(0, (len(output) - 1))

        return output[index]  # Returns gif data


if __name__ == '__main__':
    model()
