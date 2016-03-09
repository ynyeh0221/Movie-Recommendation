import csv
import math
import itertools
from collections import Counter

Nu=943
Ni=1682

userLines=None
with open('uabase.tsv', 'r') as f:
    reader=csv.reader(f, delimiter="\t")
    data=list(reader)

userLines = [[0 for x in range(Ni)] for x in range(Nu)]
for i in xrange(len(data)):
    userLines[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])

userscore={}
usermean={}
for i in xrange(0,Nu):
    userscore[i]=map(float, userLines[i])
    sums=0
    notnull=0
    for j in xrange(0,Ni):
        print [i,j]
        if userscore[i][j]!=0:
            sums+=userscore[i][j]
            notnull+=1
    usermean[i]=sums/notnull
vectorMagnitudes = {}
for j in xrange(0,Ni):
    jokesscore[j]=[]
    for i in xrange(0,Nu):
        jokesscore[j].append(float(userLines[i][j])-usermean[i])
    temp=[x **2 if x!=0 else 0 for x in jokesscore[j]]
    vectorMagnitudes[j]=math.sqrt(sum(temp))

with open('./m_similarities.csv', 'wb') as f:
    writer=csv.writer(f)
    #writer.writerow(['jokeA', 'jokeB', 'similarity'])
    jokes=list(jokesscore)
    for i, jokeA in enumerate(jokes):
        for jokeB in jokes[i+1:]:
            vectorA=jokesscore[jokeA]
            vectorB=jokesscore[jokeB]
            similarity=sum([a * b  if a!=0 and b!=0 else 0 for a, b in zip(vectorA, vectorB)])
            similarity/=vectorMagnitudes[jokeA] * vectorMagnitudes[jokeB]
            writer.writerow([jokeA, jokeB, '%.4f'%similarity])
