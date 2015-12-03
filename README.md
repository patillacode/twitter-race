# twitter-race
Python - twitter hashtag tracker [console based]
Keep track of different hashtags and see who is winning

# Install

* `pip -r requirements.txt`

# Notes

* Remember to set your keys in a `keys.py` file (grab them [here](https://apps.twitter.com/))
```
ACCESS_TOKEN = "YOUR ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR ACCESS_TOKEN_SECRET"
CONSUMER_KEY = "YOUR CONSUMER_KEY"
CONSUMER_SECRET = "YOUR CONSUMER_SECRET"
```
* All hits will be stored in a db (`track.db` by default)
* To access the db run a python console and:
```
import shelve
shelve.open('track.db')
db.items()
```

# Usage
`python track.py <hashtag#1> <hashtag#2> ... <hashtag#n>`

# Output Example
```
##########################
# python      #   00019   #
# javascript  #   00046   #
# ruby        #   00011   #
##########################
```
