#!/usr/bin/python
import sys

DROPBOX="glance1.dropbox"

def catpw():
    with open(DROPBOX, 'rw+') as dropbox:
        password=dropbox.read()
        #shutil.copyfileobj(dropbox, sys.stdout)
        sys.stdout.write(password)
        #write something over the password
        dropbox.seek(0) 
        dropbox.write('-- security-erased --') 
   
if __name__ == '__main__' :
    catpw()
