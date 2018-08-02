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
	Likelihoods.write(rel2 + "\n")
	
	#Process the likelihoods
	prefix = ""
	const_name = ""
	fastas = open("ListofFastas.templist", "r")
	for i in fastas:
		gene = []
		row = ""
		i = i.strip("\n")
		gene = i.split("/")
		gene = gene[2]
		row = gene
		const = open("ListofConstraints.templist", "r")
		for x in const:
			x = x.strip("\n")
			const_name = x.split("/")
			const_name = const_name[2]
			prefix = gene + "_" + const_name
			cmd = ""
			cmd = TreeProg + " -msa " + i + " --model GTR+G --tree-constraint " + x + " --prefix " + prefix + " | grep \"Final LogLikelihood:\" "
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			t = p.communicate()[0].split(":")
			cmd2 = ""
			cmd2 = "mv " + prefix + ".* " + OutFolder + "/RaxmlLikelihoods/"
			os.system(cmd2)
			row = row + "\t" + t[1].strip("\n").strip(" ")
		print row
		Likelihoods.write(row + "\n")
			#print cmd
			#os.system(cmd)
	
	
	#Delete the list files
	cmd = ""
	cmd = "rm ListofFastas.templist ListofConstraints.templist"
	os.system(cmd)
