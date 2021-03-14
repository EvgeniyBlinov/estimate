#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
import re,string

class EstimateParser(object):
    STR_BEGIN = 'BEGIN';
    STR_END   = 'END';
    STR_HOURS = 'HOURS';
    STR_EPOCH = 'EPOCH';
    STR_TOTAL = 'TOTAL';
    STR_PAID  = 'PAID';
    STR_REST  = 'REST';
    STR_MONEY = 'MONEY';


    def __init__(self):
        self.endof          = 0;
        self.hours_all      = 0;
        self.hour_rate      = 10;
        self.exchange_rate  = 0.0;
        self.hours_per_date = 0;
        self.paid           = 0;
        self.periods        = {}
        self.tags           = {}
        self.operations = {
            re.compile('^set\s+([^=]+)=([^$]+)$') : self.foundOption,
            re.compile('\$\$\$\ *(\d{1,3})')     : self.foundPaid,
            # date format YYYY-mm-dd
            re.compile('(\d{4}-\d{2}-\d{2})')    : self.foundDate,
            re.compile('===\ *(\d{1,3})')        : self.foundHours,
            re.compile('#\s*(END\s+HOURS)\s*#')  : self.setEndOf,
            re.compile('--- (ERA|EPOCH)\s+(END|BEGIN)\s*([^\s][^$]+)$') : self.setPeriod
        }


    def calculate_score(self):
        return (self.hours_all * self.hour_rate) - self.paid


    def setEndOf(self, line, match, matches):
        self.endof = 1


    def foundDate(self, line, match, matches):
        #print("ИТОГО: " + str(self.hours_per_date))
        self.hours_per_date = 0


    def foundHours(self, line, match, matches):
        self.hours_per_date  += int(match)
        self.hours_all       += int(match)
        for tag in re.compile('[^\w]#([-_\w0-9]+)').findall(line):
            if tag not in self.tags:
                self.tags[tag] = 0
            self.tags[tag] += int(match)


    def foundPaid(self, line, match, matches):
        self.paid += int(match)
        print(self.STR_TOTAL + ": " + str(self.hours_all))


    def parseStr(self, x):
        return x.isalpha() and x or x.isdigit() and int(x) or x.isalnum() and x or len(set(string.punctuation).intersection(x)) == 1 and x.count('.') == 1 and float(x) or x


    def foundOption(self, line, match, matches):
        optionName  = matches.group(1).strip(' \t\n\r')
        optionValue = matches.group(2).strip(' \t\n\r')
        optionValue = self.parseStr(optionValue)
        if hasattr(self, optionName):
            if type(getattr(self, optionName)) == type(optionValue):
                setattr(self, optionName, optionValue)


    def setPeriod(self, line, match, matches):
        periodName = matches.group(1)
        periodOp   = matches.group(2)
        periods    = matches.group(3)
        for name in periods.rstrip('\n').split('|'):
            periodFullName = periodName + '_' + name

            if periodFullName not in self.periods:
                self.periods[periodFullName] = {}

            if periodOp == self.STR_BEGIN:
                self.periods[periodFullName]['hours_start'] = self.hours_all
            elif periodOp == self.STR_END:
                self.periods[periodFullName]['hours_end'] = self.hours_all
                self.periods[periodFullName]['hours'] = self.periods[periodFullName]['hours_end'] - self.periods[periodFullName]['hours_start']


    def printPeriods(self):
        for name, period in self.periods.items():
            if 'hours' not in period:
                period['hours'] = self.hours_all - period['hours_start']
            print(name + ': ' + str(period['hours']))


    def printTags(self):
        print('TAGS:')
        tags_all = 0
        for name, tag in self.tags.items():
            tags_all += int(tag)
            print('    ' + name + ': ' + str(tag))
        print('TAGS_TOTAL:' + str(tags_all))


    def printMoney(self):
        print("______________________________________________________")
        print(self.STR_TOTAL + " " + self.STR_HOURS + ": " + str(self.hours_all))
        print(self.STR_TOTAL + " " + self.STR_PAID  + ": " + str(self.paid))
        print(self.STR_TOTAL + " " + self.STR_REST  + ": " + str(self.calculate_score()))
        if self.exchange_rate:
            print(self.STR_TOTAL + " " + self.STR_MONEY + ": " + str(self.calculate_score() * self.exchange_rate))

    def parseText(self, text):
        for line in text:
            if self.endof == 0:
                for regex, callback in self.operations.items():
                    match = regex.search(line)
                    if match and match.group(1):
                        callback(line, match.group(1), match)
                        break
            print(line.rstrip('\n'))
        print("______________________________________________________")
        self.printPeriods()
        self.printTags()
        self.printMoney()
