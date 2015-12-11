import os
import sys
import keys
import json
import shelve
import logging

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

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

ATTR_COUNTER_FORMAT = '{0}_counter'


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

        for h in hashtags:
            if h['text'] in self.tracker.hashtags:
                hashtag_name = h['text']
                # we add 1 to the actual counter
                hits = getattr(self.tracker, hashtag_name) + 1

                # we set the new value
                counter = ATTR_COUNTER_FORMAT.format(h['text'])
                setattr(self.tracker, counter, hits)
                # store it in database
                self.tracker.set_data(counter, hits)
                # store whole tweet in database
                self.tracker.set_data(str(data['id']), data)
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
            db (str): path to db
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
        # Set all static attributes
        self.db = None
        self.stream = None
        self.listener = None
        self.hashtags = hashtags
        self.set_longest_hashtag()
        self.verbose = verbose
        # define vars needed for console output (also static)
        self.cell_size = (self.longest + 3)
        self.counter_whitespace = " " * ((self.cell_size - 6) / 2)
        self.border = "-" * ((self.cell_size * 2) + 1)

        # Set dynamic attributes (counters for each hashtag)
        for h in self.hashtags:
            setattr(self, "{0}_counter".format(h), 0)

    def __getattr__(self, name):
        try:
            counter = ATTR_COUNTER_FORMAT.format(name)
            return getattr(self, counter)
        except:
            raise AttributeError

    def set_data(self, key, value):
        """

            To set a value in the database

            Args:
                key (str): the key for the record to be saved
                value (*): the value for the record to be saved
        """
        self.db[key] = value

    def open_db(self, path):
        """ Opens the db file to be accessed """
        self.db = shelve.open(path)

    def close_db(self):
        """ Closes the db file """
        self.db.close()

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
            # counter = "{0}_counter".format(h)
            # hits = getattr(self, counter)
            hits = getattr(self, h)
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
            # counter = "{0}_counter".format(hashtag)
            # hits = getattr(self, counter)
            hits = getattr(self, hashtag)

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
