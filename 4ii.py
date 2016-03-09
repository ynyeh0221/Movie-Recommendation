from __future__ import division
import csv
import plotly.plotly as py
import plotly.graph_objs as go
import math
import numpy as np
import numpy.matlib
from numpy.linalg import inv
from sklearn import linear_model

Nu=943
Ni=1682

with open("u1base.tsv") as ff:
	    data=[tuple(line) for line in csv.reader(ff, delimiter="\t")]
#print data
Matrix = [[0 for x in range(Ni)] for x in range(Nu)]
Matrix2 = [[0 for x in range(Ni)] for x in range(Nu)]

userscores=None
with open('u1test.tsv', 'r') as f:
    reader=csv.reader(f, delimiter="\t")
    data=list(reader)

userscores = [[0 for x in range(Ni)] for x in range(Nu)]
for i in xrange(len(data)):
    userscores[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])

s=0
ss=0
for i in xrange(len(data)):
    Matrix[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])
    Matrix2[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])
    s+=int(data[i][2])
    ss+=1
mu=s/ss

avgscores=[]
for i in xrange(Nu):
    ssss=0
    for j in xrange(Ni):
        if Matrix[i][j]!=0:
            ssss+=1
    avgscores.append([sum(Matrix[i])/ssss, userscores[i],i])
avgscores=sorted(avgscores,key=lambda x:x[0])

for i in xrange(Nu):
    for j in xrange(Ni):
        if Matrix2[i][j]>0:
            Matrix2[i][j]-=mu



group1=[]
group2=[]
group3=[]
group4=[]
group5=[]
for i in xrange(Nu):
    #print avgscores[i][0]
    if 1 in userscores[i]:
        group1.append(userscores[i])
    if 2 in userscores[i]:
        group2.append(userscores[i])
    if 3 in userscores[i]:
        group3.append(userscores[i])
    if 4 in userscores[i]:
        group4.append(userscores[i])
    if 5 in userscores[i]:
        group5.append(userscores[i])

Nu=len(group1)
usercores=group1


X=np.matlib.identity(Nu)
Xt=X.transpose()
XX=np.dot(Xt,X)

lambdaa=10
beta=np.dot(np.dot(inv(XX+lambdaa*np.matlib.identity(Nu)),Xt),Matrix2)
beta=beta.tolist()
bui = [[0 for x in range(Ni)] for x in range(Nu)]
check=[]



with open('./p4m22g1.csv', 'wb') as fff:
    writer=csv.writer(fff)
    for i in xrange(Nu):
        for j in xrange(Ni):
            if userscores[i][j]==1:
                bui[i][j]=round(beta[i][j]+mu,2)
                check.append(round(bui[i][j]-userscores[i][j],2))
                writer.writerow([str(bui[i][j]-userscores[i][j])])
checksquare=map(lambda x: x ** 2, check)
print "RMSE"
print round(math.sqrt(sum(checksquare)/len(checksquare)),2)
            
