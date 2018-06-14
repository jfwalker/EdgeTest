import node
import sys,os
import subprocess
import tree_utils, tree_reader

'''
Get the conflicts from the dataset
Make conflict trees
'''
def get_conflicts(phyx_loc,Trees,name_list):
	
	
	#This is not great, but gets clades in tree1
	text_file = open(Trees, "r")
	temp = text_file.read().split("\n")
	outf = open("tempbipart", "w")
	outf.write(temp[0] + "\n")
	outf.close()
	cmd = ""
	cmd = phyx_loc + "pxbp -t tempbipart"
	print cmd
	os.system(cmd)
	p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	x = p.communicate()[0].split("\n")
	cmd = "rm tempbipart"
	os.system(cmd)
	for i in x:
		if i[0:5] == "CLADE":
			print i

	
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
