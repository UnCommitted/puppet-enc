#!/usr/bin/env python3

"""
Script to extract information from the enc database
and return an environment and role based on the
hostname given.

classify_node.py <hostname>
"""

import sys
from puppetenc.puppetenc import PuppetENC

class HPCPuppetENC(PuppetENC):
    """
    HPC node classification class
    """

    def __init__(self):
        """
        Initialize this object using PuppetENC
        """
        PuppetENC.__init__(self)
        self.classify_host()

    def classify_host(self):
        """
        Classify the hostname given on the command line
        """

        # Check if we are a puppet master
        if self.check_single_tag('puppetmaster'):
            self.role = 'roles::puppetmaster'
            self.report_classification()
            sys.exit(0)

        # Check if we are apt repository
        if self.check_single_tag('apt_repo_host'):
            self.role = 'roles::apt_repo_host'
            self.report_classification()

        # # Check if we are a puppet master
        # self.db1.execute(
        #     "SELECT count(*) FROM hosttag_mappings WHERE "
        #     "host_name=? AND ("
        #     "tag_name=? OR "
        #     "tag_name=?)",
        #     (self.hostname, 'puppetmaster', 'apt-repo-host')
        # )
        # self.db1.fetchone()[0])

if __name__ == '__main__':
    """
    Actual application
    """

    app = HPCPuppetENC()
