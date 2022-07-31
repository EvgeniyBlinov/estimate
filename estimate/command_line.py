#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ._version import __version__


from typing import Callable
import sys,os,getopt
from .estimate_parser import EstimateParser
import argparse
import re
import subprocess

class TrackerCmd(object):

    """Docstring for TrackerCmd. """

    def __init__(self):
        self.trackerProgramm = '~/.local/bin/youtrack.sh'
        self.taskIdRe = re.compile('^([A-Z]+-[0-9]+) ')
        self.track_type = ''

    def track(self, line: str, ep: EstimateParser) -> str:
        """docstring for track"""
        trackerCmd = '%s %s %s %s "%s" "%s"' % (self.trackerProgramm, self.getTaskId(line), self.getTime(ep.cursor_hours), ep.cursor_date, self.track_type, line)
        result = subprocess.check_output(trackerCmd, stderr=subprocess.STDOUT, shell=True)
        status = 'not_logged'
        if str(result).find('WorkItem created') != -1:
            status = 'logged'
        loggedStr = line.rstrip('\n') + ' !' + status
        return loggedStr

    def getTime(self, time: str) -> str:
        """docstring for getTime"""
        timeList = time.split('.')
        hours = timeList[0]
        minutes = 0
        if len(timeList) > 1:
            minutes = int(timeList[1]) * 6
        timeStr = "%dh%dm" % (int(hours), int(minutes))
        return timeStr


    def getTaskId(self, line: str) -> str:
        """docstring for getTaskId"""
        taskIdMatch = self.taskIdRe.search(line)
        return taskIdMatch.group(1)


class CliRunner(object):

    def __init__(self):
        self.ARGS = "hdvHST"

        self.verbose = False
        self.params  = {
            'show': 'all',
            'hours-only': False,
            'show-stats': True,
            'track-time': False,
            'hours-done': 0
        }
        self.parser = EstimateParser()
        self.parse_args()


    def parse_args(self):
      parser = argparse.ArgumentParser(description='estimate')

      parser.add_argument(
          '-V', '--version',
          action='version',
          version='%(prog)s {version}'.format(version=__version__))

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

      parser.add_argument(
          "-T", "--track-time",
          help="Track time to plugin",
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
      if args.track_time:
        self.params['track-time'] = True

      self.infile = args.infile


    def getTracker(self) -> Callable:
        """docstring for getTracker"""
        callback = None
        if self.params['track-time']:
            callback = TrackerCmd()
        return callback


    def run(self):
        self.parser.tracker = self.getTracker()
        self.parser.show_stats = int(self.params['show-stats'])
        self.parser.parseText(self.infile)


def main():
    cli = CliRunner()
    cli.run()

if __name__ == "__main__":
    main()
