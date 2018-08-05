# PHAIL
PHylogenetic Analysis Into Lineages

Currently under significant developments (Although early EdgeTest.py is ready)
There should be a lot more coming shortly

### August 4th, EdgeTest.py has working early version

This is the constraint version of the MGWE method (it explores more tree space): 
SysBio: [Analyzing contentious relationships and outlier genes in phylogenomics](https://academic.oup.com/sysbio/advance-article/doi/10.1093/sysbio/syy043/5034973)

I will be updating this for edge based analyses from now on

If you choose to have conflicts identified you will need the programs phyx (specifically pxbp). If you want to only specify your own relationships `-o` phyx will not be used.

[phyx](https://github.com/FePhyFoFum/phyx)

This uses the always amazing raxml, specifically raxml-ng

[raxml-ng](https://github.com/amkozlov/raxml-ng)

This program will calculate the likelihood of an edge using a series of constraints that define the edge.

inputs are:

`-s` Supermatrix file in fasta format

`-q` Partition file (raxml formatted)

`-t` List of rooted trees, although the genes don't need complete sampling the rooted trees do

`-z` List of relationships, can be a file if you are using `-i` or on the command line if not. If using a file these should be comma separated and on separate lines if using `-o`

`-i` This tells the program you are using a file with relationships

`-o` This tells the program to avoid identifying conflicts and just calculate the likelihoods for the relationships given
`-p` This is the path to pxbp, assuming you are not using `-o`

`-f` This is the name of the folder you would like the output to go to (Default is output_folder_EdgeTest)

`-d` This is the number of threads you would like to use (probably not good to go above 4) can crash if you specify too many

`-r` This is the path to raxml-ng, by default it will assume it is in your path

`-v` This makes it a bit more verbose

To run the program giving a clade of interest in csv format (relationship.txt) and having all conflicts with that clade of interest identified and analyzed run. This will only use the first clade in relationship.txt

EX: `python src/EdgeTest.py -s Examples/EdgeTest.fa -q Examples/test.model -t Examples/Test.tre -z Examples/relationship_file.txt -i`

To analyze the edge likelihood of a set of clades you can run

EX: `python src/EdgeTest.py -s Examples/EdgeTest.fa -q Examples/test.model -t Examples/Test.tre -z Examples/relationship_file.txt -i -o`

The outfolder will contain

Likelihoods.txt: This is all the likelihoods for each constraint of each edge, along with a likelihood for if the genes had no constraints. The sum of these likelihoods is the likelihood for a given relationship. The difference between that likelihood and the likelihood of the constraint is the penalty having that relationship has on your likelihood score.

untestable.txt: This is when a constraint could not be made for a certain relationship (taxon sampling insufficient), thus likelihood was calculated without using a constraint.

DeletedTaxa.txt: This is a list of taxa that were not present in a gene, for book keeping.
conflicts.txt: This is created if you have pxbp identify conflicts against your clade of interest
