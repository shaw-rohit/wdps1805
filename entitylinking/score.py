INPUTFILE = sys.argv[1]
OUTFILE = sys.argv[2]
ES_ADDRESS =sys.argv[3]
SPARQL_ADDRESS = sys.argv[4]

INPUT = {}
for line in open(INPUTFILE):
        record, string, entity = line.strip().split('\t', 2)
        INPUT[(record,string)] = entity
n_INPUT = len(INPUT)
print ('input: %s' % n_INPUT)
output = {}
for line in open(outputFile):
  record, string, entity =line.strip().split('\t',2)
  output[(record, string)]=entity
n_output =len(input)
print('output: %s' % n_output)


OUTPUT = {}for line in open(OUTFILE):
        record, string, entity = line.strip().split('\t', 2)
        OUTPUT[(record,string)] =entity
n_OUTPUT = len(OUTPUT)
print ('output: %s' % n_OUTPUT)


n_correct = sum( int(OUTPUT[i]==INPUT[i]) for i in set(INPUT) & set(OUTPUT))
print('correct: %s' % n_correct)
precision =float(n_correct) / float(n_OUTPUT)
print('precision: %s' % precision)
recall = float(n_correct) / float(n_INPUT)
print('recall: %s' % recall)
f1 = 2 *( (precision * recall) / (precision + recall) )
print('f1: %s' %f1)
