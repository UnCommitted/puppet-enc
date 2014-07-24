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
        self.site = ''
        self.role = ''
        self.hosttags = ()

        # Parse the command line
        self.args = ""
        (self.dbfile, self.hostname) = self.parseargs()

        # Open the db connection
        (self.dbconn, self.db1) = self.opendb()

        # Force foreign keys
        self.db1.execute('PRAGMA foreign_keys = ON;')

        # Report the classification
        self.report_classification()

    def parseargs(self):
        """
        Get the options from the command line
        """
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument(
            '--dbfile',
            default='./puppet-enc.db',
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


    def report_classification(self):
        """
        Queries the database, and builds a role and environment.
        Constructs and returns the yaml required by puppet
        """
        # Check that the host actually exists in the database
        # by getting this environment
        self.db1.execute(
            "SELECT "
            "    env_name,"
            "    site_name,"
            "    system_name,"
            "    role_name "
            "FROM hostoverview "
            "WHERE host_name=?",
            (self.hostname,)
        )

        result = self.db1.fetchone()
        if result == None:
            # Return the default unknown host role.
            # This role should report that it is an unknown host
            print(
                yaml.dump(
                    {
                        'classes': ['roles::unknown_role']
                    },
                    default_flow_style=False
                )
            )
        else:
            # Read the values
            (environment, site_name, system_name, role_name) = result
            print(
                yaml.dump(
                    {
                        'environment': environment,
                        'classes': [
                            'roles::'
                            + system_name
                            + "::"  + role_name
                        ],
                        'parameters': {
                            'site': site_name
                        }
                    },
                    default_flow_style=False
                )
            )

