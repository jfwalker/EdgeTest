import sys
import argparse
import os
import seq_utils

'''
Needs a supermatrix, a tree set


'''

def generate_argparser():

	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--supermatrix", required=True, type=str, help="""
	Supermatrix file in fasta, if not fasts use pxs2fa from the phyx package""")
	parser.add_argument("-p", "--phyx_location", required=False, type=str, help="""
	path to phyx, default is in path""")
	parser.add_argument("-l", "--log_file", required=False, type=str, help="""
	Name of a log file to print things to, default is just logfile""")
	
	parser.add_argument("-v", "--verbosity", action="count", default=0, help="""
	How verbose should this be [1,2,3]""")
	return parser
   
def main(arguments=None):
	
	HASH = {}
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]

	#Get the info from arg parse
	fasta = open(args.supermatrix, "r")
	
	if args.phyx_location:
		phyx_loc = args.phyx_location
	else:
		phyx_loc = ""
	
	
	if args.log_file:
		outlog = args.log_file
	else:
		outlog = "log.log"
	print "Your log file is " + outlog
	outf_log = open(outlog, "w")
	
	#Writ some stuff to 
	outf_log.write("####Basic Info About the Analysis####\n")
	outf_log.write("Your Fasta File is " + args.supermatrix + "\n")
	outf_log.write("Path to phyx is " + args.phyx_location + "\n")
	
	#Get the fasta into a hash
	HASH = seq_utils.fasta_parse(fasta)
		
	

if __name__ == "__main__":
	main()
