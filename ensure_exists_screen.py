# -*- coding: utf-8 -*-
import subprocess
import re
import sys
import argparse

parser = argparse.ArgumentParser(description='check screen exists or not and create it')
parser.add_argument('-c', '--check', action='store_true', help='check screen exists only.')
parser.add_argument("screenname", help='screen name')
opts = parser.parse_args()

    
def check_screen(screenname):
    if not re.match(r"^[a-zA-z][\w_-]*\w$", screenname):
        print('>>> Invalid screen name:%s' % screenname)
        exit(-1)
        
    p2 = subprocess.Popen(['screen', '-ls'], stdout=subprocess.PIPE)
    output = p2.communicate()[0].decode().strip()

    zz = re.findall(r"\.(%s)\s+" % screenname, output, re.M)
    if 1 == len(zz) and zz[0] == screenname:
        print("Passed to check screen:%s" % screenname)
        return True
    print("Failed to check screen:%s" % screenname)
    if len(zz) > 1:
        print("There are more than two screen with same name:%s" % screenname)
    return False
    
if not check_screen(opts.screenname):
    if not opts.check:
        subprocess.call("screen -dmS %s" % opts.screenname, shell=True)
        if not check_screen(opts.screenname):
            exit(-1)
    else:
        exit(-1)

