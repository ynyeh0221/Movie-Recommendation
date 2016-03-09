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
    if avgscores[i][0]>=0 and avgscores[i][0]<avgscores[0][0]+gap:
        group1.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+gap and avgscores[i][0]<avgscores[0][0]+2*gap:
        group2.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+2*gap and avgscores[i][0]<avgscores[0][0]+3*gap:
        group3.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+3*gap and avgscores[i][0]<avgscores[0][0]+4*gap:
        group4.append(avgscores[i][1])
    elif avgscores[i][0]>=avgscores[0][0]+4*gap and avgscores[i][0]<=avgscores[0][0]+5*gap:
        group5.append(avgscores[i][1])
        
print len(group1)+len(group2)+len(group3)+len(group4)+len(group5)

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
with open('./p4m13g5.csv', 'wb') as fff:
    writer=csv.writer(fff)
    for i in xrange(Nu):
        for j in xrange(Ni):
            if userscores[i][j]!=0:
                bui[i][j]=round(mu+bu[i]+bi[j],2)
                print bui[i][j]-userscores[i][j]
                check.append(bui[i][j]-userscores[i][j])
                writer.writerow([str(bui[i][j]-userscores[i][j])])
        
checksquare=map(lambda x: x ** 2, check)
print "RMSE"
print round(math.sqrt(sum(checksquare)/len(checksquare)),2)
            
