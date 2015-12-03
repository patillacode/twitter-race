# Import the necessary methods from tweepy library
import os
import sys
import keys
import json
import shelve
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET

DB_PATH = 'track'


def open_db():
    return shelve.open(DB_PATH)


# This is a basic listener that just prints received tweets to stdout.
class Listener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        hashtags = []
        if 'entities' in data and 'hashtags' in data['entities']:
            hashtags = data['entities']['hashtags']

        if len(hashtags):
            for h in hashtags:
                if h['text'] in tracker.hashtags:
                    # we get the hashtag name
                    counter = "{0}_counter".format(h['text'])
                    # we add 1 to the actual counter
                    hits = getattr(tracker, counter) + 1
                    # we set the new value
                    setattr(tracker, counter, hits)
                    # store it in the database
                    tracker.store_data(counter, hits)
                    # show results in console
                    tracker.results()
        return True

    def on_error(self, status):
        print "Error: {0}".format(status)


class Tracker():
    def __init__(self, hashtags):
        try:
            assert(isinstance(hashtags, list))
        except AssertionError:
            sys.exit(2)

        self.known_items = ["hashtags",
                            "listener",
                            "stream",
                            "known_items",
                            "longest"]

        self.hashtags = hashtags
        for h in self.hashtags:
            setattr(self, "{0}_counter".format(h), 0)

        self.set_longest_hashtag()

    def store_data(self, key, value):
        db = open_db()
        db[key] = value
        db.close()

    def authenticate(self):
        # Twitter authentication and connection to Twitter Streaming API
        self.listener = Listener()
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.stream = Stream(auth, self.listener)
        return self.stream

    def set_longest_hashtag(self):
        self.longest = 0
        for h in self.hashtags:
            if len(h) > self.longest:
                self.longest = len(h)

    def results(self):
        os.system('clear')
        cell_size = (self.longest + 3)
        print "#" * (cell_size * 2)
        for k, v in self.__dict__.iteritems():
            if k not in self.known_items:
                whitespace = " " * (self.longest - len(k) + 9)
                print "# {0}{1} #   {2}  #".format(k[:-8],
                                                   whitespace,
                                                   str(v).zfill(5))
        print "#" * (cell_size * 2)


def usage():
    print "Usage:"
    print '\tpython track.py <hashtag#1> <hashtag#2> ... <hashtag#n>\n'
    sys.exit(2)


if __name__ == '__main__':

    if len(sys.argv[1:]) < 1:
        usage()

    hashtags = list()
    for a in sys.argv[1:]:
        # list of hashtags to track
        hashtags.append(str(a))

    tracker = Tracker(hashtags)
    stream = tracker.authenticate()
    # This line filter Twitter Streams to capture data by the keywords
    stream.filter(track=tracker.hashtags)
