'''
This is a set of ways to summarize the data
Logic behind a separate program is so that you're forced
to think about the analysis you are doing. So please only
choose one option at a time
'''
import sys
import argparse
import os
import subprocess
import seq_utils, Folder_utils, bipart_utils, Tree_estimation_utils
import file_utils,Summary_utils

LICENSE = """
The reason only one will work at once is to
avoid an overload of results.           
------------------------------------------------------------------------                                                              
email: jfwalker@umich.edu
"""

def generate_argparser():

	#parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(
        prog="EdgeSummarizer.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		epilog=LICENSE)
	parser.add_argument("-i", "--like_file", required=True, type=str, help="""
	Likelihood file from your previous analysis""")
	parser.add_argument("-b", "--best_rel", required=False,action="count", default=0, help="""
	Checks for the best relationship among all""")
	parser.add_argument("-p", "--penalty_rel", required=False,action="count", default=0, help="""
	Get the likelihood penalty each relationship imposes""")
	parser.add_argument("-l", "--l_diff", required=False, type=str, help="""
	Gets the likelihood difference each gene is from the no constraint""")
	parser.add_argument("-r", "--relationship_file", required=False, action="count", default=0, help="""
	prints out a file with all the relationships""")
	return parser
	
	

def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]
	
	likelihood_file = []
	#Get the info likelihood file
	like = open(args.like_file, "r")
	likelihood_file = file_utils.get_like_file(like)
	like.close()
	# likelihood_file is an array of arrays with all the data of the likelihood
	# file stored in it
	
	
	best_hash = {}
	sorted_arrays = []
	if args.best_rel:
		best_hash = Summary_utils.get_best(likelihood_file)
		sorted_arrays = file_utils.sort_hash(best_hash)
		names = sorted_arrays[0]
		values = sorted_arrays[1]
		for i in range(0,len(names)):
			print "Relationship: " + names[i] + "\t" + str(values[i])
		sys.exit()
	
	if args.penalty_rel:
		best_hash = Summary_utils.get_best(likelihood_file)
		sorted_arrays = file_utils.sort_hash(best_hash)
		names = sorted_arrays[0]
		values = sorted_arrays[1]
		penalty = 0.0
		for i in range(0,len(names)):
			penalty = values[0] - values[i]
			print "Relationship: " + names[i] + "\t" + str(penalty)
		sys.exit()

	
	
if __name__ == "__main__":
	main()
