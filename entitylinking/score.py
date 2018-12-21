import sys
GoldFile = sys.argv[1]
PredFile = sys.argv[2]


Gold = {}
for line in open(GoldFile):
        record, string, entity = line.strip().split('\t', 2)
        Gold[(record,string)] = entity
n_Gold = len(Gold)
print ('input: %s' % n_Gold)

Pred = {}for line in open(PredFile):
        record, string, entity = line.strip().split('\t', 2)
        Pred[(record,string)] =entity
n_Pred = len(Pred)
print ('output: %s' % n_Pred)


n_correct = sum( int(Gold[i]==Pred[i]) for i in set(Gold) & set(Pred))
print('correct: %s' % n_correct)
precision =float(n_correct) / float(n_Pred)
print('precision: %s' % precision)
recall = float(n_correct) / float(n_Gold)
print('recall: %s' % recall)
f1 = 2 *( (precision * recall) / (precision + recall) )
print('f1: %s' %f1)
