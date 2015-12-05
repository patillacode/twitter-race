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
  -d DB, --db DB        Path for the database file [default: track.db]

mandatory arguments:
  --hashtags [HASHTAGS [HASHTAGS ...]]

```

------------

## Example

 * This will start tracking all tweets with either #python or #javascript
 `python track.py --hashtags python javascript -d database`

 * Output will be something like this:
```
 -------------------------
| python      |   00003   |
| javascript  |   00014   |
 -------------------------
```

* A logger file will be created: `track.log`

* And a database file also: `database.db`

------------

## Notes
* All hits will be stored in a db (`track.db` by default)
* Also, a counter will be created in the database for each hashtag as `<hashtag>_counter`
* To access the db run a python console and:
```
import shelve
shelve.open('track.db')
db.items()
```
* Alternatively you can use the Tracker class, just look at the code ;)
* Remember the db is not accesible while the code is running to avoid 'Resource temporarily unavailable' issues when db gets hit a lot (I created this with no expectations, a better db mangement would be nice, yes, feel free to add it and pull request, I will be happy to adopt that feature!)
* Not Python 3.x compatible (yet)
* Python 2.7.9 or higher is needed because of [this](https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning)
* DB structure is something like this (key, value):
```
db['<yourhastag>_counter'] = 17
db['<tweet_id>'] = { u'contributors': None,
                     u'coordinates': None,
                     u'created_at': u'Fri Dec 04 15:01:22 +0000 2015',
                     u'entities': {u'hashtags': [{u'indices': [67, 78], u'text': u'javascript'},
                       {u'indices': [79, 83], u'text': u'php'},
                       {u'indices': [84, 91], u'text': u'python'},
                       {u'indices': [92, 113], u'text': u'softwarearchitecture'}],
                      u'symbols': [],
                      u'urls': [{u'display_url': u'goo.gl/fb/XGY31t',
                        u'expanded_url': u'http://goo.gl/fb/XGY31t',
                        u'indices': [34, 57],
                        u'url': u'https://t.co/IsV6k4D6BL'}],
                      u'user_mentions': []},
                     u'favorite_count': 0,
                     u'favorited': False,
                     u'filter_level': u'low',
                     u'geo': None,
                     u'id': 672792817341743104,
                     u'id_str': u'672792817341743104',
                     u'in_reply_to_screen_name': None,
                     u'in_reply_to_status_id': None,
                     u'in_reply_to_status_id_str': None,
                     u'in_reply_to_user_id': None,
                     u'in_reply_to_user_id_str': None,
                     u'is_quote_status': False,
                     u'lang': u'en',
                     u'place': None,
                     u'possibly_sensitive': False,
                     u'retweet_count': 0,
                     u'retweeted': False,
                     u'source': u'<a href="http://www.google.com/" rel="nofollow">Google</a>',
                     u'text': u'Write some Software by kleemann21 https://t.co/IsV6k4D6BL Hello!!  #javascript #php #python #softwarearchitecture',
                     u'timestamp_ms': u'1449241282197',
                     u'truncated': False,
                     u'user': {u'contributors_enabled': False,
                      u'created_at': u'Thu Jun 25 06:52:27 +0000 2009',
                      u'default_profile': False,
                      u'default_profile_image': False,
                      u'description': u'Freelance Provider, and Social Networking',
                      u'favourites_count': 0,
                      u'follow_request_sent': None,
                      u'followers_count': 522,
                      u'following': None,
                      u'friends_count': 1861,
                      u'geo_enabled': True,
                      u'id': 50575507,
                      u'id_str': u'50575507',
                      u'is_translator': False,
                      u'lang': u'en',
                      u'listed_count': 431,
                      u'location': None,
                      u'name': u'Kalpataru Deori',
                      u'notifications': None,
                      u'profile_background_color': u'0099B9',
                      u'profile_background_image_url': u'http://pbs.twimg.com/profile_background_images/19790339/h1.jpg',
                      u'profile_background_image_url_https': u'https://pbs.twimg.com/profile_background_images/19790339/h1.jpg',
                      u'profile_background_tile': False,
                      u'profile_image_url': u'http://pbs.twimg.com/profile_images/590172778/KB_Deori_11_normal.jpg',
                      u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/590172778/KB_Deori_11_normal.jpg',
                      u'profile_link_color': u'F00E3B',
                      u'profile_sidebar_border_color': u'81C4F7',
                      u'profile_sidebar_fill_color': u'7DC4FA',
                      u'profile_text_color': u'3C3940',
                      u'profile_use_background_image': True,
                      u'protected': False,
                      u'screen_name': u'kalpataru123',
                      u'statuses_count': 1351823,
                      u'time_zone': u'Kolkata',
                      u'url': u'http://kalpatarudeori.blogspot.com',
                      u'utc_offset': 19800,
                      u'verified': False}}
```
