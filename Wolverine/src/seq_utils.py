import sys,os


'''
Read in a fasta
'''
def fasta_parse(fasta):

	name_list=[]
	seq_list=[]
	dic={}
	seq=""
	prev_name=""
	count = 0
	for i in fasta:
	
		i=i.strip("\n")
		if i[0] == '>':
			if count != 0:
				dic[prev_name]=seq
				name_list.append(prev_name)
			
			seq = ""
			prev_name = i.strip(">")
		else:
			seq += i.upper()
			
		count += 1
	dic[prev_name] = seq
	name_list.append(prev_name)
	return dic,name_list

'''
Read in partition file
'''

def partition_parse(partition):
	
	name_array = []
	length = []
	part_hash = {}
	for i in partition:
		i=i.strip("\n")
		length = i.split("=")
		length[1] = length[1].strip(" ")
		#name_array = i.replace(",", " ").replace("=", " = ").split(" ")
		i = i.replace(" ","").replace("=",",")
		name_array = i.split(",")
		#print name_array[1]
		part_hash[name_array[1]] = length[1]
	return part_hash

def get_rel(rel):
	temp = []
	for i in rel:
		temp.append(i.strip("\n"))
	return temp
