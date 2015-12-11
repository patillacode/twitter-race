import os
import sys
import keys
import json
import logging

from uuid import uuid4
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import settings

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET

# Colors definition for output
COLORS = {'magenta': '35',
          'green': '32',
          'red': '33;1',
          'cyan': '36',
          'white': '37;1',
          'yellow': '33'}


class Listener(StreamListener):
    """This is a basic listener that just prints received tweets."""
    def __init__(self, tracker, *args, **kwargs):
        self.tracker = tracker
        super(Listener, self).__init__(*args, **kwargs)

    def on_data(self, data):
        """
            What to do on the event of receiving data while listening

            Args:
                data: Response form twitter API with the tracked tweet
        """
        data = json.loads(data)
        hashtags = []
        if 'entities' in data and 'hashtags' in data['entities']:
            hashtags = data['entities']['hashtags']

        if len(hashtags):
            for h in hashtags:
                if h['text'] in self.tracker.hashtags:
                    # we get the hashtag name
                    counter = "{0}_counter".format(h['text'])
                    # we add 1 to the actual counter
                    hits = getattr(self.tracker, counter) + 1
                    # we set the new value
                    setattr(self.tracker, counter, hits)
                    # store it in database
                    self.tracker.set_data(counter, hits)
                    # create data to be published in channel
                    data_to_publish = {}
                    data_to_publish.update({'event': 'tweet'})
                    data_to_publish.update({'hashtag': h['text']})
                    data_to_publish.update(
                        {'text': data['text'].encode('utf-8')})
                    user_data = {'id': data['user']['id_str'],
                                 'name': data['user']['name'].encode('utf-8'),
                                 'screen_name': data['user']['screen_name']
                                 }
                    data_to_publish.update({'user': user_data})
                    # publish data
                    self.tracker.publish_data(data_to_publish)
                    # show results table in console if verbose was indicated
                    if self.tracker.verbose:
                        self.tracker.print_table()
        return True

    def on_error(self, status):
        """
            Log if an error occurs when accessing the API

            Args:
                status (int): HTTP status code
        """
        logging.error("Listener had problems connecting. Status: {0}".format(
            status))


class Tracker():
    """
        Main class that handles most of our app.

        Attributes:
            redis (Redis): redis connection (settings)
            channel (str): channel unique identifier
            hashtags (list): hashtags to keep track of
            known_items (list): all known attributes of the class
            listener (Listener): Twitter StreamListener
            longest (int): length of longest hashtags (for output purposes)
            stream (Stream): Twitter authenticated stream of data
    """

    def __init__(self, verbose, hashtags=[]):
        """
            Args:
                hashtags (list, optional): hashtags entered as parameters
        """
        # Confirm hashtags are given in a list
        try:
            assert(isinstance(hashtags, list))
        except AssertionError:
            sys.exit(2)

        # Set all static attributes
        self.stream = None
        self.listener = None
        self.verbose = verbose
        self.hashtags = hashtags
        self.set_longest_hashtag()
        self.redis = settings.REDIS
        self.create_redis_channels()
        self.set_unique_redis_channel()

        # define vars needed for console output (also static)
        self.cell_size = (self.longest + 3)
        self.counter_whitespace = " " * ((self.cell_size - 6) / 2)
        self.border = "-" * ((self.cell_size * 2) + 1)

        # Set dynamic attributes (counters for each hashtag)
        for h in self.hashtags:
            setattr(self, "{0}_counter".format(h), 0)

    def create_redis_channels(self):
        """
            Creates 'channels' in redis if it doesn't exist
            'channels' is to keep track of existing publishing channels
        """
        if "channels" not in self.redis.keys():
            self.redis.set("channels", json.dumps({"channels": []}))

    def set_unique_redis_channel(self):
        """ Creates a unique channel id """
        channel_id = str(uuid4())
        used_channels = json.loads(self.redis.get("channels"))["channels"]
        if channel_id in used_channels:
            self.get_unique_redis_channel()
        else:
            self.channel = channel_id
            used_channels.append(channel_id)
            self.redis.set("channels", json.dumps({"channels": used_channels}))

    def set_data(self, key, value):
        """ Set a key/value pair in redis """
        self.redis.set(key, value)

    def publish_data(self, data):
        """

            Publish data/event in a channel

            Args:
                data: data to publish in redis
        """
        logging.debug("publishing to channel {0}".format(self.channel))
        self.redis.publish(self.channel, json.dumps(data))

    def authenticate(self):
        """
            Authenticate against the Twitter API

            Returns:
                Stream: <Twitter authenticated Stream object>
        """
        # Twitter authentication and connection to Twitter Streaming API
        self.listener = Listener(self)
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.stream = Stream(auth, self.listener)
        return self.stream

    def set_longest_hashtag(self):
        """ Sets our longest_hashtag attribute """
        self.longest = 0
        for h in self.hashtags:
            if len(h) > self.longest:
                self.longest = len(h)

    def get_winning_hashtag(self):
        """
            Get currently winning hashtag

            Returns:
                str: <winner>
        """
        winner = {'hashtag': '', 'value': 0}
        for h in self.hashtags:
            counter = "{0}_counter".format(h)
            hits = getattr(self, counter)
            if hits > winner['value']:
                winner['hashtag'] = h
                winner['value'] = hits
        return winner['hashtag']

    def colorize(self, color, message):
        """
            Colorizes given message with given color

            Args:
                color (str): Parsed with global var COLORS
                message (str): message to be colorized

            Returns:
                str: message with requested color codes
        """
        return "\033[{0}m{1}\033[0m".format(COLORS[color], message)

    def print_table(self):
        """ Prints table with live results into console """
        # clear console
        os.system('clear')

        # Colorize table items!
        border = self.colorize('cyan', self.border)
        separator = self.colorize('cyan', '|')

        # print table top border
        sys.stderr.write(" {0} \n".format(border))

        # Grab all counters and print their value
        for hashtag in self.hashtags:
            # For better output we calculate the whitespace necessary
            # depending on each hashtag length
            hashtag_whitespace = " " * (self.longest - len(hashtag) + 3)

            # get number of hits for each hashtag
            counter = "{0}_counter".format(hashtag)
            hits = getattr(self, counter)

            # set winner banner and color for output
            winner_banner = ''
            color = 'yellow'

            # set different banner and different color for winning hashtag
            if hashtag is self.get_winning_hashtag():
                winner_banner = self.colorize('magenta', ' # WINNING #')
                color = 'green'

            # Colorize
            hashtag = self.colorize(color, hashtag)
            hits = self.colorize(color, str(hits).zfill(5))

            # output table contents
            sys.stderr.write('{0} {1}{2} {0}{3}{4}{3}{0}{5}\n'.format(
                separator,
                hashtag,
                hashtag_whitespace,
                self.counter_whitespace,
                hits,
                winner_banner))

        # print table bottom border
        sys.stderr.write(" {0} \n".format(border))
