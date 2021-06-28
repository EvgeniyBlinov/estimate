#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
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
        usageMsg = 'Usage: '+ os.path.basename(sys.argv[0])+' -i <file1> [option]' + "\n"
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
        self.parser.parseText(sys.stdin)


if __name__ == "__main__":
    cli = CliRunner()
    cli.run()
