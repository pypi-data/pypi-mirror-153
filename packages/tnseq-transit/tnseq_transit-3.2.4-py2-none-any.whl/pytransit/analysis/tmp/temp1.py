import sys
E = 0
for line in open(sys.argv[1]):
  if line[0]=='#': continue
  w = line.rstrip().split('\t')
  if w[-1]=='E': E += 1
print E
