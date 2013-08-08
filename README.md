Glance1: assessing Linux hosts
==============================

glance1ssh.py is the "driver" script which reads a list of hosts from glance1.list

Each line in that list is like this:

hostN sshPortN sshUserX UserPassX

Lines starting with "#" are ignored.

Driver 

* copies glance1.script to the hostN using scp binary
* calls it remotely via ssh binary
* collects result (named glance1.tgz on hostN) and saves it as hostN-glance1.tgz in the current dir

Password authentication uses ssh ASKPASS mechanics which is implemented with the help of catpass.py
It sources temporary file glance1.dropbox supplied by driver, sends password to ssh/scp and overwrites dropbox to minimize password exposure.
The full package thus contains:

# glance1ssh.py - the driver
# catpass.py - helper to the driver
# glance1.script - the script to execute remotely
# (optional) glance1.list - list of hosts to assess
# (optional) README.md - this Markdown-formatted description

Some features used in glance1ssh.py require Python 2.6 (t.b.d.)
This is the default Python version on Debian 6, RHEL 6, and SuSE 11. 
On RHEL 5 one may install it from EPEL. In the later case please use python26 binary (edit line 1 of glance1ssh.py)

This project is hosted https://github.com/mz0/glance1
and bears no license - this work is in the Public Domain.

mz@exactpro.com
