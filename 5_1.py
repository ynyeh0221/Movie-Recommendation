from __future__ import division
import csv
import math
import itertools
from collections import Counter

Nu=943
Ni=1682

userscore=[0]*1682
jid=0
jscore=0

K=10

userscores=None
with open('uatest.tsv', 'r') as f:
    reader=csv.reader(f, delimiter="\t")
    data=list(reader)

userscores = [[0 for x in range(Ni)] for x in range(943)]
for i in xrange(len(data)):
    userscores[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])

js=[]
with open('./m_similarities.csv', 'r') as f:
    reader=csv.reader(f)
    joke_simi=[tuple(float(n) for n in line.split(",")) for line in f]
    
simi = [[0 for x in range(Ni)] for x in range(Ni)]
for i in xrange(len(joke_simi)):
    simi[int(joke_simi[i][0])][int(joke_simi[i][1])]=float(joke_simi[i][2])

check=[]

predition = [[0 for x in range(Ni)] for x in range(Nu)]
for i in xrange(Nu):
    userscore=userscores[i]
    similaritylist=[]
    for j in xrange(0,Ni):
        if userscore[j]!=0:
            simi_sum=0
            weighted_sum=0
            predit=0
            for k in xrange(0,Ni):
                if userscore[k]!=0 and simi[j][k]!=0:
                    similaritylist.append([userscore[k],simi[j][k]])
                elif userscore[k]!=0 and simi[k][j]!=0:
                    similaritylist.append([userscore[k],simi[k][j]])
            similaritylist=sorted(similaritylist, key=lambda x: x[1], reverse=True)
            if len(similaritylist)<K:
                K=len(similaritylist)
            similaritylist=similaritylist[0:K]
            #print similaritylist
            for k in xrange(K):
                simi_sum+=abs(similaritylist[k][1])
                weighted_sum+=similaritylist[k][1]*similaritylist[k][0]
            predit=weighted_sum/simi_sum
            predition[i][j]=round(predit,2)
            print predition[i][j]-userscore[j]
            check.append(predition[i][j]-userscore[j])

checksquare=map(lambda x: x ** 2, check)
print "RMSE"
print round(math.sqrt(sum(checksquare)/len(checksquare)),2)

