#!/usr/bin/env python3

import calendar
import datetime
import gitlab
import sys

from datetime import timedelta

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

  def print_monthly_issues(self, username, userid, monthname, beforedate, afterdate):
      created_after_date = afterdate.isoformat()
      created_before_date = beforedate.isoformat()
      monthly_issues = self.project.issuesstatistics.get(author_id=userid, created_after=created_after_date, created_before=created_before_date)
      print('Issues by user \'{username}\' in month {monthname}: {issues}'.format(username=username, monthname=monthname, issues=monthly_issues.statistics["counts"]["all"]), file=sys.stdout)

  def print_monthly_mrs(self, username, userid, monthname, beforedate, afterdate):
      created_after_date = afterdate.isoformat()
      created_before_date = beforedate.isoformat()
      monthly_mrs = self.project.mergerequests.list(author_id=userid, created_after=created_after_date, created_before=created_before_date, as_list=False)
      print('Merge requests by user \'{username}\' in month {monthname}: {mrs}'.format(username=username, monthname=monthname, mrs=monthly_mrs.total), file=sys.stdout)

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
      
      for y_idx in range(startdate.year, currentdate.year + 1):
        print("In year {}".format(y_idx))
        # Months in all years in range
        if startdate.year == y_idx and currentdate.year != y_idx:
          # Year of the start date but not the current date
          for m_idx in range(startdate.month, 13):
            after_date = datetime.date(year=y_idx, month=m_idx, day=1) - timedelta(days=1)
            before_date = datetime.date(year=y_idx, month=m_idx, day=calendar.monthrange(y_idx, m_idx)[1]) + timedelta(days=1)

            if m_idx == startdate.month:
              after_date = startdate - timedelta(days=1)

            self.print_monthly_issues(username, user.id, calendar.month_name[m_idx], before_date, after_date)
            self.print_monthly_mrs(username, user.id, calendar.month_name[m_idx], before_date, after_date)
        elif currentdate.year == y_idx and startdate.year != y_idx:
          # Year of the current date but not the start date
          for m_idx in range(1, currentdate.month + 1):
            after_date = datetime.date(year=y_idx, month=m_idx, day=1) - timedelta(days=1)
            before_date = datetime.date(year=y_idx, month=m_idx, day=calendar.monthrange(y_idx, m_idx)[1]) + timedelta(days=1)

            if m_idx == currentdate.month:
              before_date = currentdate + timedelta(days=1)

            self.print_monthly_issues(username, user.id, calendar.month_name[m_idx], before_date, after_date)
            self.print_monthly_mrs(username, user.id, calendar.month_name[m_idx], before_date, after_date)
        else:
          # Year of the current date and the start date
          for m_idx in range(startdate.month, currentdate.month + 1):
            after_date = startdate - timedelta(days=1)
            before_date = currentdate + timedelta(days=1)

            if m_idx != startdate.month:
              after_date = datetime.date(year=startdate.year, month=m_idx, day=1) - timedelta(days=1)

            if m_idx != currentdate.month:
              before_date = datetime.date(year=startdate.year, month=m_idx, day=calendar.monthrange(currentdate.year, m_idx)[1]) + timedelta(days=1)
            
            self.print_monthly_issues(username, user.id, calendar.month_name[m_idx], before_date, after_date)
            self.print_monthly_mrs(username, user.id, calendar.month_name[m_idx], before_date, after_date)
