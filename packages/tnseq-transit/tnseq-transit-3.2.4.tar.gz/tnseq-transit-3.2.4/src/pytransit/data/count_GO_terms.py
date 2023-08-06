
terms = {}
for line in open("H37Rv_GO_terms.txt"):
  w = line.rstrip().split('\t')
  rv,term = w[0],w[1]
  if term not in terms: terms[term] = []
  terms[term].append(rv)

temp = []
for term in terms.keys(): temp.append((term,len(terms[term])))
temp.sort(key=lambda x: x[1],reverse=True)
for term,size in temp: print term,size

print 'total terms:',len(terms)
  

