from __future__ import division
import csv
import plotly.plotly as py
import plotly.graph_objs as go
import math

Nu=943
Ni=1682

py.sign_in('ynyeh0221', 'cwg3vrmt9o')

with open("u1base.tsv") as ff:
        data=[tuple(line) for line in csv.reader(ff, delimiter="\t")]
Matrix = [[0 for x in range(Ni)] for x in range(Nu)]
s=0
for i in xrange(len(data)):
        Matrix[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])
        s+=int(data[i][2])
mu=s/len(data)
bui = [[0 for x in range(Ni)] for x in range(Nu)]
bu=[0]*Nu
for i in xrange(Nu):
    ss=0
    l=0
    for j in xrange(Ni):
        if Matrix[i][j]>0:
            ss+=int(Matrix[i][j])
            l+=1
    bu[i]=round(ss/l-mu,2)
bi=[0]*Ni
for j in xrange(Ni):
    ss=0
    l=0
    for i in xrange(Nu):
        if Matrix[i][j]>0:
            ss+=int(Matrix[i][j])
            l+=1
    if l>0:
        bi[j]=round(ss/l-mu,2)
for i in xrange(Nu):
    for j in xrange(Ni):
        bui[i][j]=round(mu+bu[i]+bi[j],2)
S=0
sss=0
for i in xrange(Nu):
    for j in xrange(Ni):
        if Matrix[i][j]>0:
            S+=1
            sss+=(bui[i][j]-Matrix[i][j])**2
print round(math.sqrt(sss/S),2)
            
