from __future__ import print_function
import sys
def msg(s): print (s)
def dashes(char='-'): msg(40*char)
def msgt(s): dashes(); msg(s); dashes()
def msgx(s): dashes('='); msg(s); dashes('='); sys.exit(0)

"""

curl -H "Content-type:application/json" -X POST -d user_params.json "http://dvn-build.hmdc.harvard.edu/api/users?password=linus"
"""
