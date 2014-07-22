"""
Base class for the PuppetENC script.

Takes care of everything except actual classification, which
needs to be taken care of in a method called
classify_host.
"""

import os
import sys
import sqlite3
import argparse
import yaml

class PuppetENC(object):
    """
    Class to classify a node and return the current
    environment and role based on the hostname
    """

    def __init__(self):
        """
        Opens the database and reads information based
        on the hostname
        """

        # Some variables that will be set later
        self.environment = ''
        self.role = ''
        self.hosttags = ()

        # Parse the command line
        self.args = ""
        (self.dbfile, self.hostname) = self.parseargs()

        # Open the db connection
        (self.dbconn, self.db1) = self.opendb()

        # Force foreign keys
        self.db1.execute('PRAGMA foreign_keys = ON;')

        # Get the host environment
        self.get_host_environment()

    def parseargs(self):
        """
        Get the options from the command line
        """
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument(
            '--dbfile',
            default='./db.db',
            help='Name of the sqlite database to use.'
        )
        parser.add_argument(
            'hostname',
            help='hostname/fqdn of the host to classify'
        )

        args = parser.parse_args()
        return (args.dbfile, args.hostname)

    def opendb(self):
        """
        Checks for the existence of the db file,
        then open it into the db variable
        """

        # Check that the dbfile exists, and if so open a connection
        if not os.path.isfile(self.dbfile):
            sys.stderr.write("Could not find DB file " + self.dbfile + "\n")
            sys.exit(1)
        dbconn = sqlite3.connect(self.dbfile)
        return (dbconn, dbconn.cursor())

    def classify_host(self):
        """
        Stub that must be filled in by the subclass
        This class does the actual classification and returns
        the yaml to the puppet master.
        """
        sys.stderr.write("classify_host() method undefined in subclass.\n")
        sys.exit(1)

    def report_classification(self):
        """
        Constructs and returns the yaml required by puppet
        """
        print(
            yaml.dump(
                {
                    'environment': self.environment,
                    'classes': [self.role]
                },
                default_flow_style=False
            )
        )

    def get_host_environment(self):
        """
        Queries the database for the host environment
        """
        # Check that the host actually exists in the database
        # by getting this environment
        self.db1.execute(
            "SELECT env_name FROM host_environments where host_name=?",
            (self.hostname,)
        )

        self.environment = self.db1.fetchone()[0]
        if self.environment == None:
            sys.stderr.write("Host " + self.hostname + " is not known\n")
            sys.exit(1)

    def check_single_tag(self, tagname):
        """
        Checks the host for a single tag
        """
        self.db1.execute(
            "SELECT count(*) FROM hosttag_mappings WHERE "
            "    host_name=? "
            "    AND "
            "    tag_name=?",
            (self.hostname, tagname)
        )
        return self.db1.fetchone()[0] == 1

