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
#print data
Matrix = [[0 for x in range(Ni)] for x in range(Nu)]
#print len(Matrix)
#print len(Matrix[0])
#print data[0]
#print data[0][2]
s=0
for i in xrange(len(data)):
        Matrix[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])
        s+=int(data[i][2])
mu=s/len(data)

userscores=None
with open('u1test.tsv', 'r') as f:
    reader=csv.reader(f, delimiter="\t")
    data=list(reader)

userscores = [[0 for x in range(Ni)] for x in range(943)]
for i in xrange(len(data)):
    userscores[int(data[i][0])-1][int(data[i][1])-1]=int(data[i][2])
    
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

Nu=len(group5)
usercores=group5
check=[]
with open('./p4m12g5.csv', 'wb') as fff:
    writer=csv.writer(fff)
    for i in xrange(Nu):
        for j in xrange(Ni):
            if userscores[i][j]==5:
                bui[i][j]=round(mu+bu[i]+bi[j],2)
                print bui[i][j]-userscores[i][j]
                check.append(bui[i][j]-userscores[i][j])
                writer.writerow([str(bui[i][j]-userscores[i][j])])
        
checksquare=map(lambda x: x ** 2, check)
print "RMSE"
print round(math.sqrt(sum(checksquare)/len(checksquare)),2)
            