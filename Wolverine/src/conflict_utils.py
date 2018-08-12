# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import seq_utils, Folder_utils, bipart_utils, Tree_estimation_utils, read_a_tree

def summarize(all_info,biparts,OutFolder):
	
	out_conf = OutFolder + "/conflict_results.txt"
	conf = open(out_conf, "w")
	out_conc = OutFolder + "/concordance_results.txt"
	conc = open(out_conc, "w")
	
	print "( •_•) lets do this "
	count = 0
	for i in biparts:
		line = ""
		for y in i:
			line = line + y + " "
		conf.write("Clade " + str(count) + ": " + line + "\n")
		for j in all_info:
			t_count = 0
			for k in j:
				for l in k:
					print l[0]
					print l[1]
					print count
					if str(l[0]) == str(count) and str(l[1]) == "conflict":
						print "Here"
						conf.write("\tConflict Tree " + str(t_count) + ": " + str(l[2]) + "\n")
				t_count += 1
		count += 1
	
	
	
	print "( •_•)>⌐■-■"
	print "(⌐■_■) done"
	
def get_left(bipart):

	keepgoing = "true"
	left_array = []
	right_array = []
	for x in bipart:
		if x == "|":
			keepgoing = "false"
		else:
			if keepgoing == "true":
				left_array.append(x)
			else:
				right_array.append(x)
	return left_array, right_array

def miss_conflict(left_array, right_array, biparts, name_array):
	
	#print "This tree has missing data"
	#print "here is the bipart in question: " + str(left_array)
	#print "Here is the combo of taxa: " + str(right_array)
	all_taxa = left_array + right_array
	#identify the taxa that are missing
	#print "Here is the whole list: " + str(name_array)
	no_match = set(name_array)
	diff =list(no_match.symmetric_difference(all_taxa))
	#print "Here is the difference: " + str(diff)
	#Parse all the bipartitions (have a counter so a Hash can match the biparitions)
	r_array = []
	
	#count can be a way to associate bipartitions and trees
	count = 0
	for i in biparts:
		#print count
		test_left = []
		test_right = []
		test_left, test_right = get_left(i)
		return_array = []
		#splice out the extra with the available for your test, this removes
		#From your test the missing taxa of you clade
		#tot_test = test_left + test_right
		avail = set(all_taxa)
		#Here is where you create the new left
		new_left = list(avail.intersection(test_left))
		
		all_taxa2 = test_right + test_left
		avail2 = set(all_taxa2)
		new_left_bipart = list(avail.intersection(left_array))
		
		#print "here is the bipart in question: " + str(left_array)
		#print "Here is your test left: " + str(test_left)
		#print "Here is your test right: " + str(test_right)
		#Check if they are identical (aka easy congruence)
		left_match_test = set(new_left)
		diff_test_match = list(left_match_test.symmetric_difference(new_left_bipart))
		
		#Get intersection of test and bipart
		intersect = set(new_left)
		bipart_intersect = list(intersect.intersection(new_left_bipart))
		
		#print "Here is the differences in size: " + str(len(diff_test_match))
		#print "Here is new left bipart:" + str(new_left_bipart)
		#print "Here is new left: " + str(new_left)
		array_size_diff = abs(len(new_left) - len(diff_test_match))
		bipart_array_size_diff = abs(len(new_left_bipart) - len(diff_test_match))
		#print "Here is array diff size: " + str(array_size_diff)
		#print "Here is the length of the new bipart: " + str(len(new_left_bipart))
		
		#print bipart_intersect

		#print "Here is your test left: " + str(test_left)
		#print "here is the bipart in question: " + str(left_array)
		
		#This means you have no diffences left at the test match (easy congruence)
		if len(diff_test_match) == 0:
			h = ""
			#print "You have congruence: "
			#print "Here is your test left: " + str(test_left)
			#print "here is the bipart in question: " + str(left_array)
			#Check if the have overlap (left array) (If so check if the overlap conflicts or is the result of missing data) just missing data equals congruence, no missing data is lack of congruence
			#Add together the one in question and the one not in question then check if that is the size of the difference
			return_array.append(str(count))
			return_array.append("congruence")
			return_array.append(str(left_array))
			r_array.append(return_array)
			
		#this means that one is nested perfectly within another
		elif array_size_diff == len(bipart_intersect) or bipart_array_size_diff == len(bipart_intersect):
			h = ""
			#print "Cool nested, can't speak this clades good: "
			#print "Here is left test unstripped: " + str(test_left)
			#print "Here is your left bipart in question unstripped: " + str(left_array)
			#print "Here is your test left: " + str(new_left)
			#print "here is the bipart in question: " + str(new_left_bipart)
		
		#if there is no intesection then don't bother
		elif len(bipart_intersect) == 0:
			h = ""
			#print "There is no overlap"
			#print "Here is left test unstripped: " + str(test_left)
			#print "Here is your left bipart in question unstripped: " + str(left_array)
			#print "Here is your test left: " + str(new_left)
			#print "here is the bipart in question: " + str(new_left_bipart) 
				
		#This is triggered if there is not perfect congruence (ugh...)
		else:
			#print "There is conflict"
			#print "Here is left test unstripped: " + str(test_left)
			#print "Here is your left bipart in question unstripped: " + str(left_array)
			#print "Here is your test left: " + str(new_left)
			#print "here is the bipart in question: " + str(new_left_bipart)
			return_array.append(str(count))
			return_array.append("conflict")
			return_array.append(str(left_array))
			r_array.append(return_array)
		count += 1
	
	return r_array
					
				
	#If there's no over don't worry it


'''
Add this for future speed upgrades
'''
def no_miss_conflict(left_array, biparts):
	
	h = ""
	#print "No Missing data"

'''
Steps: Dissect tree 1 into bipartitions
Check if there is conflict and if there can be conflict
Assuming there is and analyze it
Need to account for missing taxa in gene trees and in
clades that have been found already
'''
def test_trees(biparts,name_list,Trees,cutoff):
	
	
	print "Mixing Tree Pools"
	tropen = open(Trees, "r")
	#print name_list
	all_info = []
	tree_info_array = []
	count = 0
	hit_count = 10
	for i in tropen:
		#print i
		if(count == hit_count):
			print "(>_<)> Mixed :" + str(count)
			hit_count += 10
		tree_info_array = []
		array = []
		test = []
		name_array = []
		test_tree = read_a_tree.build(i)
		name_array = read_a_tree.postorder_name_getter(test_tree, name_array)
		array = read_a_tree.postorder(test_tree,cutoff,test,name_array)
		#array here contains all bipartitions to test
		for j in array:
			info_array = []
			left_array = []
			right_array = []
			keepgoing = "true"
			for x in j:
				if x == "|":
					keepgoing = "false"
				else:
					if keepgoing == "true":
						left_array.append(x)
					else:
						right_array.append(x)
			total_len = len(left_array) + len(right_array)
			info_array = miss_conflict(left_array, right_array, biparts, name_list)
			tree_info_array.append(info_array)
		all_info.append(tree_info_array)
		count += 1
		#sys.exit()
	#print all_info
	#print "here"
	return all_info

