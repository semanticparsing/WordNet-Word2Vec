import os
import sys

relations = []

class SemanticPair:
     def __init__(self, value, relationone, relationtwo):
         self.value = float(value)
         self.relationone = relationone
         self.relationtwo = relationtwo

for line in sys.stdin:
	vals = line.replace("\n", "").split("\t")
	relations.append(SemanticPair(vals[0], vals[1], vals[2]))

relations.sort(key=lambda x: x.value, reverse=True)

for r in relations:
	print str(r.value) + "\t" + r.relationone + "\t" + r.relationtwo