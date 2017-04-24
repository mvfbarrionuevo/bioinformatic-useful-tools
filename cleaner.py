#!/usr/bin/python
#################################################################
# Cleaner-stp1.py - created by Manoel Barrionuevo - 2016        #
#################################################################
import __main__
__main__.pymol_argv = [ 'pymol', '-qc'] # Quiet and no GUI

import sys, time, os, shutil
import pymol

pymol.finish_launching()

#################################################################

def pdb_listing(p):
	# Creating list of present pdbs
	dirs = os.listdir(p)
	lista = []
	for files in dirs:
	   if files.endswith(".pdb"):
	      lista.append(files)
	lista.sort()
	return lista

# Calling listing to get a list of pdb files to work with

pdbs = []
pdbs = pdb_listing(p)

# Getting list of residues for each pocket in each pdb

index=0
for index in range(len(pdbs)):
	pymol.cmd.load(pdbs[index])
	pymol.cmd.remove("chain B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+S+T+U+V+W+X+Y+Z")
	pymol.cmd.select("zincos", "symbol ZN")
	pymol.cmd.select("pocket", "all within 7.5 of zincos")
	pymol.cmd.remove("symbol li+na+k+mg+sr+be+fe+ca+ag+pt+hg+co+au+ni+cd")
	pymol.cmd.remove("resname SO4+CO3+PO4+AZI+CL")
	pymol.cmd.remove("solvent beyond 15 of zincos")
	pymol.cmd.delete("zincos")
	pymol.cmd.remove("not (alt ''+A)")
	pymol.cmd.alter("all","alt=''")
	pymol.cmd.save("%s-c.pdb" % lines[index], "%s_A" % lines[index])
	pymol.cmd.remove("all")
	pymol.cmd.delete("all")

# Get out!
pymol.cmd.quit()

index=0
ter = ['TER']
for index in range(len(lines)):
   with open('%s-c.pdb' % lines[index]) as oldfile, open('%s_f.pdb' % lines[index], 'w') as newfile:
	for line in oldfile:
		if not all(ters in line for ters in ter):
			newfile.write(line)
	oldfile.close()
	newfile.close()

index=0
ter = ['ANISOU']
for index in range(len(lines)):
   with open('%s_f.pdb' % lines[index]) as oldfile, open('%s-f.pdb' % lines[index], 'w') as newfile:
	for line in oldfile:
		if not all(ters in line for ters in ter):
			newfile.write(line)
	oldfile.close()
	newfile.close()

# Moving all treated pdbs to its new directory

destinationpath = './Cleaned'
sourcepath = './'
source = os.listdir(sourcepath)

for files in source:
	if files.endswith('-f.pdb'):
		shutil.move(os.path.join(sourcepath,files),os.path.join(destinationpath,files))
	if files.endswith('-c.pdb'):
		os.remove(files)
	if files.endswith('_f.pdb'):
		os.remove(files)

# Ends everything

print " "
print "Great, everything ran smoothly. Have a good one! :D"
print " "
quit()
