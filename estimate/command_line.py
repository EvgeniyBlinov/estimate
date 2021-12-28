#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys,os,getopt
from estimate import EstimateParser
import argparse


class CliRunner(object):

    def __init__(self):
        self.ARGS = "hdvHS"

        self.verbose = False
        self.params  = {
            'show': 'all',
            'hours-only': False,
            'show-stats': True,
            'hours-done': 0
        }
        self.parser = EstimateParser()
        self.parse_args()


    def parse_args(self):
      parser = argparse.ArgumentParser(description='estimate')

      parser.add_argument(
          "-v", "--verbose",
          help="increase output verbosity",
          action="store_true")

      parser.add_argument(
          "-d", "--done",
          help="show done",
          action="store_true")

      parser.add_argument(
          "-D", "--show-day-hours",
          help="show hours per date",
          action="store_true")

      parser.add_argument(
          "-H", "--hours-only",
          help="show hours only",
          action="store_true")

      parser.add_argument(
          "-S", "--without-stats",
          help="Don't show stats",
          action="store_true")

      parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
            default=sys.stdin)

      args = parser.parse_args()

      if args.verbose:
        self.verbose = True
      if args.done:
        self.params['show'] = 'done'
      if args.show_day_hours:
        self.parser.show_hours_per_date = 1
      if args.hours_only:
        self.params['hours-only'] = True
      if args.without_stats:
        self.params['show-stats'] = False

      self.infile = args.infile


    def run(self):
        self.parser.show_stats = int(self.params['show-stats'])
        self.parser.parseText(self.infile)


def main():
    cli = CliRunner()
    cli.run()

if __name__ == "__main__":
    main()
