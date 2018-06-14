import sys,os

def split_to_genes(fasta, part, folder, v):
	
	cmd = ""
	cmd = "mkdir " + folder + "/Fastas"
	os.system(cmd)
	if v:
		print "Dividing into folders"
	
	len = []
	for i in part:
		len = part[i].split("-")
		start = int(len[0]) - 1
		stop = int(len[1])
		for j in fasta:
			#print fasta[j][len[0]:len[1]]
			print ">" + j + "\n" + fasta[j][start:stop]