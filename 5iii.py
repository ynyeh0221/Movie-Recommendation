from __future__ import division
import csv
import math
import itertools
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pylab

#Item-based collaborative filtering with Adjusted cosine similarity
Nu=943
Ni=1682

userscore=[0]*1682
jid=0
jscore=0

K=5

userscores=None
with open('u1test.tsv', 'r') as f:
    reader=csv.reader(f, delimiter="\t")
    data=list(reader)

userscores = [[0 for x in range(Ni)] for x in range(943)]
for i in xrange(len(data)):
    userscores[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])
    
tuserscores=None
with open('u1base.tsv', 'r') as f:
    reader=csv.reader(f, delimiter="\t")
    data=list(reader)

tuserscores = [[0 for x in range(Ni)] for x in range(943)]
for i in xrange(len(data)):
    tuserscores[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])
    
avgscores=[]
for i in xrange(943):
    ssss=0
    for j in xrange(Ni):
        if tuserscores[i][j]!=0:
            ssss+=1
    avgscores.append([sum(tuserscores[i])/ssss, userscores[i],i])
avgscores=sorted(avgscores,key=lambda x:x[0])

group1=[]
group2=[]
group3=[]
group4=[]
group5=[]
gap=(avgscores[len(avgscores)-1][0]-avgscores[0][0])/5
#print gap
for i in xrange(len(avgscores)):
    #print avgscores[i][0]
    if avgscores[i][0]>=avgscores[0][0] and avgscores[i][0]<avgscores[0][0]+gap:
        group1.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+gap and avgscores[i][0]<avgscores[0][0]+2*gap:
        group2.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+2*gap and avgscores[i][0]<avgscores[0][0]+3*gap:
        group3.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+3*gap and avgscores[i][0]<avgscores[0][0]+4*gap:
        group4.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+4*gap and avgscores[i][0]<avgscores[0][0]+5*gap:
        group5.append(avgscores[i][1])

js=[]
with open('./m_similarities.csv', 'r') as f:
    reader=csv.reader(f)
    joke_simi=[tuple(float(n) for n in line.split(",")) for line in f]

simi = [[0 for x in range(Ni)] for x in range(Ni)]
for i in xrange(len(joke_simi)):
    simi[int(joke_simi[i][0])][int(joke_simi[i][1])]=float(joke_simi[i][2])
    
Nu=len(group5)
check=[]
checkx=[]

with open('./g5k5.csv', 'wb') as fff:
    writer=csv.writer(fff)

    predition = [[0 for x in range(Ni)] for x in range(Nu)]
    for i in xrange(Nu):
        userscore=group5[i]
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
                writer.writerow([str(predition[i][j]-userscore[j])])

checksquare=map(lambda x: x ** 2, check)
print "RMSE"
print round(math.sqrt(sum(checksquare)/len(checksquare)),2)




