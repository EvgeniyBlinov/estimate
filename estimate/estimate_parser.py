#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 ft=python
from typing import Callable
import re,string
import datetime
from re import Match
from .project import Project
import os
import io

# @TODO:  <31-03-23, Evgeniy Blinov <evgeniy_blinov@mail.ru>> : DEBUG
from pprint import pprint
import sys


class EstimateParser(object):
    STR_BEGIN   = 'BEGIN';
    STR_END     = 'END';
    STR_PROJECT = 'PROJECT';
    STR_HOURS   = 'HOURS';
    STR_EPOCH   = 'EPOCH';
    STR_TOTAL   = 'TOTAL';
    STR_PAID    = 'PAID';
    STR_REST    = 'REST';
    STR_MONEY   = 'MONEY';

    STR_TIME_FORMAT = '%H:%M';
    STR_BEGIN_HOURS_PATTERN = '#\s*(BEGIN\s+HOURS)\s*#';

    STR_PATTERN_TAG = '[^\w]#([-_\w0-9]+)'


    def __init__(self) -> None:
        self.show_hours_per_date = 0
        self.show_stats          = 1
        self.projects            = {}

        self.operations = {
            re.compile('---\s*(logged)\s*---')                           : self.foundLogged,
            re.compile('---\ *(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})')        : self.foundTime,
            re.compile('^set\s+([^=]+)=([^$]+)$')                        : self.foundOption,
            re.compile('\$\$\$\ *(\d{1,3})')                             : self.foundPaid,
            # date format YYYY-mm-dd
            re.compile('(\d{4}-\d{2}-\d{2})')                            : self.foundDate,
            re.compile('===\ *(\d{1,3}\.?\d?)')                          : self.foundHours,
            re.compile(self.STR_BEGIN_HOURS_PATTERN)                     : self.foundBeginHours,
            re.compile('#\s*(END\s+HOURS)\s*#')                          : self.setEndOf,
            re.compile('--- (PROJECT)\s+(END|BEGIN)\s*([-a-zA-Z0-9_]+)\s*([^\s][^$]+)$')    : self.setProject,
            re.compile('--- (ERA|EPOCH)\s+(END|BEGIN)\s*([^\s][^$]+)$')  : self.setPeriod
        }

        self.tracker = None

    def usage(self) -> str:
        usageMsg = 'Patterns:' + "\n"
        usageMsg += ('\tTag pattern\t-\t"%s"' % self.STR_PATTERN_TAG )

        return usageMsg


    def addHours(self, project: Project, line: str, hours: float) -> None:
        project.hours_per_date  += hours
        project.hours_all       += hours
        for tag in re.compile(self.STR_PATTERN_TAG).findall(line):
            if tag not in project.tags:
                project.tags[tag] = 0
            project.tags[tag] += hours


    def setEndOf(self, project: Project, line: str, match, matches) -> None:
        project.endof          = 1
        project.is_hours_line  = 0

        if not project.is_subproject:
            self.printStats()


    def foundLogged(self, project: Project, line: str, match, matches):
        project.logged_found = 1


    def foundBeginHours(self, project: Project, line: str, match, matches) -> None:
        project.is_hours_line  = 1

        # clean
        project.hours_all      = 0
        project.hours_per_date = 0
        project.paid           = 0


    def setEndDate(self, project: Project) -> None:
        if self.show_hours_per_date and not project.silent:
            if project.hours_per_date > 0:
                print("TOTAL BY DAY: " + str(project.hours_per_date))
        project.hours_per_date = 0


    def foundDate(self, project: Project, line: str, match, matches: Match) -> None:
        project.cursor_date = matches.group(1)
        self.setEndDate(project)


    def foundTime(self, project: Project, line: str, match, matches) -> str:
        time_begin = datetime.datetime.strptime(matches.group(1), self.STR_TIME_FORMAT)
        time_end   = datetime.datetime.strptime(matches.group(2), self.STR_TIME_FORMAT)
        time_delta = time_end - time_begin

        hours,minutes,seconds = map(int, str(time_delta).split(':'))
        # add minutes
        hours += round(int(minutes) / 60, 1)

        ## do not add hours if exists
        new_line = line.rstrip('\n')
        hours_fixed = re.compile('===\ *(\d{1,3}\.?\d?)').search(line)
        if hours_fixed and hours_fixed.group(1):
            ## set hours from fixed
            hours = float(hours_fixed.group(1))
            project.cursor_hours = hours
            if self.tracker and project.logged_found == 1:
                current_logged = re.compile('(!logged)').search(line)
                if not (current_logged and current_logged.group(1)):
                    new_line = self.tracker.track(line.rstrip('\n'), self)
        else:
            new_line = line.rstrip('\n') + ' === ' + str(hours)

        self.addHours(project, line, hours)

        return new_line


    def foundHours(self, project: Project, line: str, match, matches) -> None:
        self.addHours(project, line, float(match))


    def foundPaid(self, project: Project, line: str, match, matches) -> None:
        project.paid += int(match)
        print(self.STR_TOTAL + ": " + str(project.hours_all))


    def parseStr(self, x):
        return x.isalpha() and x or x.isdigit() and int(x) or x.isalnum() and x or len(set(string.punctuation).intersection(x)) == 1 and x.count('.') == 1 and float(x) or x


    def foundOption(self, project: Project, line: str, match, matches) -> None:
        optionName  = matches.group(1).strip(' \t\n\r')
        optionValue = matches.group(2).strip(' \t\n\r')
        optionValue = self.parseStr(optionValue)
        if hasattr(project, optionName):
            if type(getattr(project, optionName)) == type(optionValue):
                setattr(project, optionName, optionValue)


    def setProject(self, project: Project, line: str, match, matches) -> None:
        projectCursor = matches.group(2).strip()
        projectName = matches.group(3).strip()
        projectFilePath = matches.group(4).strip()
        if projectCursor == self.STR_BEGIN:
            project = Project(projectName)
            project.silent = 1
            project.is_subproject = 1
            self.projects[projectName] = project

            with open(os.path.expanduser(projectFilePath)) as pf:
                self.parseEstimateText(self.projects[projectName], pf)


    def setPeriod(self, project: Project, line: str, match, matches) -> None:
        periodName = matches.group(1)
        periodOp   = matches.group(2)
        periods    = matches.group(3)
        for name in periods.rstrip('\n').split('|'):
            periodFullName = periodName + '_' + name

            if periodFullName not in project.periods:
                project.periods[periodFullName] = {}

            if periodOp == self.STR_BEGIN:
                project.periods[periodFullName]['hours_start'] = project.hours_all
            elif periodOp == self.STR_END:
                project.periods[periodFullName]['hours_end'] = project.hours_all
                project.periods[periodFullName]['hours'] = project.periods[periodFullName]['hours_end'] - project.periods[periodFullName]['hours_start']


    def printPeriods(self, project: Project) -> None:
        for name, period in project.periods.items():
            if 'hours' not in period:
                period['hours'] = project.hours_all - period['hours_start']
            print(name + ': ' + str(period['hours']))


    def printTags(self, project: Project) -> None:
        print('TAGS:')
        tags_all = 0
        for name, tag in project.tags.items():
            tags_all += int(tag)
            print('    ' + name + ': ' + str(tag))
        print('TAGS_TOTAL:' + str(tags_all))


    def printMoney(self, project: Project) -> None:
        print("______________________________________________________")
        print(self.STR_TOTAL + " " + self.STR_HOURS + ": " + str(project.hours_all))
        print(self.STR_TOTAL + " " + self.STR_PAID  + ": " + str(project.paid))
        print(self.STR_TOTAL + " " + self.STR_REST  + ": " + str(project.calculate_score()))
        exchange_rate = project.exchange_rate
        if not exchange_rate:
            exchange_rate = 1
        print(self.STR_TOTAL + " " + self.STR_MONEY + ": " + str(project.calculate_score() * exchange_rate))


    def printStats(self) -> None:
        for projectName, project in self.projects.items():
            if self.show_stats:
                print("______________________________________________________")
                print(self.STR_PROJECT + " " + project.name)
                print("______________________________________________________")
                self.printPeriods(project)
                self.printTags(project)
                self.printMoney(project)
                print("______________________________________________________")


    def parseEstimateText(self, project: Project, text: io.TextIOWrapper) -> None:
        for line in text:
            if project.endof == 0:
                for regex, callback in self.operations.items():
                    match = regex.search(line)
                    if match and match.group(1):
                        result = callback(project, line, match.group(1), match)
                        if result is not None:
                            line = result
                        break

            if not project.silent:
                print(line.rstrip('\n'))


    def parseText(self, text) -> None:
        defaultProjectName = 'main'
        self.projects[defaultProjectName] = Project(defaultProjectName)
        self.parseEstimateText(self.projects[defaultProjectName], text)

        # print stats if END HOURS not found
        if self.projects[defaultProjectName].endof == 0:
            self.printStats()

        self.setEndDate(self.projects[defaultProjectName])
