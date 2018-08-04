import sys
import argparse
import os
import subprocess
import seq_utils, Folder_utils, bipart_utils, Tree_estimation_utils

'''
Arguments
'''

LICENSE = "Quick disclaimer, this is the follow up to the MGWE program! Original publication:\nAnalyzing contentious relationships and outlier genes in phylogenomics\nThis is more efficient and explores a greater amount of tree space. As suggested in the MGWE manuscript this creates constraint files and analyzes those A similar procedure was implemented in the MS:\nNested phylogenetic conflicts and deep phylogenomics in plants\nFeel free to edit etc...but please don't steal credit for the code. For questions: jfwalker@umich.edu\n"

def generate_argparser():

	#parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(
        prog="TdgeTest.py",
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
epilog=LICENSE)
	parser.add_argument("-s", "--supermatrix", required=True, type=str, help="""
	Supermatrix file in fasta, if not fasts use pxs2fa from the phyx package""")
	parser.add_argument("-q", "--partition", required=True, type=str, help="""
	Partition file, should be in RAxML readable format""")
	parser.add_argument("-t", "--trees", required=True, type=str, help="""
	List of trees to analyze, in default will estimate trees separately""")
	parser.add_argument("-z", "--relationship", required=True, type=str, help="""
	comma separated list of species in clade to test (Must be in first tree)""")
	parser.add_argument("-f", "--output_folder", required=False, type=str, help="""
	Name for the output folder, default is output_folder_EdgeTest""")
	parser.add_argument("-p", "--phyx_location", required=False, type=str, help="""
	path to phyx, default is in path""")
	parser.add_argument("-r", "--raxml", required=False, type=str, help="""
	Location of raxml-ng""")
	return parser

def main(arguments=None):
	
	parser = generate_argparser()
	args = parser.parse_args(arguments)
	arguments = sys.argv[1:]
	print "Here"




if __name__ == "__main__":
	main()
