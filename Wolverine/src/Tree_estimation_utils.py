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
	
	#create header
	const = open("ListofConstraints.templist", "r") 
	for x in const:
		print x
	
		
	#Create folder for raxml likelihoods to be output to
	cmd = ""
	cmd = "mkdir " + OutFolder + "/RaxmlLikelihoods/"
	os.system(cmd)
	LikeFile = OutFolder + "/Likelihoods.txt"
	Likelihoods = open(LikeFile, "a")
	#
	
	
	


	#Delete the list files
	cmd = "rm ListofFastas.templist ListofConstraints.templist"
	os.system(cmd)
