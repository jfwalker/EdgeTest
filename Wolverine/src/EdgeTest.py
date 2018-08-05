import sys
import argparse
import os
import subprocess
import seq_utils, Folder_utils, bipart_utils, Tree_estimation_utils

'''
Arguments
'''

LICENSE = """
Quick disclaimer, this is the follow up to the MGWE program! This
creates a constraint of all conflicts. Similar to the "Analyzing contentious
relationships and outlier genes in phylogenomics"-Walker et al. 2018 paper 
this is focused on an edge but uses a method more in the vain of "Nested 
phylogenetic conflicts and deep phylogenomics in plants".-Smith et al. 2018              
------------------------------------------------------------------------                                                              
email: jfwalker@umich.edu
"""


def generate_argparser():

	#parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(
        prog="EdgeTest.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
epilog=LICENSE)
	parser.add_argument("-s", "--supermatrix", required=True, type=str, help="""
	Supermatrix file in fasta, if not fasts use pxs2fa from the phyx package""")
	parser.add_argument("-q", "--partition", required=True, type=str, help="""
	Partition file, should be in RAxML readable format""")
	parser.add_argument("-t", "--trees", required=True, type=str, help="""
	List of trees to analyze for conflicts""")
	parser.add_argument("-z", "--relationship", required=True, type=str, help="""
	comma separated list of species in clade to test (Must be in first tree)""")
	parser.add_argument("-i", "--relationship_file", required=False, action="count", default=0, help="""
	flag to indicate that your comma separated list of species in clade to test 
	is in a file (Must be in first tree), must be turned on if you are giving a
	file and not a command line input of relationship""")
	parser.add_argument("-o", "--only_specified", required=False, action="count", default=0, help="""
	No conflict identification test only the csv list of user specified relationships (does more at one time)""")
	parser.add_argument("-f", "--output_folder", required=False, type=str, help="""
	Name for the output folder, default is output_folder_EdgeTest""")
	parser.add_argument("-p", "--phyx_location", required=False, type=str, help="""
	path to phyx, default is in path""")
	parser.add_argument("-d", "--Threads", required=False, type=str, help="""
	default is 2""")
	parser.add_argument("-r", "--raxml", required=False, type=str, help="""
	Location of raxml-ng""")
	parser.add_argument("-v", "--verbosity", action="count", default=0, help="""
	Increase the verbosity""")
	return parser

def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]
	
	#necessary variables
	FastaHash = []
	PartitionHash = []
	name_list = []
	clade_of_i = []
	Threads = "2"
	Cutoff = 0
	
	
	#Get the info from arg parse
	fasta = open(args.supermatrix, "r")
	partition = open(args.partition, "r")
	
	#Get the fasta into a hash
	FastaHash,name_list = seq_utils.fasta_parse(fasta)
	PartitionHash = seq_utils.partition_parse(partition)
	
	if args.phyx_location:
		phyx_loc = args.phyx_location
	else:
		phyx_loc = ""
	
	if args.output_folder:
		OutFolder = args.output_folder
	else:
		OutFolder = "output_folder_EdgeTest"
	cmd = ""
	cmd = "mkdir " + OutFolder
	os.system(cmd)
	outlog = OutFolder + "/conflicts.txt"
	
	if args.Threads:
		Threads = args.Threads
	
	if args.raxml:
		raxml = args.raxml
	else:
		raxml = "raxml-ng"
	
	#Tree data
	Trees = args.trees
	
	#Relationship of interest
	if args.relationship_file:
		test_rel = open(args.relationship, "r")
		relationship2 = seq_utils.get_rel(test_rel)
		relationship = relationship2[0]
	else:
		relationship = args.relationship
	
	#Create the folder of genes
	#taxon_list: taxons in genes
	#gene_name: name of genes
	
	taxon_list, gene_name = Folder_utils.split_to_genes_edge(FastaHash,PartitionHash,OutFolder,args.verbosity)
		
	if args.only_specified:
		temp_rel = []
		edges = []
		for j in relationship2:
			temp_rel = j.split(",")
			edges.append(temp_rel)
		print edges
	else:
		#Get Conflicts
		temp = []
		temp = relationship.split(",")
		clade_of_i.append(temp)
		just_edge = "true"
		edges = []
		edges = bipart_utils.conflict_with_clade_of_i(clade_of_i, phyx_loc, Trees, name_list, outlog, Cutoff, just_edge)

	#Estimate all the likelihoods of each gene
	print edges
	Tree_estimation_utils.estimate_edge(edges, taxon_list, gene_name, OutFolder, raxml, Threads)
	
	#Summarize the data
	
	#types of summaries (total likelihood of edges), diff between edges,
	#genes that are 2lnl greater in likelihood
	
	
if __name__ == "__main__":
	main()
