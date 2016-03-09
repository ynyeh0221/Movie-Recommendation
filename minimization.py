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
for i in xrange(Nu):
    for j in xrange(Ni):
        if userscores[i][j]>0:
            bui[i][j]=round(beta[i][j]+mu,2)
            check.append(round(bui[i][j]-userscores[i][j],2))
checksquare=map(lambda x: x ** 2, check)
print "RMSE"
print round(math.sqrt(sum(checksquare)/len(checksquare)),2)
