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
	for i in fasta:
		i=i.strip("\n")
		if i[0] == '>':

			dic[prev_name]=seq
			seq_list.append(seq)
			name_list.append(i.strip(">"))
			seq = ""
			prev_name=i.strip(">")
		else:
			seq += i.upper()
			seqlength = len(seq)
			dic[prev_name] = seq
	return dic

'''
Read in partition file
'''

def partition_parse(partition):
	
	name_array = []
	length = []
	for i in partition:
		i=i.strip("\n")
		print i