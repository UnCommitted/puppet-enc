#!/usr/bin/env python3

"""
Script to extract information from the enc database
and return an environment and role based on the
hostname given.

classify_node.py <hostname>
"""

from puppetenc.puppetenc import PuppetENC

if __name__ == '__main__':
    """
    Actual application
    """

    app = PuppetENC()
