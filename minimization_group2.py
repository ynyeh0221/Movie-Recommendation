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

py.sign_in('ynyeh0221', 'cwg3vrmt9o')

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

for i in xrange(Nu):
    for j in xrange(Ni):
        if Matrix2[i][j]>0:
            Matrix2[i][j]-=mu
X=np.matlib.identity(Nu)
Xt=X.transpose()
XX=np.dot(Xt,X)


lambdaa=10
beta=np.dot(np.dot(inv(XX+lambdaa*np.matlib.identity(Nu)),Xt),Matrix2)
beta=beta.tolist()
bui = [[0 for x in range(Ni)] for x in range(Nu)]
check=[]

Nu=len(group5)
userscores=group5
with open('./p4m23g5.csv', 'wb') as fff:
    writer=csv.writer(fff)
    for i in xrange(Nu):
        for j in xrange(Ni):
            if userscores[i][j]>0:
                bui[i][j]=round(beta[i][j]+mu,2)
                check.append(round(bui[i][j]-userscores[i][j],2))
                writer.writerow([str(bui[i][j]-userscores[i][j])])
checksquare=map(lambda x: x ** 2, check)
print "RMSE"
print round(math.sqrt(sum(checksquare)/len(checksquare)),2)
            
