import node
import sys,os
import subprocess
import tree_utils, tree_reader
import bipart_utils

def get_like_file(like):
	
	array = []
	array2 = []
	for i in like:
		i = i.strip("\n")
		array = i.split("\t")
		array2.append(array)
	return array2

def sort_hash(best_hash):
	
	name_array = []
	value_array = []
	both_array = []
	for key, value in sorted(best_hash.iteritems(), key=lambda (k,v): (v,k)):
		
		name_array.append(key)
		value_array.append(value)
	both_array.append(name_array[::-1])
	both_array.append(value_array[::-1])
	return both_array	

def get_concordance_file(concord):

	HASH = {}
	tree_name = ""
	names = []
	for i in concord:

		i = i.strip("\n")
		if i[0:5] == "Clade":
			array = i.split(":")
			array2 = array[1].split("|")
			temp = array2[0][1:-1]
			names.append(temp)
			HASH[temp] = []
		if i[0] == "\t":
			array3 = i.split(":")
			array22 = array3[0].split(" ")
			tree_name = array22[1] + " " + array22[2]
			HASH[temp].append(tree_name)
	return HASH,names
		
		
def get_conflict_file(con):

	HASH = {}
	names = []
	for i in con:
		i = i.strip("\n")
		if i[0:5] == "Clade":
			array = i.split(":")
			array2 = array[1].split("|")
			temp = array2[0][1:-1]
			HASH[temp] = []
			names.append(temp)
		if i[0] == "\t":
			array3 = i.split(":")
			array22 = array3[1].split("|")
			temp2 = array22[0][1:-1].split(" ")
			HASH[temp].append(temp2)
	return HASH,names