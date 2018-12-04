# -*- coding: utf-8 -*-
'''
This is a series of methods for summarizing the conflict
'''


import sys
import argparse
import os
import subprocess
import seq_utils, Folder_utils, bipart_utils, Tree_estimation_utils
import file_utils,Summary_utils

LICENSE = """
A series of methods for summarizing conflict, feel free to use code
but please don't take credit for the code or what not. At least
wait until I have a stable job and am not a contract postdoc        
------------------------------------------------------------------------                                                              
email: jfwalker@umich.edu
"""


def generate_argparser():

	#parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(
        prog="SumCon.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		epilog=LICENSE)
	parser.add_argument("-i", "--like_file", required=False, type=str, help="""
	Likelihood file from your previous analysis""")
	parser.add_argument("-c", "--conflict_file", required=False, type=str, help="""
	Conflict file generated by Wolverine.py""")
	parser.add_argument("-d", "--concordance_file", required=False, type=str, help="""
	Concordance file output by Wolverine.py""")
	parser.add_argument("-e", "--calc_entropy", required=False, type=str, help="""
	A rough entropy calculation, needs conflict and concordance file""")
	parser.add_argument("-o", "--output_file", required=False, type=str, default=0, help="""
	output file, or else will go to terminal""")
	return parser


def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]
	likelihood_file = []
	#Get the info likelihood file
	
	#Take in the like file, future stuff for this
	
	if args.like_file:
		like = open(args.like_file, "r")
		likelihood_file = file_utils.get_like_file(like)
		like.close()
	
	if args.concordance_file:
		concord = open(args.concordance_file, "r")
		concordance_file = file_utils.get_concordance_file(concord)
		concord.close()
	
	if args.conflict_file:
		con = open(args.conflict_file, "r")
		conflict_file = file_utils.get_conflict_file(con)
		con.close()
	
	
	
	
if __name__ == "__main__":
	main()