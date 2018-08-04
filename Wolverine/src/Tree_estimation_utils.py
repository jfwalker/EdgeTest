# -*- coding: utf-8 -*-
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
	rel2 = "GeneName\tNoRel"
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
		free = ""
		i = i.strip("\n")
		gene = i.split("/")
		gene = gene[2]
		row = gene
		
		#Get with no constraint
		cmd = ""
		cmd = TreeProg + " --msa " + i + " --model GTR+G --threads 4 --prefix " + gene + " | grep \"Final LogLikelihood:\" "
		p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		t = p.communicate()[0].split(":")
		row = row + "\t" + t[1].strip("\n").strip(" ")
		cmd2 = ""
		cmd2 = "mv " + gene + ".* " + OutFolder + "/RaxmlLikelihoods/"
		os.system(cmd2)		
		
		const = open("ListofConstraints.templist", "r")
		for x in const:
			x = x.strip("\n")
			const_name = x.split("/")
			const_name = const_name[2]
			prefix = gene + "_" + const_name
			cmd = ""
			cmd = TreeProg + " -msa " + i + " --model GTR+G --threads 4 --tree-constraint " + x + " --prefix " + prefix + " | grep \"Final LogLikelihood:\" "
			p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
			t = p.communicate()[0].split(":")
			cmd2 = ""
			cmd2 = "mv " + prefix + ".* " + OutFolder + "/RaxmlLikelihoods/"
			os.system(cmd2)
			row = row + "\t" + t[1].strip("\n").strip(" ")
		print "(☞ﾟヮﾟ)☞\t" + gene
		Likelihoods.write(row + "\n")
			#print cmd
			#os.system(cmd)
	
	
	#Delete the list files
	cmd = ""
	cmd = "rm ListofFastas.templist ListofConstraints.templist"
	os.system(cmd)
	

'''
Edge Estimation
'''
def estimate_edge(edge, all_species, genes, outfolder):
	
	#edge is the relationship of interest
	#all_species is the species each gene has
	#genes is the names of the genes
	
	#Create folder for raxml likelihoods to be output to and file for them
	cmd = ""
	cmd = "mkdir " + outfolder + "/RaxmlLikelihoods/"
	os.system(cmd)
	LikeFile = outfolder + "/Likelihoods.txt"
	Likelihoods = open(LikeFile, "w")
		
	#Make a header
	header = "GeneName"
	for i in edge:
		rel = ""
		for j in i:
			rel += j + ","
		header += "\t" + rel
	
	Likelihoods.write(header + "\n")

	#Iterates over genes
	input_gene_name = ""
	for i in genes:
		input_gene_name = outfolder + "/Fastas/" + i + ".fa"
		print input_gene_name			
		#Make a likelihood estimation no constraint
	
	
	
		#Make likelihoods with constraints implemented
	
	
	
	
	
