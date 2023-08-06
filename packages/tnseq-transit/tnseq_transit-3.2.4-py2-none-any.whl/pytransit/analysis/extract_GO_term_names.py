import sys

# /pacific/home/ioerger/U19/gene_ontology.1_2.obo-3-11-18

OBOfile = sys.argv[1]

ontology,parents = {},{}

for line in open(OBOfile):
  if line[:3]=="id:": id = line[4:-1]
  if line[:5]=="is_a:":
    parent = line.split()[1]
    if id not in parents: parents[id] = []
    parents[id].append(parent)
  if len(line)<2: id = None
  if line[:5]=="name:": ontology[id] = line[6:-1]

for key,val in ontology.items(): print '\t'.join([key,val])
