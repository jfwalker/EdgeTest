import sys
import argparse
import os 
import seq_utils, Folder_utils

'''
Needs a supermatrix, a tree set
'''

def generate_argparser():

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--supermatrix", required=True, type=str, help="""
	Supermatrix file in fasta, if not fasts use pxs2fa from the phyx package""")
	parser.add_argument("-q", "--partition", required=True, type=str, help="""
	Partition file, should be in RAxML readable format""")
	parser.add_argument("-t", "--trees", required=False, type=str, help="""
	List of trees to analyze, in default will estimate trees separately""")
	parser.add_argument("-w", "--output_tree", required=False, type=str, help="""
	Name for the output tree, default is EdgeTree.tre""")
	parser.add_argument("-f", "--output_folder", required=False, type=str, help="""
	Name for the output folder, default is output_folder""")
	parser.add_argument("-p", "--phyx_location", required=False, type=str, help="""
	path to phyx, default is in path""")
	parser.add_argument("-l", "--log_file", required=False, type=str, help="""
	Name of a log file to print things to, default is just logfile""")
	parser.add_argument("-c", "--cut_off", required=False, type=int, help="""
	Support value cutoff""")
	parser.add_argument("-v", "--verbosity", action="count", default=0, help="""
	How verbose should this be [1,2,3]""")
	return parser
   
def main(arguments=None):
	
	FastaHash = {}
	PartitionHash = {}
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]

	#Get the info from arg parse
	fasta = open(args.supermatrix, "r")
	partition = open(args.partition, "r")
	
	if args.phyx_location:
		phyx_loc = args.phyx_location
	else:
		phyx_loc = ""
		
	if args.output_tree:
		OutTree = args.output_tree
	else:
		OutTree = "EdgeTree.tre"
		
	if args.cut_off:
	
		Cutoff = args.cut_off
	else:
		Cutoff = 0
			
	if args.output_folder:
		OutFolder = args.output_folder
	else:
		OutFolder = "output_folder"
		
	if args.log_file:
		outlog = args.log_file
	else:
		outlog = "log.log"
	
	if args.verbosity:
		print "Your log file is " + outlog
		print "Your Fasta file is " + args.supermatrix
		print "Your Partition file is " + args.partition
		print "Your Output tree file is " + OutTree
		print "Path to phyx is: " + phyx_loc
		print "Your Output folder is " + OutFolder
		print "Your cutoff is: " + str(Cutoff)
	
	outf_log = open(outlog, "w")
	
	#make output folder
	cmd = ""
	cmd = "mkdir " + OutFolder
	os.system(cmd)
	
	#Write some stuff out 
	outf_log.write("####Basic Info About the Analysis####\n")
	outf_log.write("Your Fasta file is " + args.supermatrix + "\n")
	outf_log.write("Your Partition file is " + args.partition + "\n")
	outf_log.write("Your Output tree file is " + OutTree + "\n")
	outf_log.write("Your Output folder is " + OutFolder + "\n")
	outf_log.write("Path to phyx is: " + phyx_loc + "\n")
	outf_log.write("Your cutoff is: " + str(Cutoff) + "\n")
	
	#Get the fasta into a hash
	FastaHash = seq_utils.fasta_parse(fasta)
	PartitionHash = seq_utils.partition_parse(partition)
	
	#Divide to genes
	Folder_utils.split_to_genes(FastaHash,PartitionHash,OutFolder,args.verbosity)
	

if __name__ == "__main__":
	main()
