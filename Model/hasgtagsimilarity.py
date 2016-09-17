import pymysql
fn = open('lastGraphUsers.csv','r')
fj = open('hashtagsimilarity.csv','w')
usernamelist =[]
hashtag=[]
diction1 = dict()
content = fn.readlines()
db = pymysql.connect(host='localhost',user='root',passwd='1234', db='demo')
cur = db.cursor()
count =0
for i in content:
    i = i.strip()
    usernamelist.append(i)
    cur.execute("select distinct hashtag from tweet_hashtag where username = \'"+i +'\'')
    #print (count)
    tags =[]
    temp = cur.fetchall()
    print("count: " + str(count) + " listLength: " + str(len(temp)))
    for j in temp:
        tags.append(j[0])
    diction1[i]= tags
    count = count +1
    if count > 10:
        break

print (len(usernamelist))
for k in range(0,len(usernamelist)-1):
    for j in range(0,len(usernamelist)-1):
        if(k==j):
            print (0)
        else:
             templist = []
             templist.extend(diction1[usernamelist[k]])
             fj.write(usernamelist[k].replace("\n","").replace('"',''))
             fj.write("****")
             fj.write(usernamelist[j].replace("\n","").replace('"',''))
             fj.write(",")
             s1 = set(diction1[usernamelist[k]])
             s2 = set(diction1[usernamelist[j]])
             s3 = set(s1).intersection(s2)
             templist.extend(diction1[usernamelist[j]])
             z = templist
             s4 = set (z)
             if len(s4)!=0:
                jaccard = float(len(s3)/float(len(s4)))
                fj.write(str(jaccard))
                print ("jaccard---"+str(jaccard))
                fj.write("\n")
             else:
                fj.write(str(0)+'\n')

fj.close()
fn.close()



