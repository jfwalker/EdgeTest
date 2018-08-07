# -*- coding: utf-8 -*-
import node
import sys,os
import subprocess
import tree_utils, tree_reader
import bipart_utils

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
Runs raxml with no constraint
Possible to do evaluate with a small edit of uncommenting but evaluate
seems a bit screwy right now
'''
def run_ng_no_const(raxml, Threads, gene_name, input_gene, OutFolder):
	
	cmd = ""
	#cmd = raxml + " --msa " + input_gene + " --lh-epsilon 0.000001 --blopt nr_safe --model GTR+G --threads " + str(Threads) + " --prefix " + gene_name + " | grep \"Final LogLikelihood:\""
	cmd = raxml + " --msa " + input_gene + " --blopt nr_safe --seed 12345 --lh-epsilon 0.000001 --model GTR+G --threads " + str(Threads) + " --prefix " + gene_name + " | grep \"Final LogLikelihood:\""

	#print cmd
	#os.system(cmd)
	#cmd = ""
	#cmd = raxml + " --evaluate --msa " + input_gene + " --tree " + gene_name + ".raxml.bestTree --lh-epsilon 0.00001 --blopt nr_safe" + " --model GTR+G --threads " + str(Threads) + " --prefix " + "revaluated_" + gene_name + " | grep \"final logLikelihood:\""
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	t = p.communicate()[0].split(":")
	#print t
	cmd2 = "mv *" + gene_name + ".* " + OutFolder + "/RaxmlLikelihoods/"
	os.system(cmd2)
	if len(t) == 1:
		print "RAxML did not run, probably too many threads"
		sys.exit()
	#change to three for evaluate
	return t[1].strip("\n").strip(" ")

def run_ng_const(raxml, Threads, gene_name, input_gene, OutFolder, count, file_name_const):	

	cmd = ""
	#cmd = raxml + " --msa " + input_gene + " --tree-constraint " + file_name_const + " --lh-epsilon 0.000001 --blopt nr_safe --model GTR+G --threads " + str(Threads) + " --prefix " + gene_name + str(count) + " | grep \"Final LogLikelihood:\""
	cmd = raxml + " --msa " + input_gene + " --tree-constraint " + file_name_const + " --blopt nr_safe --seed 12345 --lh-epsilon 0.000001 --model GTR+G --threads " + str(Threads) + " --prefix " + gene_name + str(count) + " | grep \"Final LogLikelihood:\""
	#os.system(cmd)
	#cmd = ""
	#cmd = raxml + " --evaluate --msa " + input_gene + " --tree " + gene_name + str(count) + ".raxml.bestTree --lh-epsilon 0.00001 --blopt nr_safe" + " --model GTR+G --threads " + str(Threads) + " --prefix " + "revaluated_" + gene_name + str(count) + " | grep \"final logLikelihood:\""
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	t = p.communicate()[0].split(":")
	#print t
	cmd2 = "mv *" + gene_name + str(count) + ".raxml.* " + OutFolder + "/RaxmlLikelihoods/ && mv " + gene_name + str(count) + ".tre " + OutFolder + "/ConstraintsUsed/"
	os.system(cmd2)
	if len(t) == 1:
		print "RAxML did not run, probably too many threads"
		sys.exit()
	return t[1].strip("\n").strip(" ")

'''
Edge Estimation
'''
def estimate_edge(edge, all_species, genes, outfolder, raxml, Threads):
	
	#edge is the relationship of interest
	#all_species is the species each gene has
	#genes is the names of the genes
	
	#Create folder for raxml likelihoods to be output to and file for them
	cmd = ""
	cmd = "mkdir " + outfolder + "/RaxmlLikelihoods/"
	os.system(cmd)
	cmd = ""
	cmd = "mkdir " + outfolder + "/ConstraintsUsed/"
	os.system(cmd)
	LikeFile = outfolder + "/Likelihoods.txt"
	Likelihoods = open(LikeFile, "w")
	
	list_of_testable_species = outfolder + "/untestable.txt"
	outfile_of_testable = open(list_of_testable_species, "w")
	
	constraint = ""
	
	
	#Make a header
	header = "GeneName\tNoConstraint"
	for i in edge:
		rel = ""
		for j in i:
			rel += j + ","
		header += "\t" + rel[:-1]
	
	Likelihoods.write(header + "\n")

	#Iterates over genes, relationship should match gene its on so that 
	#uses a counter, line is the line to be printed
	count = 0
	edge_count = 0
	input_gene_name = ""
	line = ""
	no_const_likely = ""
	const_likely = ""
	for i in genes:
		line = ""
		input_gene_name = outfolder + "/Fastas/" + i + ".fa"
		line += i
		#Make a likelihood estimation no constraint
		no_const_likely = run_ng_no_const(raxml, Threads, i, input_gene_name, outfolder)
		line += "\t" + no_const_likely
		#print no_const_likely
		edge_count = 0
		#Make likelihoods with constraints implemented
		for j in edge:
				

				constraint = bipart_utils.create_constraint(all_species[count], j, i)
				file_name_const = str(i) + str(edge_count) + ".tre"
				if constraint == "false":
					outfile_of_testable.write("no constraint used for: " + str(i) + str(edge_count) + " " + str(j) + "\n")
					#Don't rerun raxml just use the one without the constraint
					line += "\t" + no_const_likely
				else:
					#run with constraint
					#print constraint
					Const_file = open(file_name_const, "w")
					Const_file.write(constraint)
					Const_file.close()
					const_likely = run_ng_const(raxml, Threads, i, input_gene_name, outfolder, edge_count, file_name_const)
					line += "\t" + const_likely
					#print const_likely
				edge_count += 1
		print line
		print "(☞ﾟヮﾟ)☞\t" + i
		Likelihoods.write(line + "\n")	
					
		count += 1			
	
	
def estimate_gene_trees(TreeProg,FastaHash,PartitionHash,Threads, OutFolder):	
	
	cmd = ""
	cmd = "mkdir " + OutFolder + "/EstimatedGeneTrees/"
	os.system(cmd)
	cmd = ""
	cmd = "ls " + OutFolder + "/Fastas/* > ListofFastas.templist"
	os.system(cmd)
	fastas = open("ListofFastas.templist", "r")
	for i in fastas:
		gene = []
		row = ""
		free = ""
		i = i.strip("\n")
		gene = i.split("/")
		gene = gene[2]
		row = gene
		cmd = TreeProg + " --msa " + i + " --model GTR+G --threads " + str(Threads) + " --prefix " + gene
		os.system(cmd)
		cmd2 = ""
		cmd2 = "mv " + gene + ".* " + OutFolder + "/RaxmlLikelihoods/"
		os.system(cmd2)
