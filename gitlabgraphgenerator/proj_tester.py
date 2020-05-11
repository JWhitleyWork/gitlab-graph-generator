#!/usr/bin/env python3

import sys

from ProjectStats import GenProjectStats

if __name__ == "__main__":
    proj = GenProjectStats(8229519)

    proj.print_project_stats()
    print('\r', file=sys.stdout)
    proj.print_project_stats_by_milestone('AVP MS2: Follow waypoints with the ndt_localizer')
    print('\r', file=sys.stdout)
    proj.print_project_stats_by_user('JWhitleyWork')
