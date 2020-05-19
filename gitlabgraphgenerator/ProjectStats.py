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

class GenProjectStats:
  """Generates a graph of project statistics by type."""

  def __init__(self, projectid, configpath=None, servername=None):
    self.projectid = projectid

    if configpath is not None:
      if servername is not None:
        self.gl = gitlab.Gitlab.from_config(servername, [configpath])
      else:
        self.gl = gitlab.Gitlab.from_config(config_files=[configpath])
    else:
      self.gl = gitlab.Gitlab.from_config('gitlab.com', ['data/example.cfg'])

    self.project = self.gl.projects.get(self.projectid)

  def print_monthly_issues(self, userid, monthname, beforedate, afterdate):
    created_after_date = afterdate.isoformat()
    created_before_date = beforedate.isoformat()
    monthly_issues = self.project.issuesstatistics.get(author_id=userid, created_after=created_after_date, created_before=created_before_date)
    print('  Issues in month {monthname}: {issues}'.format(monthname=monthname, issues=monthly_issues.statistics["counts"]["all"]), file=sys.stdout)

  def print_monthly_mrs(self, userid, monthname, beforedate, afterdate):
    created_after_date = afterdate.isoformat()
    created_before_date = beforedate.isoformat()
    monthly_mrs = self.project.mergerequests.list(author_id=userid, created_after=created_after_date, created_before=created_before_date, as_list=False)
    print('  Merge requests in month {monthname}: {mrs}'.format(monthname=monthname, mrs=monthly_mrs.total), file=sys.stdout)

  def print_monthly_commits(self, userid, monthname, beforedatetime, afterdatetime):
    created_after_datetime = afterdatetime.isoformat()
    created_before_datetime = beforedatetime.isoformat()
    monthly_commits = self.project.commits.list(author_id=userid, since=created_after_datetime, until=created_before_datetime, as_list=False)
    print('  Commits in month {monthname}: {commits}'.format(monthname=monthname, commits=monthly_commits.total), file=sys.stdout)

  def print_project_stats(self):
    issue_stats = self.project.issuesstatistics.get()
    merge_requests = self.project.mergerequests.list(as_list=False)

    print('Total issues: {}'.format(issue_stats.statistics["counts"]["all"]), file=sys.stdout)
    print('Total merge requests: {}'.format(merge_requests.total), file=sys.stdout)

  def print_project_stats_by_user(self, username):
    user = self.gl.users.list(username=username)[0]
    issue_stats = self.project.issuesstatistics.get(author_id=user.id)
    merge_requests = self.project.mergerequests.list(author_id=user.id, as_list=False)

    print('Issues by user \'{username}\': {issues}'.format(username=username, issues=issue_stats.statistics["counts"]["all"]), file=sys.stdout)
    print('Merge requests by user \'{username}\': {mrs}'.format(username=username, mrs=merge_requests.total), file=sys.stdout)

  def print_project_stats_by_user_by_month(self, username, startdate):
    user = self.gl.users.list(username=username)[0]
    currentdate = datetime.date.today()

    date_ranges = get_monthly_date_ranges(startdate, currentdate)

    print('Project stats for {}:'.format(username))

    for month_name, after_date, before_date in date_ranges:
      self.print_monthly_issues(user.id, month_name, before_date, after_date)
      self.print_monthly_mrs(user.id, month_name, before_date, after_date)
      self.print_monthly_commits(user.id, month_name, datetime.datetime(year=before_date.year, month=before_date.month, day=before_date.day), datetime.datetime(year=after_date.year, month=after_date.month, day=after_date.day))
