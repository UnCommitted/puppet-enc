#!/usr/bin/env python3

"""
Script to dump a copy of the ENC database in SQL format into
a specified format
"""

import os
import sys
import sqlite3
import argparse

class App(object):
    """
    Dumps a database to a specified file.
    """

    def __init__(self):
        """
        Actually runs the app
        """
        # Get the configuration
        (self.dbfile, self.outfile) = self.parseargs()

        # Dump the database
        self.dump_database()

    def parseargs(self):
        """
        Get the options from the command line
        """
        parser = argparse.ArgumentParser(
            description='Backup an the ENC database'
        )
        parser.add_argument(
            'dbfile',
            help='Path to the sqlite database to use.'
        )
        parser.add_argument(
            'outfile',
            help='Path to the output sql file'
        )

        args = parser.parse_args()
        return (args.dbfile, args.outfile)

    def dump_database(self):
        """
        Opens the database and runs a dump
        """

        # Check that the dbfile exists, and if so open a connection
        if not os.path.isfile(self.dbfile):
            sys.stderr.write("Could not find DB file " + self.dbfile + "\n")
            sys.exit(1)
        dbconn = sqlite3.connect(self.dbfile)
        with open(self.outfile, 'w') as backup:
            for line in dbconn.iterdump():
                backup.write('%s\n' % line)

if __name__ == '__main__':
    """
    Actual application
    """
    thisapp = App()
