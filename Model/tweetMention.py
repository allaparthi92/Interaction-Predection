import pymysql
import math

fs = open('lastGraphUsers.csv','r')
fd = open('similaritiesvalue.csv','w')
usernamelist =[]
hashtag=[]
diction1 = dict()
content = fs.readlines()
db = pymysql.connect(host='localhost',user='root', passwd='1234', db='demo')
cur = db.cursor()
count =0
for i in content:
    i = i.strip()
    usernamelist.append(i)
    cur.execute(" select distinct mention from tweet_mentions where username = \'"+i+"\'")
    tags =[]
    temp = cur.fetchall()
    for j in temp:
        tags.append(j[0])
    diction1[i] = tags
    count = count+1
    print("count: " + str(count) + " tags: " + str(len(temp)))
    if count > 10:
         break

for k in range(0,len(usernamelist)-1):
    for j in range(0,len(usernamelist)-1):
        if(k==j):
            print(0)
        else:
             templist = []
             templist.extend(diction1[usernamelist[k]])
             fd.write(usernamelist[k].replace("\n","").replace('"',''))
             fd.write("****")
             fd.write(usernamelist[j].replace("\n","").replace('"',''))
             fd.write(",")
             s1 = set(diction1[usernamelist[k]])
             s2 = set(diction1[usernamelist[j]])
             s3 = set(s1).intersection(s2)
             templist.extend(diction1[usernamelist[j]])
             z = templist
             s4 = set (z)
             if len(s4) != 0:
                 jaccard = float(len(s3)/float(len(s4)))
                 fd.write(str(jaccard))
                 fd.write(",")
                 print("jaccard---"+str(jaccard))
             else:
                 fd.write(str(0)+",")
             adamicadr=float(0)
             try:
                 for x in s3:
                    adamicadr = adamicadr + float(1/(math.log(len(x),2.732)))
                 fd.write(str(adamicadr))
                 fd.write(",")
             except ZeroDivisionError as err:
                fd.write("0")
                fd.write(",")

             fd.write(str((len(s1)*len(s2))))
             fd.write("\n")
fd.close()
 #------------------------hash tags----------------------------------------

