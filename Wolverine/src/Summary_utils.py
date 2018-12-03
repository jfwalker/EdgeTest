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

'''
Get all unique names from an array with the biparts
'''
def get_all_names_array(array):
	
	HASH = {}
	names_array = []
	newick = ""
	for i in array:
		temp_array = i.split(",")
		for j in temp_array:
			HASH[j] = j
	for i in HASH:
		if i != "NoRel":
			names_array.append(i)
			newick += i + ","
	newick = newick[0:-1]
	
	#returns an array with all the names and a newick of all
	return names_array, newick
	
	
def get_conflict_struct(conflicts):
	
	HASH = {}
	input = open(conflicts, "r")
	for i in input:
		i = i.strip("\n")
		if i[0:5] == "Clade":
			array = i.split(":")
			array2 = array[1].split("|")
			temp = array2[0][1:-1]
			HASH[temp] = []
		if i[0] == "\t":
			array3 = i.split(":")
			array22 = array3[1].split("|")
			temp2 = array22[0][1:-1].split(" ")
			HASH[temp].append(temp2)
	return HASH
	
'''
Take in the conflict structure, the clade of interest, and the Relationships held
For the name of interest find if it is in the conflict structure, then if it is
Check if any of it's conflicts are in the final rels
'''
def FindKeeper(conflict,name,FinalRels):
	
	array = []
	test_array = []
	test_array2 = []
	test = ""
	name = name.replace(",", " ")
	
	for i in FinalRels:
		i = i.replace(",", " ")
		array.append(i)
	match = set(array)

	
	#parse existing conflicts to see if they are in final rels
	for j in conflict[name]:

		for i in FinalRels:
		
			test_array = i.split(",")
			if len(test_array) == len(j):

				if len(match.intersection(j)) == 0:
					test = "true"
	
	if test == "true":
		return "hit"
	else:
		return "no_hit"
			
'''			
			for i in FinalRels:
				array = i.split(",")
				match = set(array)
				if len(match.intersection(j)) == 0:
					return "false"
				else:
					return "true"	
'''
	
	
	
	
	
	
	
