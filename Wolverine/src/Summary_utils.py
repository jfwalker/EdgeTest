import node
import sys,os
import subprocess
import tree_utils, tree_reader
import bipart_utils
import math

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
Take in an ever expanding array of conflicts and see if one should be added or no
add if no intersection, add if the intersection is 100%
'''
def FindKeeper(name,FinalRels):
	
	#print name
	match = ()
	array = name.split(",")
	match = set(array)
	count = 0
	

	
	for i in FinalRels:
		
		array2 = i.split(",")
		#Check if no name the array
		if len(match.intersection(array2)) == 0:
			count += 1
		#Check if the name is 100% in the array
		if len(match.intersection(array2)) == len(array2):
			count += 1
		if len(match.intersection(array2)) == len(array):
			count += 1
		
	if count == (len(FinalRels)):
		return "true"
	else:
		return "false"

'''
This calculates entropy a la modification to Shannon 1948 by Salichos 2014
This doesn't count trees as the conflict it counts biparts, aka can have more than
one conflicting bipart
'''
def calculate_entropy(names_array,concordance_hash,conflict_hash):
	
	
	#Maybe return some structure that does like clade freq ICA
	results_array = []
	
	HASH = {}
	count = 1
	#names_array should match the other files in the order
	for i in names_array:
	
		results = ""
		array = []
		HASH = {}
		array.append(len(concordance_hash[i]))
		focal = "largest"
		for j in conflict_hash[i]:
			
			temp = ""
			for k in j:
				temp += k + " "
			temp = temp[0:-1]
			if temp in HASH:
				HASH[temp] += 1
			else:
				HASH[temp] = 1
		#array contains first the largest conflict and next the total conflicts
		for k in HASH:
			array.append(HASH[k])
			#get wether focal clade is largest
			if array[0] < HASH[k]:
				focal = "not_largest"
			
		#math.log(count_of_bipart/total_trees)
		if focal == "largest":
			x = 1.0
		else:
			x = -1.0

		if 1 == len(array):
			x += 0.0
		else:	
			for k in array:
				freq = float(k) / float(sum(array))
				size_array = float(sum(array))
				x += (freq * math.log(freq, size_array))
		results += "Clade " + str(count) + ":\t" + i.strip("\n") + "\t" + str(array[0]) + "\t" + str(sum(array)) + "\t" + str(x)
		count += 1
		results_array.append(results)
	return results_array
		#print i
		#print array	
			
			
'''			
			for i in FinalRels:
				array = i.split(",")
				match = set(array)
				if len(match.intersection(j)) == 0:
					return "false"
				else:
					return "true"	
'''
	
	
	
	
	
	
	
