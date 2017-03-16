#!/usr/bin/python
# Manoel Barrionuevo
# Enzyme wild and mutant type classifier
# Last updated : 12-03-2017

import sys, os, string

# ---- Get PDB that are ENGINEERED/SEQADV/MUTATION ---- #

def reader(lines,step):
	print "Parsing "+str(step)+" to PDB candidates."
	for i in lines:
		print "Parsing candidate: "+str(i)+"."
		os.system("find -type f -exec grep -lm1 '"+str(step)+"' "+i+" \; -a -quit >> "+str(step)+".txt")
	return lines

# ---------- Get PDB that are CHIMERA/LINKER  --------- #

def special_cases(lines,step):
	print "Parsing "+str(step)+" to PDB candidates."
	for i in lines:
		print "Parsing candidate: "+str(i)+"."
		os.system("find -type f -exec grep -Plm1 '(?=.*?SEQADV)(?=.*?"+str(step)+")' "+i+" \; -a -quit >> MUTATION.txt")
	return lines

# ----------- Get PDB list of WILD type only ---------- #

def wilder(name,pdbs):
	workfile = open(name, "r")
	print "Gethering wild types."
	lines = []
	for line in workfile:
		lines.append(line.strip())
	workfile.close()
	for mutant in lines:
	  for pdb in pdbs:
		if mutant == pdb:
			pdbs.remove(mutant) 
	pdbs.sort()
	with open('WILD.txt','w') as wd:
		for w in pdbs:
			wd.write("{0}\n".format(w))
	wd.close()
	return True


# ----------- Clean previous existent files ----------- #

os.system("rm -rf ENGINEERED.txt SEQADV.txt MUTATION.txt WILD.txt")

# -------------------- Get all PDBs ------------------- #

pdbs = []
for f in os.listdir("."):
	if f.endswith('.pdb'):
		pdbs.append(f)

# ---------- Create a list of engineered PDBs --------- #

eng = []
eng = reader(pdbs,"ENGINEERED")

# ------------ Get only SEQADV candidates ------------- #

seq = []
seq = reader(eng,"SEQADV")

# -------------- Get only known mutants --------------- #

mut = []
mut = reader(seq,"MUTATION")

# ---------------- Look for insertions ---------------- #

ins = []
ins = special_cases(seq,"INSERTION")

# ----------------- Look for chimeras ----------------- #

lik = []
lik = special_cases(seq,"LINKER")

# ------------ Create a list of wild types ------------ #

wilder("MUTATION.txt",pdbs)

print "That's it."
