#!/usr/bin/env python
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
# version         :0.1
# usage           :python track.py <hashtag#1> <hashtag#2> ... <hashtag#n>
# notes           :
# python_version  :2.7.10
# =============================================================================

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

DB_PATH = 'track.db'


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
                    # store it in database
                    tracker.set_data(counter, hits)
                    # store whole tweet in database
                    tracker.set_data(str(data['id']), data)
                    # show results table in console
                    tracker.results_table()
        return True

    def on_error(self, status):
        print "Error: {0}".format(status)


class Tracker():
    def __init__(self, hashtags=[]):
        # Confirm hashtags are given in a list
        try:
            assert(isinstance(hashtags, list))
        except AssertionError:
            sys.exit(2)

        # Set all known attributes
        self.db = None
        self.stream = None
        self.listener = None
        self.hashtags = hashtags
        self.set_longest_hashtag()
        # Set a list for all known attributes
        self.set_known_items()

        # Set dynamic attributes (counters for each hashtag)
        for h in self.hashtags:
            setattr(self, "{0}_counter".format(h), 0)

    def set_known_items(self):
        self.known_items = []
        for k, v in self.__dict__.iteritems():
            self.known_items.append(k)

    def set_data(self, key, value):
        self.db[key] = value

    def open_db(self):
        self.db = shelve.open(DB_PATH)

    def close_db(self):
        self.db.close()

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

    def results_table(self):
        # clear console
        os.system('clear')
        # define stuff for console output
        cell_size = (self.longest + 2)
        counter_whitespace = " " * ((cell_size - 5) / 2)
        border = "-" * ((cell_size * 2) + 1)

        # print table top border
        print " {0} ".format(border)
        # Grab all counters and print their value
        for k, v in self.__dict__.iteritems():
            if k not in self.known_items:
                # For better output we calculate the whitespace necessary
                # depending on each hashtag length
                hashtag_whitespace = " " * (self.longest - len(k) + 9)
                # print out the hashtaga and its counter value
                print "| {0}{1} |{2}{3}{2}|".format(k[:-8],
                                                    hashtag_whitespace,
                                                    counter_whitespace,
                                                    str(v).zfill(5))
        # print table bottom border
        print " {0} ".format(border)


def usage():
    print "Usage:"
    print "\tpython track.py <hashtag#1> <hashtag#2> ... <hashtag#n>\n"
    sys.exit(2)


if __name__ == '__main__':

    try:
        if len(sys.argv[1:]) < 1:
            usage()

        hashtags = list()
        # list of hashtags to track
        for a in sys.argv[1:]:
            hashtags.append(str(a))

        # Create Tracker with given hastags
        tracker = Tracker(hashtags)
        stream = tracker.authenticate()
        # open db - DB is not accesible during the execution to avoid
        # 'Resource temporarily unavailable' issues when it's hit a lot
        tracker.open_db()

        # Capture data by the keywords
        stream.filter(track=tracker.hashtags)

    except:
        pass

    finally:
        # Always close db
        tracker.close_db()
