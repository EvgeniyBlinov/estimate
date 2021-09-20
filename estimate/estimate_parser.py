#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
import re,string
import datetime


class EstimateParser(object):
    STR_BEGIN = 'BEGIN';
    STR_END   = 'END';
    STR_HOURS = 'HOURS';
    STR_EPOCH = 'EPOCH';
    STR_TOTAL = 'TOTAL';
    STR_PAID  = 'PAID';
    STR_REST  = 'REST';
    STR_MONEY = 'MONEY';

    STR_TIME_FORMAT = '%H:%M';
    STR_BEGIN_HOURS_PATTERN = '#\s*(BEGIN\s+HOURS)\s*#';

    STR_PATTERN_TAG = '[^\w]#([-_\w0-9]+)'


    def __init__(self) -> None:
        self.is_hours_line  = 1
        self.endof          = 0
        self.hours_all      = 0
        self.hour_rate      = 10
        self.exchange_rate  = 0.0
        self.hours_per_date = 0
        self.paid           = 0
        self.periods        = {}
        self.tags           = {}
        self.operations = {
            re.compile('---\ *(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})')        : self.foundTime,
            re.compile('^set\s+([^=]+)=([^$]+)$')                        : self.foundOption,
            re.compile('\$\$\$\ *(\d{1,3})')                             : self.foundPaid,
            # date format YYYY-mm-dd
            re.compile('(\d{4}-\d{2}-\d{2})')                            : self.foundDate,
            re.compile('===\ *(\d{1,3}\.?\d?)')                          : self.foundHours,
            re.compile(self.STR_BEGIN_HOURS_PATTERN)                     : self.foundBeginHours,
            re.compile('#\s*(END\s+HOURS)\s*#')                          : self.setEndOf,
            re.compile('--- (ERA|EPOCH)\s+(END|BEGIN)\s*([^\s][^$]+)$')  : self.setPeriod
        }

    def usage(self) -> str:
        usageMsg = 'Patterns:' + "\n"
        usageMsg += ('\tTag pattern\t-\t"%s"' % self.STR_PATTERN_TAG )

        return usageMsg


    def calculate_score(self) -> str:
        return (self.hours_all * self.hour_rate) - self.paid


    def addHours(self, line: str, hours: float) -> None:
        self.hours_per_date  += hours
        self.hours_all       += hours
        for tag in re.compile(self.STR_PATTERN_TAG).findall(line):
            if tag not in self.tags:
                self.tags[tag] = 0
            self.tags[tag] += hours


    def setEndOf(self, line, match, matches) -> None:
        self.endof          = 1
        self.is_hours_line  = 0

        self.printStats()


    def foundBeginHours(self, line, match, matches) -> None:
        self.is_hours_line  = 1

        # clean
        self.hours_all      = 0
        self.hours_per_date = 0
        self.paid           = 0


    def foundDate(self, line, match, matches) -> None:
        #print("TOTAL BY DAY: " + str(self.hours_per_date))
        self.hours_per_date = 0


    def foundTime(self, line, match, matches) -> str:
        time_begin = datetime.datetime.strptime(matches.group(1), self.STR_TIME_FORMAT)
        time_end   = datetime.datetime.strptime(matches.group(2), self.STR_TIME_FORMAT)
        time_delta = time_end - time_begin

        hours,minutes,seconds = map(int, str(time_delta).split(':'))
        # add minutes
        hours += round(int(minutes) / 60, 1)

        self.addHours(line, hours)

        new_line = line.rstrip('\n') + ' === ' + str(hours)
        return new_line


    def foundHours(self, line, match, matches) -> None:
        self.addHours(line, float(match))


    def foundPaid(self, line, match, matches) -> None:
        self.paid += int(match)
        print(self.STR_TOTAL + ": " + str(self.hours_all))


    def parseStr(self, x):
        return x.isalpha() and x or x.isdigit() and int(x) or x.isalnum() and x or len(set(string.punctuation).intersection(x)) == 1 and x.count('.') == 1 and float(x) or x


    def foundOption(self, line, match, matches) -> None:
        optionName  = matches.group(1).strip(' \t\n\r')
        optionValue = matches.group(2).strip(' \t\n\r')
        optionValue = self.parseStr(optionValue)
        if hasattr(self, optionName):
            if type(getattr(self, optionName)) == type(optionValue):
                setattr(self, optionName, optionValue)


    def setPeriod(self, line, match, matches) -> None:
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


    def printPeriods(self) -> None:
        for name, period in self.periods.items():
            if 'hours' not in period:
                period['hours'] = self.hours_all - period['hours_start']
            print(name + ': ' + str(period['hours']))


    def printTags(self) -> None:
        print('TAGS:')
        tags_all = 0
        for name, tag in self.tags.items():
            tags_all += int(tag)
            print('    ' + name + ': ' + str(tag))
        print('TAGS_TOTAL:' + str(tags_all))


    def printMoney(self) -> None:
        print("______________________________________________________")
        print(self.STR_TOTAL + " " + self.STR_HOURS + ": " + str(self.hours_all))
        print(self.STR_TOTAL + " " + self.STR_PAID  + ": " + str(self.paid))
        print(self.STR_TOTAL + " " + self.STR_REST  + ": " + str(self.calculate_score()))
        exchange_rate = self.exchange_rate
        if not exchange_rate:
            exchange_rate = 1
        print(self.STR_TOTAL + " " + self.STR_MONEY + ": " + str(self.calculate_score() * exchange_rate))


    def printStats(self) -> None:
        print("______________________________________________________")
        self.printPeriods()
        self.printTags()
        self.printMoney()


    def parseText(self, text) -> None:
        for line in text:
            if self.endof == 0:
                for regex, callback in self.operations.items():
                    match = regex.search(line)
                    if match and match.group(1):
                        result = callback(line, match.group(1), match)
                        if result:
                            line = result
                        break
            print(line.rstrip('\n'))

        # print stats if END HOURS not found
        if self.endof == 0:
            self.printStats()
