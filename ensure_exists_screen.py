# -*- coding: utf-8 -*-
import subprocess
import re
import sys

if len(sys.argv) != 2:
    print("We need one screen name argument.")
    exit(-1)


def check_screen(screenname):
    if not re.match(r"^[a-zA-z][\w_-]*\w$", screenname):
        print('>>> Invalid screen name:%s' % screenname)
        exit(-1)
        
    cmd='screen -ls'
    p2 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = p2.communicate()[0].decode().strip()

    zz = re.findall(r"\.(%s)\s+" % screenname, output, re.M)
    if 1 == len(zz) and zz[0] == screenname:
        print("Passed: check screen:%s" % screenname)
        return True
    print("Failed: check screen:%s" % screenname)
    if len(zz) > 1:
        print("There are more than two screens with same name:%s" % screenname)
    return False


if not check_screen(sys.argv[1]):
    subprocess.call("screen -dmS %s" % sys.argv[1], shell=True)
    if not check_screen(sys.argv[1]):
        exit(-1)


#zz = re.finditer(r"\.(%s)\s+" % screenname, output, re.M)
#for z in zz:
#    print(z, z.group(1))
    
#print('hello')
#print(output)
#print('hello')

#p=subprocess.run(cmd, shell=True)
#print(p, p.stdout, p.stderr)
