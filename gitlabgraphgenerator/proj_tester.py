#!/usr/bin/env python3

import datetime
import sys

from ProjectStats import GenProjectStats

if __name__ == "__main__":
    proj = GenProjectStats(8229519)

    proj.print_project_stats()
    print('\r', file=sys.stdout)
    proj.print_project_stats_by_user('JWhitleyWork')
    print('\r', file=sys.stdout)
    proj.print_project_stats_by_user_by_month('JWhitleyWork', datetime.date(year=2020, month=2, day=17))
