import node
import sys,os
import subprocess
import tree_utils, tree_reader

def estimate_tree_raxml(TreeProg, OutFolder):
	print "Estimating likelihoods using " + TreeProg
	
	cmd = ""
	cmd = "ls " + OutFolder + "/Fastas/* > ListofFastas.templist"
	os.system(cmd)
	
	cmd = ""
	cmd = "ls " + OutFolder + "/constraints/* > ListofConstraints.templist"
	os.system(cmd)
	
	#create header for the likelihood file
	
	rel = ""
	rel2 = "GeneName"
	const = open("ListofConstraints.templist", "r") 
	for x in const:
		x = x.strip("\n")
		readconst = open(x, "r")
		for i in readconst:
			i = i.strip("\n")
			i = i.split(")")
			i = i[0].split("(")
			i = i[2]
			rel2 = rel2 + "\t" + i
	#Create folder for raxml likelihoods to be output to and file for them
	cmd = ""
	cmd = "mkdir " + OutFolder + "/RaxmlLikelihoods/"
	os.system(cmd)
	LikeFile = OutFolder + "/Likelihoods.txt"
	Likelihoods = open(LikeFile, "w")
	Likelihoods.write(rel2)
	
	#Process the likelihoods
	prefix = ""
	fastas = open("ListofFastas.templist", "r")
	for i in fastas:
		i = i.split("\n")
		i = i[0]
		print i
		const = open("ListofConstraints.templist", "r")
		for x in const:
			x = x.strip("\n")
			prefix = i + x
			cmd = ""
			cmd = TreeProg + " -msa " + i + " --tree-constraint " + x + " --prefix " + prefix + " | grep \"Final\" "
			os.system(cmd)
	
	
	#Delete the list files
	cmd = ""
	cmd = "rm ListofFastas.templist ListofConstraints.templist"
	os.system(cmd)
