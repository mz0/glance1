#!/usr/bin/python
from __future__ import print_function
import os, subprocess 
import sys, time

#check and correct this!
SSHBINARY = '/usr/bin/ssh'
HOSTLIST  = 'glance1.list'

#do not touch!
NOMYKEY  = "-oPubkeyAuthentication=no"
NOKHOSTS = "-oUserKnownHostsFile=/dev/null"
NOHCHECK = "-oStrictHostKeyChecking=no"
CATPASS   = "catpass.py"

import catpass

def dropbox(str0):
    try :
        dropbox=file(catpass.DROPBOX,"w")
        dropbox.write(str0)
        dropbox.close()
    except IOError as msg :
        return "Writing into dropbox %s: %s" % (catpass.DROPBOX, msg.strerror)

def delwarn0(errors):
    if errors[0].find("ermanently added ") > 0 : return errors[1:]
   
def sshcmd(host,port,user,password,cmd):
    env0 = {'SSH_ASKPASS': CATPASS, 'DISPLAY':':9999'}
    dropbox(password)
    ssh = subprocess.Popen([SSHBINARY,"-T","-p %d" % port,
        NOHCHECK, NOKHOSTS, NOMYKEY, "%s@%s" % (user,host), cmd],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=env0,
    preexec_fn=os.setsid
    )
    result = ssh.stdout.readlines()
    error = ssh.stderr.readlines()
    return result,delwarn0(error)

def hpupa(str0):
    host,port,user,password = str0.split()
    return host,int(port),user,password

def mainloop():
    try :
        hostlist = open(HOSTLIST,'r')
    except IOError as msg:
        sys.stderr.write("Error opening list of hosts %s: %" % (HOSTLIST, msg.strerror))
        return(1)
    
    for line in hostlist:
        if line.startswith('#') : continue
        host,port,user,password = hpupa(line)
        rcmd = "echo $(uname)"
        
        result,error = sshcmd(host, port, user, password, rcmd)
        print("calling remote command, result: {r}, error: {e}".format(r=result,e=error))

    return(0)

if __name__ == '__main__' :
    exit(mainloop())
