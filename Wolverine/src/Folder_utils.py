import sys,os

"""
Uses the parts file and the supermatrix to reverse concatenate
"""
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
		outname = i + ".fa"
		out = open(outname, "w")
		for j in fasta:
			out.write(">" + j + "\n" + fasta[j][start:stop] + "\n")
		cmd = ""
		cmd = "mv " + i + ".fa " + folder + "/Fastas/"
		os.system(cmd)