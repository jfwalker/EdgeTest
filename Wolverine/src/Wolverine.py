# -*- coding: utf-8 -*-
'''
This performs an exhaustive edge search and creates a log file for summarizing
to a tree. The program SummerTree.py can create the consensus tree(s) underlying
your data.
'''
import sys
import argparse
import os
import subprocess, conflict_utils
import seq_utils, Folder_utils, bipart_utils, Tree_estimation_utils, read_a_tree

'''
Needs a supermatrix, a tree set
'''

LICENSE = """
Feel free to use manipulate but please don't take credit for the code.
It's pretty sloppy and full of false laziness so I don't know why you
would want to take credit for it, but again please don't.     
------------------------------------------------------------------------                                                              
email: jfwalker@umich.edu
"""


def generate_argparser():
	
	parser = argparse.ArgumentParser(
        prog="Wolverine.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		epilog=LICENSE)
	parser.add_argument("-s", "--supermatrix", required=True, type=str, help="""
	Supermatrix file in fasta, if not fasts use pxs2fa from the phyx package""")
	parser.add_argument("-q", "--partition", required=True, type=str, help="""
	Partition file, should be in RAxML readable format""")
	parser.add_argument("-t", "--trees", required=False, type=str, help="""
	List of trees to analyze, in default will estimate trees separately""")
	parser.add_argument("-m", "--missing", required=False, type=str, help="""
	Continue where your analysis left off, specify the output folder, good
	for if you use xubuntu and your computer crashes on a semi regular basis
	or for other more normal reasons""")
	parser.add_argument("-e", "--estimate_gene_trees", action="count", default=0, help="""
	Reverse concatenates, then estimates gene trees, then ends""")
	parser.add_argument("-f", "--output_folder", required=False, type=str, help="""
	Name for the output folder, default is output_folder""")
	parser.add_argument("-p", "--phyx_location", required=False, type=str, help="""
	path to phyx""")
	parser.add_argument("-o", "--only_con", action="count", default=0, help="""
	Die after your conflict analysis, useful for creating the conflict files
	for downstream analyses""")
	parser.add_argument("-a", "--only_clade", action="count", default=0, help="""
	Die after your conflict analysis, useful for creating the conflict files
	for downstream analyses""")
	parser.add_argument("-l", "--log_file", required=False, type=str, help="""
	Name of a log file to print things to, default is just logfile""")
	parser.add_argument("-c", "--cut_off", required=False, type=int, help="""
	Support value cutoff""")
	parser.add_argument("-r", "--raxml", required=False, type=str, help="""
	Location of raxml-ng""")
	parser.add_argument("-d", "--Threads", required=False, type=str, help="""
	Threads for raxml-ng, default 2""")
	parser.add_argument("-n", "--no_edge", action="count", help="""
	Do all but the edge based analysis""")
	parser.add_argument("-v", "--verbosity", action="count", default=0, help="""
	Increase the verbosity""")
	return parser
   
def main(arguments=None):
	
	FastaHash = {}
	PartitionHash = {}
	name_list = []
	clade_of_i = []
	clades_array = []
	unused = []
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]

	#Get the info from arg parse
	fasta = open(args.supermatrix, "r")
	partition = open(args.partition, "r")
	
	#Get the fasta into a hash
	FastaHash,name_list = seq_utils.fasta_parse(fasta)
	PartitionHash = seq_utils.partition_parse(partition)
	
	
	'''
	This just gives the option to specify an alternative path to raxml-ng
	'''
	if args.raxml:
		TreeEstimator = args.raxml
	else:
		TreeEstimator = "raxml-ng"	
	
	'''
	Add in a feature that you can pick up where the analysis left off
	Probably make this log file related? Maybe easier to have it read
	in the folder and analyze what has been done?
	'''
	if args.Threads:
		Threads = args.Threads
	else:
		Threads = "2"
		
	if args.cut_off:
		if args.trees:
			Cutoff = args.cut_off
		else:
			print "You need to give trees for this"
			exit
	else:
		Cutoff = 0
			
	if args.output_folder:
		OutFolder = args.output_folder
	else:
		OutFolder = "output_folder"
	cmd = ""
	cmd = "mkdir " + OutFolder
	os.system(cmd)	
		
	if args.log_file:
		outlog = args.log_file
	else:
		outlog = "log.log"
	

	if args.trees:
		Trees = args.trees
	else:
		print "Got it, no trees given so I'll estimate them"
		Folder_utils.split_to_genes(FastaHash,PartitionHash,OutFolder,args.verbosity)
		Tree_estimation_utils.estimate_gene_trees(TreeEstimator,FastaHash,PartitionHash,Threads,OutFolder)
		Trees = "Estimated here"
		if args.estimate_gene_trees:
			sys.exit()
	
	'''
	This lets the user use phyx or do a separate conflict analysis
	'''
	if args.phyx_location != None:
		phyx_loc = args.phyx_location
		Trees = args.trees
		clade_of_i = bipart_utils.get_clade_from_first_seq(phyx_loc, Trees, name_list)
		#turn of the edge analysis and leave that to EdgeTest.py
		just_edge = "false"
		unused = bipart_utils.conflict_with_clade_of_i(clade_of_i, phyx_loc, Trees, name_list, outlog, Cutoff, just_edge)
		bipart_utils.get_clades(phyx_loc, Trees, name_list, args.cut_off, Cutoff, OutFolder)
	else:
		biparts = []
		all_info = []
		phyx_loc = ""
		print "own conflict (slower but more robust to missing data)"
		print "Pooling Trees"
		'''
		The array biparts is an array of arrays containing clades identified
		'''
		biparts = read_a_tree.trees_to_bipart(Trees,Cutoff)
		#Get a print out of all the clades identified
		Folder_utils.get_clade_output(OutFolder, biparts)
		#Get unique with accordance to other side of bipartition
		if args.only_clade:
			print "Only Doing clades"
			cmd = ""
			cmd = "mkdir " + OutFolder + "/CladeAnalysis/"
			os.system(cmd)
			cmd = ""
			cmd = "mv " + OutFolder + "/clades_identified_by_phail.txt " + OutFolder + "/CladeAnalysis/"
			os.system(cmd)
		else:
			all_info = conflict_utils.test_trees(biparts,name_list,Trees,Cutoff)
			print "Summarizing results"
			conflict_utils.summarize(all_info,biparts,OutFolder)
			cmd = ""
			cmd = "mkdir " + OutFolder + "/CladeAnalysis/"
			os.system(cmd)
			cmd = ""
			cmd = "mv " + OutFolder + "/conflict_results.txt " + OutFolder + "/concordance_results.txt " + OutFolder + "/clades_identified_by_phail.txt " + OutFolder + "/unique_conflict_results.txt " + OutFolder + "/CladeAnalysis/"
			os.system(cmd)
		
		if args.only_con:
			print "Ending at conflict analysis"
			sys.exit()
		else:
			print "Building Constraints"
			bipart_utils.get_const_from_own(OutFolder)
	
	if args.verbosity:
		print "Your log file is " + outlog
		print "Your Fasta file is " + args.supermatrix
		print "Your Partition file is " + args.partition
		print "Path to phyx is: " + phyx_loc
		print "Your Output folder is " + OutFolder
		print "Your cutoff is: " + str(Cutoff)
	
	outf_log = open(outlog, "a")
	
	'''
	#make output folder
	cmd = ""
	cmd = "mkdir " + OutFolder
	os.system(cmd)
	'''
	#Write some stuff out 
	outf_log.write("####Basic Info About the Analysis####\n")
	outf_log.write("You are using " + TreeEstimator + "\n")
	outf_log.write("Your Fasta file is " + args.supermatrix + "\n")
	outf_log.write("Your Partition file is " + args.partition + "\n")
	outf_log.write("Your Trees file is " + Trees + "\n")
	outf_log.write("Your Output folder is " + OutFolder + "\n")
	outf_log.write("Path to phyx is: " + phyx_loc + "\n")
	outf_log.write("Your cutoff is: " + str(Cutoff) + "\n")
	
	#Divide to genes
	Folder_utils.split_to_genes(FastaHash,PartitionHash,OutFolder,args.verbosity)
	
	if args.no_edge:
		print "(⌐■_■) Finished without an edge analysis"
	else:
		Tree_estimation_utils.estimate_tree_raxml(TreeEstimator, OutFolder,args.verbosity)
	

	

if __name__ == "__main__":
	main()
