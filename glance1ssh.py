#!/usr/bin/python
from __future__ import print_function
import os, subprocess 
import sys, time

#check and correct this!
SSHBINARY = '/usr/bin/ssh'
SCPBINARY = '/usr/bin/scp'
HOSTLIST  = 'glance1.list'
REMOTEDIR    = ''
#REMOTEDIR = '/tmp/' # should start AND end with "/" 

#do not touch!
NOMYKEY  = "-oPubkeyAuthentication=no"
NOKHOSTS = "-oUserKnownHostsFile=/dev/null"
NOHCHECK = "-oStrictHostKeyChecking=no"
CATPASS   = "catpass.py"  # TODO: use __import__() from this variable
REMOTESCRIPT = "glance1.script"
REMOTEPICK   = "glance1.tgz"

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

def scpcmd(port,wherefrom,whereto,password):
    env0 = {'SSH_ASKPASS': CATPASS, 'DISPLAY':':9999'}
    dropbox(password)
    ssh = subprocess.Popen([SCPBINARY,"-P %d" % port,
        NOHCHECK, NOKHOSTS, NOMYKEY, wherefrom, whereto],
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
        whereto="{u}@{h}:{d}".format(u=user, h=host,d=REMOTEDIR)
        wherefrom=REMOTESCRIPT
        rcmd = "{rdir}./{rscript}".format(rdir=REMOTEDIR, rscript=REMOTESCRIPT)
        
        result,error = scpcmd(port, wherefrom, whereto, password)
        print("coping to remote host, result: {r}, errors: {e}".format(r=result,e=error))

        result,error = sshcmd(host, port, user, password, rcmd)
        print("calling remote script, result: {r}, errors: {e}".format(r=result,e=error))

        print("waiting")
        time.sleep(2)
        
        whereto="./glance-{h}.tgz".format(h=host)
        wherefrom="{u}@{h}:{d}{result}".format(u=user,h=host,d=REMOTEDIR,result=REMOTEPICK)
        
        result,error = scpcmd(port, wherefrom, whereto, password)
        print("coping from remote host, result: {r}, errors: {e}".format(r=result,e=error))
        
        rcmd = "rm {d}./{rscript} {d}{result}".format(d=REMOTEDIR, rscript=REMOTESCRIPT,result=REMOTEPICK)
        result,error = sshcmd(host, port, user, password, rcmd)
        print("removing script and archive from remote host, result: {r}, errors: {e}".format(r=result,e=error))

    # TODO: rm glance1.dropbox    
    return(0)

if __name__ == '__main__' :
    exit(mainloop())
