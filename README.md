# twitter-race
A python hashtag tracker for twitter [console based]
Keep track of different hashtags and see who is winning

* See live how many tweets are sent with the hashtags your are looking for
* DB stores counters for each hashtag given
* DB stores each tweet (as a json) that has one of your given hashtags for a deeper later analysis if wanted
* Specify the DB name to

 Please report issues, enhancements you can think of, suggestions, whatever!
------------

## Install

* `pip -r requirements.txt`
* Remember to set your keys in a `keys.py` file (grab them [here](https://apps.twitter.com/))
```
ACCESS_TOKEN = "YOUR ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR ACCESS_TOKEN_SECRET"
CONSUMER_KEY = "YOUR CONSUMER_KEY"
CONSUMER_SECRET = "YOUR CONSUMER_SECRET"
```

------------

## Usage
```
usage: track.py [-h] --hashtags [HASHTAGS [HASHTAGS ...]] [-d DB]

optional arguments:
  -h, --help            show this help message and exit
  -d DB, --db DB        Path for the database file [default: database.db]

mandatory arguments:
  --hashtags [HASHTAGS [HASHTAGS ...]]

```

------------

## Example

* To start tracking all tweets with #money, #sex, #love or #health
* Run: `python track.py --hashtags money sex love health`

* Output will be something like this:

![alt tag](http://i.imgur.com/VvIK5IN.png)

* A logger file will be created: `track.log`
* And a database file also: `database.db`

------------

## Notes
* All hits will be stored in a db (`database.db` by default)
* Also, a counter will be created in the database for each hashtag as `<hashtag>_counter`
* To access the db run a python console and:
```
import shelve
shelve.open('database.db')
db.items()
```
* Alternatively you can use the Tracker class, just look at the code ;)
* Remember the db is not accesible while the code is running to avoid 'Resource temporarily unavailable' issues when db gets hit a lot (I created this with no expectations, a better db mangement would be nice, yes, feel free to add it and pull request, I will be happy to adopt that feature!)
* Not Python 3.x compatible (yet)
* Python 2.7.9 or higher is needed because of [this](https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning)
* DB structure is something like this (key, value):
```
db['<yourhastag>_counter'] = 17
db['<tweet_id>'] = {[<tweet>](https://gist.github.com/patillacode/1fc239540ec006dd70a7#file-tweet-py)}
```
