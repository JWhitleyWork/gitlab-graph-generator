#!/usr/bin/env python3

import datetime
import sys

from GroupStats import GenGroupStats

if __name__ == "__main__":
    proj = GenGroupStats(5217727)

    proj.print_group_stats()
    print('\r', file=sys.stdout)
    proj.print_group_stats_by_user('JWhitleyWork')
    print('\r', file=sys.stdout)
    proj.print_group_stats_by_user_by_month('JWhitleyWork', datetime.date(year=2020, month=2, day=17))
