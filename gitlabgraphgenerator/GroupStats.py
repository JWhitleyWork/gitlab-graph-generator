#!/usr/bin/env python3

import calendar
import datetime
import gitlab
import sys

from datetime import timedelta

def get_monthly_date_ranges(startdate, enddate):
    dates = []

    for y_idx in range(startdate.year, enddate.year + 1):
      # Months in all years in range
      if startdate.year == y_idx and enddate.year != y_idx:
        # Year of the start date but not the end date
        for m_idx in range(startdate.month, 13):
          after_date = datetime.date(year=y_idx, month=m_idx, day=1) - timedelta(days=1)
          before_date = datetime.date(year=y_idx, month=m_idx, day=calendar.monthrange(y_idx, m_idx)[1]) + timedelta(days=1)

          if m_idx == startdate.month:
            after_date = startdate - timedelta(days=1)

          dates.append((calendar.month_name[m_idx], after_date, before_date))
      elif enddate.year == y_idx and startdate.year != y_idx:
        # Year of the end date but not the start date
        for m_idx in range(1, enddate.month + 1):
          after_date = datetime.date(year=y_idx, month=m_idx, day=1) - timedelta(days=1)
          before_date = datetime.date(year=y_idx, month=m_idx, day=calendar.monthrange(y_idx, m_idx)[1]) + timedelta(days=1)

          if m_idx == enddate.month:
            before_date = enddate + timedelta(days=1)

          dates.append((calendar.month_name[m_idx], after_date, before_date))
      else:
        # Year of the end date and the start date
        for m_idx in range(startdate.month, enddate.month + 1):
          after_date = startdate - timedelta(days=1)
          before_date = enddate + timedelta(days=1)

          if m_idx != startdate.month:
            after_date = datetime.date(year=startdate.year, month=m_idx, day=1) - timedelta(days=1)

          if m_idx != enddate.month:
            before_date = datetime.date(year=startdate.year, month=m_idx, day=calendar.monthrange(enddate.year, m_idx)[1]) + timedelta(days=1)
          
          dates.append((calendar.month_name[m_idx], after_date, before_date))

    return dates

class GenGroupStats:
  """Generates a graph of group statistics by type."""

  def __init__(self, groupid, configpath=None, servername=None):
    self.groupid = groupid

    if configpath is not None:
      if servername is not None:
        self.gl = gitlab.Gitlab.from_config(servername, [configpath])
      else:
        self.gl = gitlab.Gitlab.from_config(config_files=[configpath])
    else:
      self.gl = gitlab.Gitlab.from_config('gitlab.com', ['data/example.cfg'])

    self.group = self.gl.groups.get(self.groupid)

  def print_monthly_issues(self, userid, monthname, beforedate, afterdate):
    created_after_date = afterdate.isoformat()
    created_before_date = beforedate.isoformat()
    monthly_issues = self.group.issues.list(author_id=userid, created_after=created_after_date, created_before=created_before_date, as_list=False)
    print('  Issues in month {monthname}: {issues}'.format(monthname=monthname, issues=monthly_issues.total), file=sys.stdout)

  def print_monthly_mrs(self, userid, monthname, beforedate, afterdate):
    created_after_date = afterdate.isoformat()
    created_before_date = beforedate.isoformat()
    monthly_mrs = self.group.mergerequests.list(author_id=userid, created_after=created_after_date, created_before=created_before_date, as_list=False)
    print('  Merge requests in month {monthname}: {mrs}'.format(monthname=monthname, mrs=monthly_mrs.total), file=sys.stdout)

  def print_group_stats(self):
    issues = self.group.issues.list(as_list=False)
    merge_requests = self.group.mergerequests.list(as_list=False)

    print('Total issues: {}'.format(issues.total), file=sys.stdout)
    print('Total merge requests: {}'.format(merge_requests.total), file=sys.stdout)

  def print_group_stats_by_user(self, username):
    user = self.gl.users.list(username=username)[0]
    issues = self.group.issues.list(author_id=user.id, as_list=False)
    merge_requests = self.group.mergerequests.list(author_id=user.id, as_list=False)

    print('Issues by user \'{username}\': {issues}'.format(username=username, issues=issues.total), file=sys.stdout)
    print('Merge requests by user \'{username}\': {mrs}'.format(username=username, mrs=merge_requests.total), file=sys.stdout)

  def print_group_stats_by_user_by_month(self, username, startdate):
    user = self.gl.users.list(username=username)[0]
    currentdate = datetime.date.today()

    date_ranges = get_monthly_date_ranges(startdate, currentdate)

    print('Group stats for {}:'.format(username))

    for month_name, after_date, before_date in date_ranges:
      self.print_monthly_issues(user.id, month_name, before_date, after_date)
      self.print_monthly_mrs(user.id, month_name, before_date, after_date)
