
"""
this takes a newick string as instr
and reads the string and makes the 
nodes and returns the root node
"""
#This code will let you walk through a tree
#and act on nodes that you want to
import sys, tree_utils
from node import Node
 
#This takes in the newick and the
#seq data then puts them in a data
#structure that can be preorder or
#postorder traversed pretty easily
def build(instr):
	#print "Entered build"
	root = None
	index = 0
	nextchar = instr[index]
	begining = "Yep"
	keepgoing = True
	current_node = None
	#keeps going until the value becomes false
	while keepgoing == True:
		#This situation will only happen at the very beginning but
		#when it hits this it will create a root and change begining
		#to no
		if nextchar == "(" and begining == "Yep":
				
			root = Node()
			current_node = root
			begining = "No"
		#This happens anytime their is an open bracket thats not the
		#beginning
		elif nextchar == "(" and begining == "No":
		
			newnode = Node()
			current_node.add_child(newnode)
			current_node = newnode
		#This indicates that you are in a clade and tells the 
		#program to move back one to grab the sister to the clade
		elif nextchar == ',':
		
			current_node = current_node.parent
		#This says you are closing a clade and therefore it moves
		#back to where the parent node is which allows the name
		#to be added to the parent node
		elif nextchar == ")":
			#print "Closing Clade"
			current_node = current_node.parent
			index += 1
			nextchar = instr[index]
			while True:
			
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				index += 1
				nextchar = instr[index]
			current_node.label = name
			index -= 1
		#This indicates everything is done so keepgoing becomes false
		elif nextchar == ';':
		
			keepgoing = False
			break
		#This indicates you have branch lengths so it grabs the branch
		#lengths turns them into floats and puts them in the current node
		elif nextchar == ":":
			index += 1
			nextchar = instr[index]
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				branch += nextchar
				index += 1
				nextchar = instr[index]
			current_node.length = float(branch)
			index -= 1
		#This is for if anywhitespace exists
		elif nextchar == ' ':
		
			index += 1
			nextchar = instr[index]
		#This is for when any taxa name is hit, it will concatenate
		#the taxa names together and add the name
		else: # this is an external named node
		
			newnode = Node()
			current_node.add_child(newnode)
			current_node = newnode
			current_node.istip = True
			while True:
				if nextchar == ',' or nextchar == ')' or nextchar == ':' \
					or nextchar == ';' or nextchar == '[':
					break
				name += nextchar
				index += 1
				nextchar = instr[index]
			current_node.label = name
			index -= 1
		if index < len(instr) - 1:
			index += 1
		nextchar = instr[index]
		name = ""
		branch = ""
	return root

def pretty_up(clade):
	
	name = ""
	prev_char = ""
	keepgoing = "true"
	for i in clade:
		if i == ")" and prev_char != ",":
			if keepgoing == "true":
				name = name + ","
			keepgoing = "false"
		if i == "(":
			keepgoing = "true"
		if keepgoing == "true" and i != "(":
			name += i
			prev_char = i
	#print name
		

	return(name+",")

'''
Performs the postorder traversal and returns a clade under the assumption
it has met a cutoff if a cutoff is given
'''
def postorder(root,cutoff, array):
	
	clade_array = []
	for i in root.children:
		if i.children:
			if i.label:
				clade = ""
				if(cutoff <= int(i.label)):
					#print "Here is Label: " + str(i.label)
					#print "Here is I.child: " + str(i.children)
					for j in i.children:
						clade = clade + pretty_up(str(j))
					clade_array = clade.split(",")
					#print "Here is clade: " 
					clade_array = filter(None, clade_array)
					array.append(sorted(clade_array))
			else:
				print i.children
				for j in i.children:
					clade = clade + pretty_up(str(j))
				clade_array = clade.split(",")
				print "Here is clade: " 
				clade_array = filter(None, clade_array)
		#print array
		postorder(i,cutoff, array)
	return array
	
	
def trees_to_bipart(tree_input,cutoff):
	
	test = []
	array = []
	tropen = open(tree_input, "r")
	for i in tropen:
		n_temp = build(i)
		array = postorder(n_temp,cutoff, test)
	output = []
	for x in array:
		if x not in output:
			output.append(x)
	return output
	

if __name__ == "__main__":
	s = "((Spol,Beta),((WPYJ,Retr),((RuprSFB,MJM3360),((MJM2940,DrolusSFB),((DrobinSFB,(MJM1652,Dino)),(NepSFB,Neam))))));"
	n2 = build(s)
	test = Node()
	#print node.get_newick_repr(True)
	#tree_utils.calc_biparts_support(n2)
	postorder(n2)
	
