# twitter-race
A python hashtag tracker for twitter [console based]

Keep track of different hashtags and see which one is winning

* See live in your console how many tweets are being sent containing the hashtags your are looking for
* Database stored counters for each hashtag given
* Database stored tweets (as a json) that have one of your given hashtags (for a deeper later analysis if wanted)
* You can specify the database name as a parameter to have multiple ones, for different analysis.

 #### Please report issues, enhancements you can think of, suggestions, whatever!
------------

## Install

### tracker (twitter-race)
* `pip -r requirements.txt`
* Remember to set your keys in a `keys.py` file (grab them [here](https://apps.twitter.com/))
```
ACCESS_TOKEN = "YOUR ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR ACCESS_TOKEN_SECRET"
CONSUMER_KEY = "YOUR CONSUMER_KEY"
CONSUMER_SECRET = "YOUR CONSUMER_SECRET"
```

### redis (I recommend you take a look [here](http://redis.io/topics/quickstart))
###### Although a small summary would be this:
"""
    $ wget http://download.redis.io/redis-stable.tar.gz # download redis
    $ tar xvzf redis-stable.tar.gz                      # uncompress it
    $ cd redis-stable                                   # move into the uncompressed folder
    $ make                                              # install
    $ make test                                         # run tests
    $ sudo cp src/redis-server /usr/local/bin/          # copy server command into your environment
    $ sudo cp src/redis-cli /usr/local/bin/             # copy client command into your environment
"""
######
------------

## Usage
```
usage: track.py [-h] --hashtags [HASHTAGS [HASHTAGS ...]] [-d DB] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -d DB, --db DB        Path for the database file [default: database.db]
  -v, --verbose         Show table with live data [default: False]

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
db['<tweet_id>'] = {<tweeet>}
```
* Example of [storaged tweet](https://gist.github.com/patillacode/1fc239540ec006dd70a7#file-tweet-py)
