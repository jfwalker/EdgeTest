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
		
'''
Same as above but factors in conflict, for nucleotides but easy edit to
incorporate AA's
'''
def	split_to_genes_edge(fasta, part, folder, v):
	
	taxa_content = []
	gene_names = []
	cmd = ""
	cmd = "mkdir " + folder + "/Fastas"
	os.system(cmd)
	if v:
		print "Dividing into folders"
	outfile = folder + "/DeletedTaxa.txt"
	putout = open(outfile, "w")
	count = 0
	len = []
	for i in part:
		len = part[i].split("-")
		start = int(len[0]) - 1
		stop = int(len[1])
		outname = i + ".fa"
		count = stop - start
		out = open(outname, "w")
		species_list = []
		for j in fasta:
			missing_count = 0
			for t in range(start, stop):
				if fasta[j][t] == "-":
					missing_count += 1
				elif fasta[j][t] == "N":
					missing_count += 1
			if missing_count == count:
				if v:
					print "Deleted: " + j + " " + i
				putout.write("Deleted: " + j + " " + i + "\n")
			else:
				out.write(">" + j + "\n" + fasta[j][start:stop] + "\n")
				species_list.append(j)
		taxa_content.append(species_list)
		gene_names.append(i)
		cmd = ""
		cmd = "mv " + i + ".fa " + folder + "/Fastas/"
		os.system(cmd)
	return taxa_content, gene_names

'''
Takes in all the well supported clades and prints them out
'''
def get_clade_output(Outdir, biparts):
	
	out = Outdir + "/clades_identified_by_phail.txt"
	clades_ident = open(out,"w")
	count = 0
	for x in biparts:
		line = ""
		for y in x:
			line = line + y + " "
		count += 1
		#print line
		#print line
		clades_ident.write("Clade " + str(count) + ": "+ line + "\n")
	clades_ident.close()
