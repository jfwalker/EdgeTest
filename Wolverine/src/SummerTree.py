'''
This is the post Wolvering tree maker, different summaries of the tree
can be constructed
'''
import sys
import argparse
import os
import subprocess
import seq_utils, Folder_utils, bipart_utils, Tree_estimation_utils
import file_utils,Summary_utils

LICENSE = """
A series of methods for summarizing trees, feel free to use code
but please don't take credit for the code        
------------------------------------------------------------------------                                                              
email: jfwalker@umich.edu
"""


def generate_argparser():

	#parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(
        prog="SumAtree.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		epilog=LICENSE)
	parser.add_argument("-i", "--like_file", required=True, type=str, help="""
	Likelihood file from your previous analysis""")
	parser.add_argument("-j", "--just_clades", action="count", default=0, help="""
	Clades underlying your data, ordered by likelihood""")
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
	
	if args.just_clades:
		best_hash = Summary_utils.get_best(likelihood_file)
		sorted_arrays = file_utils.sort_hash(best_hash)
		names = sorted_arrays[0]
		values = sorted_arrays[1]
		for i in range(0,len(names)):
			#print "Relationship: " + names[i] + "\t" + str(values[i])
			if names[i] == "NoRel":
				the = "holder"
			elif names[i] == "GeneName":
				the = "holder"
			else:
				print "(" + names[i] + ")" +str(values[i]) + ";"
		



	
if __name__ == "__main__":
	main()

