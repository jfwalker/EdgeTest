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
	parser.add_argument("-l", "--l_diff", required=False,action="count", default=0, help="""
	Gets the likelihood difference each gene is from the no constraint""")
	parser.add_argument("-s", "--stat_diff", required=False, type=float, help="""
	If used you must specify a log likelihood difference, recommended is two. Will output a
	new matrix where 1 represents genes that are statistically significantly worse that having
	no constraint based on your specified cutoff and 0 represents those that are""")
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
	
	if args.l_diff:
		
		like_dif = []
		#Need an over haul
		like_dif = Summary_utils.get_like_dif(likelihood_file)
		for i in like_dif:
			temp = ""
			for j in i:
				temp = temp + str(j) + "\t"
			print temp		
		sys.exit()
	
	#This reaches a level of non-elegant impressive for even me
	if args.stat_diff:
		
		req_dif = args.stat_diff
		like_dif = []
		#Need an over haul
		like_dif = Summary_utils.get_like_dif(likelihood_file)
		sum_array = [0] * len(like_dif[0][1:])
		temp = ""
		for i in like_dif[0]:
			temp = temp + str(i) + "\t"
		print temp	
		for i in like_dif[1:]:
			temp = str(i[0]) + "\t"
			count = 0
			for j in i[1:]:
				if( j >= float(req_dif)):
					temp = temp + str(1) + "\t"
					sum_array[count] += 1
				else:
					temp = temp + str(0) + "\t"
				count += 1
			print temp
		temp = "Total\t"
		for i in sum_array:
			temp = temp + str(i) + "\t"
		print temp
		sys.exit()
	
if __name__ == "__main__":
	main()
