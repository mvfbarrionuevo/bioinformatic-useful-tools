#!/usr/bin/python
#################################################################
# Cleaner-stp1.py - created by Manoel Barrionuevo - 2016        #
#################################################################
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

import sys, time, os, shutil, pymol

pymol.finish_launching()

#################################################################

# Defining yes or no query verifier

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            print " "
            print "You have hit [ENTER] thus I'm going to proceed as default."
	    return False
        elif choice in valid:
            if choice == 'no' or choice == 'n':
		print " "
		print "So you have chosen %s, thus you may like to change 'ZN-Protein' directory by your own. See you then." % choice
		print " "
		quit()
	    elif choice == 'yes' or choice == 'y':
		print " "
		print "You have chosen '%s'." %choice		
		print " "
		return False 
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

# Creating a list named lines

lines=[]

# Creating destination directory

if not os.path.exists('./ZN-Protein'):
	print " "
	print "Nice, there is no directory named 'ZN-Protein'. I'm going to make it for ya! :)"
	print " "
	os.makedirs('./ZN-Protein')
else:
	query_yes_no("Sorry but you already have a directory named 'ZN-Protein', would you like me to delete it? ")
	print "I'm going to delete 'ZN-Protein' directory, here we go."	
	print " "
	shutil.rmtree('./ZN-Protein', ignore_errors=True)
	os.makedirs('./ZN-Protein')

# Calling Lister to get a list of pdb files to work with

if os.path.exists('Lister-stp2.py')==True:
	print "Hey, I'm going to call a friend of mine (Lister-stp2.py) to get a list of all pdbs found in here."
	os.system('python Lister-stp2.py ./')
	if os.path.exists('exit.txt')==True:
	  print "You told to my friend you wouldn't like to get a new list, hope you fix it and come back. See you then."
	  os.remove('exit.txt')
	  quit()
else:
	print "Sorry, I'm affraid 'Lister-stp2.py' isn't in this directory. May you call it to join in here?"
	print " "
	quit()

if os.path.exists("list.txt")==True:
	print " "
	print "Yeah, 'Listerstp2.py' have done the job. Now I'll rock things up!"
	print " "
else:
	print " "
	print "Something still wrong here, I found 'Lister-stp2.py' but he didn't give me back a list of pdbs, could you please check if he's working well?"
	print " "
	quit()

with open('list.txt') as lst:
	for line in lst:
		lines.append(line.strip())

lst.close()

# Load and treat pdb structures

index=0
for index in range(len(lines)):
	pymol.cmd.load(lines[index] + '.pdb')
	if pymol.cmd.select("zincos", "%s////ZN" % lines[index]) != 0:
		pymol.cmd.save("%s-zn.pdb" % lines[index], "%s" % lines[index])
		os.remove(lines[index]+'.pdb')
	else:
		pymol.cmd.save("%s-ser.pdb" % lines[index], "%s" % lines[index])
		os.remove(lines[index]+'.pdb')
	pymol.cmd.remove("all")
	pymol.cmd.delete("all")

# Get out!ls
pymol.cmd.quit()

# Moving all treated pdbs to its new directory

destinationpath = './ZN-Protein'
sourcepath = './'
source = os.listdir(sourcepath)

for files in source:
	if files.endswith('-zn.pdb'):
		shutil.move(os.path.join(sourcepath,files),os.path.join(destinationpath,files))

# Ends everything

print " "
print "Great, I think we got only the zinc proteins. Have a good one! :D"
print " "
quit()
