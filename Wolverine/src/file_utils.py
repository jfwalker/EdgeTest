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

	for i in concord:
		print i.strip("\n")
		
		
def get_conflict_file(con):

	for i in con:
		i.strip("\n")