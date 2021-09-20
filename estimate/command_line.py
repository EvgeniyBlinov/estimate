#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys,os,getopt
from estimate import EstimateParser


class CliRunner(object):


    def __init__(self):
        self.verbose = False
        self.params  = {
            'show': 'all',
            'hours-only': False,
            'hours-done': 0
        }
        self.parser = EstimateParser()


    def usage(self, status = 0):
        """Print usage and exit"""
        filename = os.path.basename(sys.argv[0])
        if not filename:
            filename = 'estimate'
        usageMsg = 'Usage: ' + filename + ' <file>' + "\n"
        usageMsg += self.parser.usage()
        print(usageMsg)
        sys.exit(status)


    def run(self):
        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                "hdvH",
                ["help", "done", "verbose", "hours-only"]
            )
        except getopt.GetoptError as err:
            # print help information and exit:
            print(str(err)) # will print something like "option -a not recognized"
            self.usage(2)


        for o, a in opts:
            if o == "-v":
                self.verbose = True
            elif o in ("-h", "--help"):
                self.usage()
            elif o in ("-d", "--done"):
                self.params['show'] = 'done'
            elif o in ("-H", "--hours-only"):
                self.params['hours-only'] = True
            else:
                assert False, "unhandled option"
                self.usage()

        # @TODO:  <20-09-21, Evgeniy Blinov <evgeniy_blinov@mail.ru>> :
        if args:
            file = args.pop()
            if file in ('-', '/dev/stdin'):
                self.parser.parseText(sys.stdin)
            else:
                with open(file, 'r') as f:
                    self.parser.parseText(f)
        else:
            self.parser.parseText(sys.stdin)


def main():
    cli = CliRunner()
    cli.run()

if __name__ == "__main__":
    cli = CliRunner()
    cli.run()
