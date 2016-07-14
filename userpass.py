#   Name:   userpass.py
#   Author: Adam Good
#
#   Description: This script will change all passwords of users with user id above 1000 on linux systems
#
#   TODO:   I still have to set up some sort of init that will check for dependacies such as the newusers tool
#           I also need to create a way to get those passwords in a secure manner (probably an encrypted file)
#
#   Notes:  This script is for anyone to use at whim. BUT I'M NOT RESPONSIBLE IF YOU BREAK SOMETHING!!!
#           Seriously, use at your own risk. It's not hard to lock yourself out of your system with this
#           I CAN'T STRESS IT ENOUGH! BE CAREFUL!!
import sys
import os.path
from subprocess import call
import random
import string

def start():
    f = "file.txt"
    fname = getFile(f)
    formatFile(fname)
    # Lastly we just execute the command
    call(["newusers", f])
    call(["rm", f])
    print "Ok, Should Be Good To Go!!"

def getFile(filename):
    if (os.path.isfile("./" + filename)):
        call(["rm", filename])
    call(["cp", "/etc/passwd", filename])
    if (not os.path.isfile("./" + filename)):
        print("Failed to copy file")
        sys.exit()
    else:
        return filename

# This will format our file so it works in the newusers command
def formatFile(f):
    fp = open(f)
    lines = []
    for n, s in enumerate(fp):
        if getUID(s) >= 1000:
            # Here we generate a password and put it in the new lines
            p = getPassword()
            s = insertPassword(s, p)
            # Now e just add the string to the list
            lines.append(s)
    fp.close()

    # I'm actually wiping this file on purpose because we'll delete the file later for security reasons
    fp = open(f, "w")
    # Here we just put our newly formatted lines in the file
    for n in lines:
        fp.write(n)
        fp.write('\n')
    fp.close()

# this function will get the actual uid for each account
def getUID(s):
    # we assume the string is in the following format
    # mysql:x:112:123:MySQL Server,,,:/nonexistent:/bin/false
    i = 0
    while s[i] != ':':
        i += 1
    # move the index past the ":x:" part
    i += 3
    # now we move through the entire uid and save it in the string
    uid = ''
    while s[i] != ":":
        uid += s[i]
        i += 1
    return int(uid)
# This function will insert the password into the string
def insertPassword(s, p):
    # We will put the password where the "x" is in the string
    #First we get everthing before where we put the password
    s1 = ''
    i = 0
    while s[i] != 'x':
        s1 = s1 + s[i]
        i += 1
    # Next we get everthing after the "x"
    s2 = ''
    i += 1
    while s[i] != '\n':
        s2 = s2 + s[i]
        i += 1
    # Lastly we mash everything together
    final = s1 + p + s2
    return final

def getPassword():
    p = ''
    # this line creates a 10 character password composed of ascii letters(upper and lower), digits, and puncuation
    p = p.join(random.choice(string.ascii_letters + string.digits + "!.?_") for _ in range(10))
    return p

start()
