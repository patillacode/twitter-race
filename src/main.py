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
import argparse
import sys
import logging
import traceback

from models import Tracker


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

    logging.basicConfig(filename='track.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

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
        # Create Tracker with given hashtags
        tracker = Tracker(args.verbose, args.hashtags)
        stream = tracker.authenticate()
        # open db
        tracker.open_db(args.db)
        # Capture data by the keywords
        stream.filter(track=tracker.hashtags)

    except (KeyboardInterrupt, SystemExit):
        logging.debug("User stopped the process. Farewell my friend!")

    except:
        logging.error(traceback.format_exc())

    finally:
        # Always close db
        tracker.close_db()
