#!/usr/bin/env python
#
#    _/                          _/    _/      _/
# _/_/_/_/  _/      _/      _/      _/_/_/_/_/_/_/_/    _/_/    _/  _/_/
#  _/      _/      _/      _/  _/    _/      _/      _/_/_/_/  _/_/
# _/        _/  _/  _/  _/    _/    _/      _/      _/        _/
#  _/_/      _/      _/      _/      _/_/    _/_/    _/_/_/  _/
#
#    _/  _/_/    _/_/_/    _/_/_/    _/_/
#   _/_/      _/    _/  _/        _/_/_/_/
#  _/        _/    _/  _/        _/
# _/          _/_/_/    _/_/_/    _/_/_/
#
# This file is part of Twitter Race.  Twitter Race is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Patilla Code
#
# title           :track.py
# description     :Stream Listener and tracker for tweets with given hashtags
# author          :PatilaCode
# date            :20151203
# version         :0.0.6
# usage           :python track.py -v --hashtags <hashtag#1> ... <hashtag#n>
# notes           :
# python_version  :2.7.10
# =============================================================================

import os
import sys
import keys
import json
import shelve
import argparse
import logging
import traceback

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

logging.basicConfig(filename='track.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET
CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET

# DB filename/path (set via argparse)
DB_PATH = ''

# Colors definition for output
COLORS = {'magenta': '35',
          'green': '32',
          'red': '33;1',
          'cyan': '36',
          'white': '37;1',
          'yellow': '33'}


class Listener(StreamListener):
    """This is a basic listener that just prints received tweets."""

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
                if h['text'] in tracker.hashtags:
                    # we get the hashtag name
                    counter = "{0}_counter".format(h['text'])
                    # we add 1 to the actual counter
                    hits = getattr(tracker, counter) + 1
                    # we set the new value
                    setattr(tracker, counter, hits)
                    # store it in database
                    tracker.set_data(counter, hits)
                    # store whole tweet in database
                    tracker.set_data(str(data['id']), data)
                    # show results table in console if verbose was indicated
                    if tracker.verbose:
                        tracker.print_table()
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
        # Confirm hashtags are given in a list
        try:
            assert(isinstance(hashtags, list))
        except AssertionError:
            sys.exit(2)

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

    def set_data(self, key, value):
        """

            To set a value in the database

            Args:
                key (str): the key for the record to be saved
                value (*): the value for the record to be saved
        """
        self.db[key] = value

    def open_db(self):
        """ Opens the db file to be accessed """
        self.db = shelve.open(DB_PATH)

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
        self.listener = Listener()
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
            hits = getattr(tracker, counter)

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


class TrackParser(argparse.ArgumentParser):
    """ Custom arguments parser """
    def error(self, message):
        """
            Custom error output method

            Args:
                message (str): message to be displayed
        """
        link = "https://github.com/patillacode/twitter-race"
        sys.stderr.write('\nerror: {0}\n\n'.format(message))
        self.print_help()
        sys.stderr.write('\nPlease check the README or go to {0}\n\n'.format(
            link))
        sys.exit(2)

if __name__ == '__main__':

    try:
        parser = TrackParser()
        mandatory = parser.add_argument_group("mandatory arguments")
        mandatory.add_argument('--hashtags',
                               required=True,
                               nargs='*',
                               help="")
        parser.add_argument("-d",
                            "--db",
                            required=False,
                            default="database.db",
                            help="Path for the database file \
                                  [default: database.db]")
        parser.add_argument("-v",
                            "--verbose",
                            required=False,
                            action="store_true",
                            default=False,
                            help="Show table with live data \
                                 [default: False]")

        args = parser.parse_args()

    except:
        logging.error(traceback.format_exc())
        sys.exit(2)

    try:
        # Set up DB path
        DB_PATH = args.db
        # Create Tracker with given hashtags
        tracker = Tracker(args.verbose, args.hashtags)
        stream = tracker.authenticate()
        # open db
        tracker.open_db()
        # Capture data by the keywords
        stream.filter(track=tracker.hashtags)

    except (KeyboardInterrupt, SystemExit):
        logging.debug("User stopped the process. Farewell my friend!")

    except:
        logging.error(traceback.format_exc())

    finally:
        # Always close db
        tracker.close_db()
