import sys
import tree_reader
import tree_utils
import node

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "python "+sys.argv[0]+" infile.trees outfile.tre"
        sys.exit(0)
    
    trees = []
    maintree = node.Node()
    for i in tree_reader.read_tree_file_iter(sys.argv[1]):
        trees.append(i)
    
    lvsnms = set()
    for i in trees:
        for l in i.lvsnms():
            lvsnms.add(l)

    for i in lvsnms:
        nd = node.Node()
        nd.label = i
        maintree.add_child(nd)
    
    for i in trees:
        mr = tree_utils.get_mrca_wnms(i.lvsnms(),maintree)
        mvnds = set()
        for j in mr.children:
            if len(set(j.lvsnms()).intersection(set(i.lvsnms())) ) > 0:
                mvnds.add(j)
        nd = node.Node()
        for j in mvnds:
            mr.remove_child(j)
            nd.add_child(j)
        mr.add_child(nd)
    of = open(sys.argv[2],"w")
    of.write(maintree.get_newick_repr(False)+";\n")
    of.close()