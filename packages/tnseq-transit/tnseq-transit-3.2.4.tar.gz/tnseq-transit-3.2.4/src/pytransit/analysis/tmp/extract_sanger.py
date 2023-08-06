for line in open("../data/H37Rv.sanger_associated_RVS.csv"):
  w = line.rstrip().split('\t')
  w = [x.strip() for x in w]
  for rv in w[2].split():
    role = w[0]
    # also add associations to parent roles for each gene
    print '\t'.join([rv,role])
    while '.' in role:
      role = role[:role.rfind('.')]
      print '\t'.join([rv,role])
  
  
