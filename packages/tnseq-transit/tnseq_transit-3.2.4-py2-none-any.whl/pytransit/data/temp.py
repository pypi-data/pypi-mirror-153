genes = {}
for line in open("smeg_GO_terms.txt"):
  w = line.rstrip().split('\t')
  genes[w[0]] = 1
print len(genes.keys())
print genes.keys()[:20]
