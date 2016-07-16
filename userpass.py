#   Name:   passchange.py
#   Author: Adam Good
#   Date:   07-16-2016
#
#   Description: This script will change all passwords of users with user id above 1000 on linux systems
#
#   TODO:   I still have to set up some sort of init that will check for dependacies such as the newusers tool
#           I also need to build my own encryption(too avoid external modules for user convencience) to secure the map file
#           I should probably throw a lot of error checking in there
#           I also need to go through and clean it up because I'm sure it's sloppy
#
#   Notes:  This script is for anyone to use at whim. BUT I'M NOT RESPONSIBLE IF YOU BREAK SOMETHING!!!
#           Seriously, use at your own risk. It's not hard to lock yourself out of your system with this
#           I CAN'T STRESS IT ENOUGH! BE CAREFUL!!
#
#           Also, you'll have to encrypt the map yourself for now...
import sys
import os.path
from subprocess import call
import random
import string

def start():
    f = "file.txt"      # this will be the name of a temporary copy of the passwd file
    fname = getFile(f)  # This should get us a copy of /etc/passwd
    formatFile(fname)   # This will format the file to our liking (uid above 1000 only and insert new passwords)
    finishTheJob(f)     # And this will actually change the passwords(and make a file that shows users and passwords)
    print "Ok, Should Be Good To Go!!"

# This function creates a copy of /etc/passwd
def getFile(filename):
    # If the file already exists we delete it
    if (os.path.isfile("./" + filename)):
        call(["rm", filename])
    # Next we create our copy
    call(["cp", "/etc/passwd", filename])
    # And here we check to see if the copy exists
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
    p = p.join(random.choice(string.ascii_letters + string.digits + "!_") for _ in range(10))
    return p

# This will actually update the passwords and make the encrypted password map
def finishTheJob(f):
    # TODO Make Password Map
    fpPasswd = open(f)
    fpMap = open("map", "w")

    # There's probably a better way to format the strings, but for now we'll do 2 loops
    for _, s in enumerate(fpPasswd):
        n = ''
        p = ''
        i = 0
        while s[i] != ":":
            n = n + s[i]
            i += 1
        i += 1
        while s[i] != ":":
            p = p + s[i]
            i += 1
        line = n + ":" + p + "\n"
        fpMap.write(line)
    fpPasswd.close()
    fpMap.close()

    # TODO Encrypt Password Map

    # This is the point of no return where the passwords are changed!
    call(["newusers", f])
    call(["rm", f])


start()
