#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
import sys,getopt
from estimate import EstimateParser

verbose = False
params  = {
    'show': 'all',
    'hours-only': False,
    'hours-done': 0
}


def usage(status = 0):
  global verbose
  print('Usage: '+ os.path.basename(sys.argv[0])+' -i <file1> [option]')
  sys.exit(status)


def main():
    global verbose,params
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hdv",
            ["help", "done", "verbose", "hours-only"]
        )
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage(2)
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-d", "--done"):
            params['show'] = 'done'
        elif o in ("-h", "--hours-only"):
            params['hours-only'] = True
        else:
            assert False, "unhandled option"
            usage()
    parser = EstimateParser()
    parser.parseText(sys.stdin)

if __name__ == "__main__":
    main()
