fa = open('similaritiesvalue.csv','r')
fd = open('retweetsimilaritalue.csv','r')
fj = open('hashtagsimilarity.csv','r')
fm = open('featuresinput.csv','w')
#f = open("labels.csv", "r")
#fm.write("users,feature1,feature2,feature3,feature4,feature5,label")
#fm.write("\n")
content = fa.readlines()
count=0
for i in content:
    count+=1
    line = i.strip().split(',')
    fm.write(line[1]+','+line[2]+','+line[3]+',')
    #fm.write(i.replace("\n",""))
    #fm.write(",")
    y = fj.readline().split(",")[1]
    fm.write(y.replace("\n",""))
    fm.write(",")
    x = fd.readline()
    y = x.split(",")[1]
    fm.write(y.replace("\n",""))
    fm.write(",")
    n = x.split(",")[2]
    fm.write(n.replace("\n",""))
    fm.write("\n")
    # print(count)
    # if count > 10:
    #     break
fm.close()