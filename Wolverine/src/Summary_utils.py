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

'''
Changes your matrix into the difference between the first data column and 
the next few rows
'''
def get_like_dif(like_array):

	diff_array = []
	diff = 0.0
	diff_array.append(like_array[0])
	for i in like_array[1:]:
		new_row = []
		new_row.append(i[0])
		for j in i[1:]:
			diff = float(i[1]) - float(j)
			new_row.append(diff)
		diff_array.append(new_row)
	return diff_array
