#!/usr/bin/env python3

import gitlab
import sys

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

    def print_project_stats(self):
        issues = self.project.issues.list(as_list=False)
        merge_requests = self.project.mergerequests.list(as_list=False)

        print('Total issues: {}'.format(issues.total), file=sys.stdout)
        print('Total merge requests: {}'.format(merge_requests.total), file=sys.stdout)

    def print_project_stats_by_milestone(self, milestone):
        issues = self.project.issues.list(milestone=milestone, as_list=False)
        merge_requests = self.project.mergerequests.list(milestone=milestone, as_list=False)

        print('Issues in milestone \'{milestone}\': {issues}'.format(milestone=milestone, issues=issues.total), file=sys.stdout)
        print('Merge requests in milestone \'{milestone}\': {mrs}'.format(milestone=milestone, mrs=merge_requests.total), file=sys.stdout)

    def print_project_stats_by_user(self, username):
        user = self.gl.users.list(username=username)[0]
        issues = self.project.issues.list(author_id=user.id, as_list=False)
        merge_requests = self.project.mergerequests.list(author_id=user.id, as_list=False)

        print('Issues by user \'{username}\': {issues}'.format(username=username, issues=issues.total), file=sys.stdout)
        print('Merge requests by user \'{username}\': {mrs}'.format(username=username, mrs=merge_requests.total), file=sys.stdout)
