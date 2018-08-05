import node
import sys,os
import subprocess
import tree_utils, tree_reader
import bipart_utils

'''
Takes in the array of array like file and returns a hash with the summarize
relationships
'''
def get_best(like_file):
	
	HASH = {}
	#make an array of floats
	sum_array = [0.0] * len(like_file[0][1:])
	header_array = like_file[0][1:]
	#first line is the header so f that
	for i in like_file[1:]:
		
		count = 0
		for j in i[1:]:
			sum_array[count] += float(j)
			count += 1
	#print sum_array
	#print header_array
	for i in range(0,len(sum_array)):
		HASH[header_array[i]] = sum_array[i]
	return HASH

