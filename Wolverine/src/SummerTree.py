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
        prog="EdgeSummarizer.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
		epilog=LICENSE)
	parser.add_argument("-i", "--like_file", required=True, type=str, help="""
	Likelihood file from your previous analysis""")
	return parser


def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]



	
if __name__ == "__main__":
	main()

