
# -*- coding: utf-8 -*-
import node
import sys,os
import subprocess
import tree_utils, tree_reader


'''
This needs to identify the other side of the bipartition
'''
def flip_side(biparts,name_list):
	print "flipping"
'''
Get the conflicts from clade of interest, uses first tree
'''
def get_clade_from_first_seq(phyx_loc,Trees,name_list):
	
	
	#This is not great, but gets clades in tree1
	parts = []
	clade_of_i = []
	clade = []
	all_clades = []
	text_file = open(Trees, "r")
	temp = text_file.read().split("\n")
	outf = open("tempbipart", "w")
	outf.write(temp[0] + "\n")
	outf.close()
	cmd = ""
	cmd = phyx_loc + "pxbp -t tempbipart"
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	x = p.communicate()[0].split("\n")
	cmd = "rm tempbipart"
	os.system(cmd)
	for i in x:
		if i[0:5] == "CLADE":
			parts = i.split("\t")
			clade_of_i = parts[0].split(":")
			clade = clade_of_i[1].split(" ")
			clade[:] = [item for item in clade if item != '']
			all_clades.append(clade)
	return all_clades

def exist_check(clade,clade_of_i):

	#print "Check " + str(clade)
	check = ""
	for i in clade_of_i:
		#print i
		if len(i) == len(clade):
			match = set(i)
			#print match.intersection(clade)
			if len(match.intersection(clade)) == len(i):
				check = "true"
	if check == "true":
		return "true"
	else:
		return "false"

	
'''
Get conflicts with clade of interest
'''
def conflict_with_clade_of_i(clade_of_i,phyx_loc,Trees,name_list, outlog, cutoff, just_edge):
	
	parts = []
	clade_of_j = []
	clade = []
	con_clade = []
	mix_clade = []
	edges = []
	clade_hash = {}
	check = ""
	names = []
	outf_log = open(outlog, "w")
	outf_log.write("##### Edges #####\n")
	#phyx stuff
	conflict_a = ""
	cmd = ""
	if cutoff == 0:
		cmd = phyx_loc + "pxbp -t " + Trees + " -v"
	else:
		cmd = phyx_loc + "pxbp -t " + Trees + " -c " + str(cutoff) + " -v"
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	x = p.communicate()[0].split("\n")
	count = 0
	#iterate the phyx output
	for i in x:
		
		#checks if matches with conflict are in clade of interest
		#if there is prints out newicks with constraints
		if i[0:5] == "\tFREQ":
			check = exist_check(clade, clade_of_i)
			if check == "true":
				names.append(clade)
				outf_log.write("Edge " + str(count) + " " + str(clade) + "\n")
				for j in mix_clade:
					outf_log.write("\tConflict " + str(j) + "\n")
					if just_edge == "true":
						edges.append(j)
				count += 1
			#print mix_clade
			#print match
			conflict_a = "false"
		if i[0:5] == "CLADE":
			parts = i.split("\t")
			clade_of_j = parts[0].split(":")
			clade = clade_of_j[1].split(" ")
			clade[:] = [item for item in clade if item != '']
		if conflict_a == "true":
			parts = i.split("\t")
			con_clade = parts[1].split(" ")
			con_clade[:] = [item for item in con_clade if item != '']
			mix_clade.append(con_clade)
		if i[0:9] == "\tCONFLICT":
			conflict_a = "true"
	
	for x in clade_of_i:
		#print x
		#print names[0]
		check = exist_check(x, names)
		if check == "false":
			outf_log.write("Edge " + str(count) + " " + str(x) + "\n")
			count += 1
		if just_edge == "true":
			edges.append(x)
	return edges
	
	outf_log.close()

'''
Is this repetive: yes
Is this the best way: No
Does this work: Seemingly
'''		
def get_clades(phyx_loc, Trees, name_list, arg, cutoff, outdir):
	
	print "Making Constraints"
	clade = []
	clade_of_j = []
	parts = []
	clade_out = ""
	clade_in = ""
	HASH = {}
	count = 0
	newick = ""
	
	cmd = "mkdir " + outdir + "/constraints"
	os.system(cmd)

	cutoff = str(cutoff)
	if arg:
		cmd = phyx_loc + "pxbp -t " + Trees + " -c " + cutoff
		print cmd
	else:
		cmd = phyx_loc + "pxbp -t " + Trees
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	x = p.communicate()[0].split("\n")
	
	for i in x:
		HASH = {}
		if i[0:5] == "CLADE":

			parts = i.split("\t")
			clade_of_j = parts[0].split(":")
			clade = clade_of_j[1].split(" ")
			clade[:] = [item for item in clade if item != '']
			for g in clade:
				HASH[g] = g
			for g in name_list:
				if g in HASH:
					if clade_in == "":
						clade_in = g
					else:
						clade_in = clade_in + "," + g
				else:
					clade_out = clade_out + "," + g
			#print clade
			newick = "((" + clade_in + ")" + clade_out + ");"
			outname = "constraint_" + str(count)
			#print outname
			out = open(outname, "w")
			out.write(newick + "\n")
			cmd = ""
			cmd = "mv " + outname + " " + outdir + "/constraints/"
			#print cmd
			os.system(cmd)
			clade_in = ""
			clade_out = ""
			count += 1
			
			
				
			
			
			#print "(☞ﾟヮﾟ)☞"

'''
Checks to see if an array of species (edge), contains the ability to
test a relationship of interest (at least 2 species), this is not
foolproof!!!! And needs work. This is basically so the constraint
does not cause it to crash
'''
def testable_edge(species_list, edge):

		match = set(species_list)
		if len(match.intersection(edge)) < 2:
			return "false"
		else:
			return "true"

'''
Actually assemble the constraint
'''
def make_constraint(sp_list,edge):
	
	ingroup = []
	out_clade = ""
	in_clade = "(("
	pointless = ""
	constraint = ""
	HASH = {}
	match = set(sp_list)
	ingroup = match.intersection(edge)
	
	for i in ingroup:
		HASH[i] = i
		in_clade += i + ","
	in_clade = in_clade[:-1]
		
	
	for i in sp_list:
		if i in HASH:
			pointless = ""
		else:
			out_clade += "," + i
	#print "Here is ingroup: " + in_clade
	#print "Here is outgroup: " + out_clade
	if out_clade == "":
		return "false"
	else:
		constraint = in_clade + ")" + out_clade + ")" + ";"
		return constraint
	
	#print "Here is the constraint: " + constraint
	
	#for i in ingroup:
	#	print i
	

'''
Create constraints by taking a list of available species and the edge
of interest
'''
def create_constraint(species_avail, edge, gene_name):
	
	
	use_constraint = "true"
	constraint = ""
	
	#Gene_name is the name of the gene
	#Edge is an array of species in the edge of interest
	#species avail is those that a constraint can be made out of
	
	#print "Gene: " + str(gene_name) + " ,Edge: " + str(edge) + " ,available species: " + str(species_avail)
	use_constraint = testable_edge(species_avail, edge)
	if use_constraint == "true":
		constraint = make_constraint(species_avail, edge)
		if constraint == "false":
			return "false"
		else:
			return constraint
	else:
		return "false"
	
	

	
'''
	#Get the conflicts that match with the clade of interest
	cmd = ""
	cmd = phyx_loc + "pxbp -t " + Trees + " -v"
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	x = p.communicate()[0].split("\n")
	#print x
	#os.system(cmd)
	#for i in x:
		#print i[0:4]
		#if i[0:5] == "CLADE":
			#print i
'''
