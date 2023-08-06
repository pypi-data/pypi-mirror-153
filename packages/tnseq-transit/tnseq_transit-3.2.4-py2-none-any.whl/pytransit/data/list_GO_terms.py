GO = {}
for line in open("GO_term_names.dat"):
  w = line.rstrip().split('\t')
  GO[w[0]] = w[1]

genes = {}
for line in open("/pacific/home/ioerger/genomics/H37Rv3.prot_table"):
  w = line.rstrip().split('\t')
  genes[w[8]] = w[7]

terms = {}
for line in open("H37Rv_GO_terms.txt"):
  w = line.rstrip().split('\t')
  rv,term = w[0],w[1]
  if term not in terms: terms[term] = []
  terms[term].append(rv)

parents = {}
OBOfile = "gene_ontology.1_2.3-11-18.obo"
for line in open(OBOfile):
      if line[:3]=="id:": id = line[4:-1]
      if line[:5]=="is_a:":
        parent = line.split()[1]
        if id not in parents: parents[id] = []
        parents[id].append(parent)
      if len(line)<2: id = None
      #if line[:5]=="name:": ontology[id] = line[6:-1]


temp = []
for term in terms.keys(): temp.append((term,len(terms[term])))
temp.sort(key=lambda x: x[1],reverse=True)
for term,size in temp: 
  label = GO.get(term,"?")
  if "iron" in label or "ferric" in label or "heme" in label or "siderophore" in GO:
    vals = [term,','.join(parents.get(term,"?")),GO.get(term,"?"),size]
    s = ""
    for rv in terms[term]: s += "%s/%s, " % (rv,genes.get(rv,"-"))
    vals.append(s)
    print '\t'.join([str(x) for x in vals])

  

