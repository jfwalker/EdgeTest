import node
import sys,os
import subprocess
import tree_utils, tree_reader

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
def conflict_with_clade_of_i(clade_of_i,phyx_loc,Trees,name_list, outlog):
	
	parts = []
	clade_of_j = []
	clade = []
	con_clade = []
	mix_clade = []
	clade_hash = {}
	check = ""
	names = []
	outf_log = open(outlog, "w")
	outf_log.write("##### Edges #####\n")
	#phyx stuff
	conflict_a = ""
	cmd = ""
	cmd = phyx_loc + "pxbp -t " + Trees + " -v"
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
	
	
	outf_log.close()

'''
Is this repetive: yes
Is this the best way: No
Does this work: Seemingly
'''		
def get_clades(phyx_loc, Trees, name_list, arg, cutoff):
	
	clade = []
	clade_of_j = []
	parts = []
	cutoff = str(cutoff)
	if arg:
		cmd = phyx_loc + "pxbp -t " + Trees + " -c " + cutoff
		print cmd
	else:
		cmd = phyx_loc + "pxbp -t " + Trees
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	x = p.communicate()[0].split("\n")
	
	for i in x:
		if i[0:5] == "CLADE":

			parts = i.split("\t")
			clade_of_j = parts[0].split(":")
			clade = clade_of_j[1].split(" ")
			clade[:] = [item for item in clade if item != '']
			print clade
	
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
