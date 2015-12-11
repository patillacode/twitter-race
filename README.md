# twitter-race
A python hashtag tracker for twitter

Keep track of different hashtags and see which one is winning

* See live in your console how many tweets are being sent containing the hashtags your are looking for
* Redis stored counters for each hashtag given
* Redis stored tweets (as a json) that have one of your given hashtags (for a deeper later analysis if wanted)


###### Notes:
* First beta release for local use can be found [here](https://github.com/patillacode/twitter-race/releases/tag/0.1.0)


#### Please report issues, enhancements you can think of, suggestions, whatever!
------------

## Install

##### hashtag tracker (twitter-race)
* `pip -r requirements.txt`
* Remember to set your keys in a `keys.py` file (grab them [here](https://apps.twitter.com/))
```
ACCESS_TOKEN = "YOUR ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR ACCESS_TOKEN_SECRET"
CONSUMER_KEY = "YOUR CONSUMER_KEY"
CONSUMER_SECRET = "YOUR CONSUMER_SECRET"
```

##### redis (I recommend you take a look [here](http://redis.io/topics/quickstart))
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
usage: track.py [-h] [-v] --hashtags [HASHTAGS [HASHTAGS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Show table with live data [default: False]

mandatory arguments:
  --hashtags [HASHTAGS [HASHTAGS ...]]

```

------------

## Example

* To start tracking all tweets with #money, #sex, #love or #health
* Run: `python track.py -v --hashtags money sex love health`

* Output will be something like this:

![alt tag](http://i.imgur.com/VvIK5IN.png)

* A logger file will be created: `track.log`

* to see redis stored keys:
* log into your redis server (-n option is to see database 1 - default for this app)

"""
  $ redis-cli -h <host> -p <port> -n 1
"""

* once in, check the existing keys like this:

"""
  localhost:6379[1]> keys *
    1) "health_counter"
    2) "love_counter"
    3) "money_counter"
    4) "sex_counter"
    5) "channels"
"""

* to retrieve the content of a key

"""
  localhost:6379[1]> get love_counter
    "18"
"""

* to see redis published data/events:
* log into your redis server (-n option is to see database 1 - default for this app)

"""
  $ redis-cli -h <host> -p <port> -n 1
"""

* once in, check the existing keys like this:

"""
  # channel id can be found in track.log)
  localhost:6379[1]> PSUBSCRIBE your-channel-id
"""

* An example of data published into the redis channel:

"""
  {'pattern': '05385555-6380-4cdf-966e-1701ba7494c5', 'type': 'pmessage', 'channel': '05385555-6380-4cdf-966e-1701ba7494c5', 'data': '{"text": "RT @GayWeHoDogs4U: #Rescue me! Adult male #Chihuahua/#Beagle mix.  #nkla #dogs #love https://t.co/v5iYldKcrh https://t.co/cLoVgVLlFg", "user": {"screen_name": "Serabbi", "id": "457904385", "name": "Serabbi"}, "event": "tweet", "hashtag": "love"}'}
"""

------------

## Notes
* All hits will be published into a unique redis channel
* Also, a counter will be created in redis as a key, like: `<hashtag>_counter`
* Not Python 3.x compatible (yet)
* Python 2.7.9 or higher is needed because of [this](https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning)
* Example of a captured [raw tweet](https://gist.github.com/patillacode/1fc239540ec006dd70a7#file-tweet-py)
