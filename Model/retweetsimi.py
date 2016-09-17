import pymysql
import math

fs = open('lastGraphUsers.csv','r')
fd = open('retweetsimilaritalue.csv','w')
usernamelist =[]
hashtag=[]
diction1 = dict()
content = fs.readlines()
db = pymysql.connect(host='localhost',user='root', passwd='1234',db='demo')
cur = db.cursor()
count =0
for i in content:
    i= i.strip()
    usernamelist.append(i)
    #print("select distinct retweetname from user_tweet_b where username = \'"+(i)+"\' and retweetflag = 1")
    cur.execute(" select distinct retweetname from user_tweet where username = \'"+(i)+"\' and retweetflag = 1")
    tags =[]
    temp = cur.fetchall()
    for j in temp:
        tags.append(j[0])
    diction1[i]= tags
    count = count+1
    print ("count: " + str(count) + " userlist: " + str(len(temp)))
    #Vary this counter accordingly..
    if count > 10:
        break

#print(usernamelist)

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
             if len(s4)!=0:
                 jaccard = float(len(s3)/float(len(s4)))
                 fd.write(str(jaccard))
                 fd.write(",")
             else:
                 fd.write(str(0))
                 fd.write(",")
             #print(usernamelist[j])
             #print(diction1[usernamelist[k]])
             if usernamelist[j] in diction1[usernamelist[k]]:
                 fd.write("1")
                 fd.write("\n")
             else:
                 fd.write("-1")
                 fd.write("\n")
fd.close()
fs.close()
 #------------------------hash tags----------------------------------------