import json
import pprint
#import mysql
import pymysql
import networkx as nx
import operator

def graphUsers(tableName, fileName1, fileName2):
    db = pymysql.connect(host='localhost',user='root', passwd='1234', db='interaction')
    cur = db.cursor()
    #cur.execute('SELECT username,retweetname FROM user_tweet WHERE retweetflag = 1')
    cur.execute('SELECT username, retweetname FROM ' + tableName + ' WHERE retweetflag = 1')
    #print('SELECT username, retweetname FROM ' + tableName + ' WHERE retweetflag = 1')
    names = cur.fetchall()
    id = 1
    f = open(fileName1, 'w')
    fanon = open(fileName2, 'w')
    userdict = dict()
    i=0
    for name in names:
        x = -1
        y = -1
        if userdict.get(name[0]) == None:
            userdict[name[0]] = id
            x = id
            id+=1
        else:
            x = userdict[name[0]]

        if userdict.get(name[1]) == None:
            userdict[name[1]] = id
            y = id
            id+=1
        else:
            y = userdict[name[1]]
        f.write(str(x)+ ',' + str(y)+'\n')
        # i+=1
        # if i > 100:
        #     break

    for item,val in userdict.items():
        fanon.write(str(item) + ',' + str(val)+'\n')

    f.close()
    fanon.close()



def cleanGraph():
    f = open('retweetGraph.csv', 'r')
    fanon = open('cleanedRetweetGraph.csv', 'w')
    i=0
    finalList = set()
    for lines in f.readlines():
        list = lines.strip().split(',')
        edge = (list[0],list[1])
        #print(edge)
        finalList.add(edge)
        # i+=1
        # if i > 100:
        #     break

    #print(finalList)

    for items in finalList:
        fanon.write(items[0]+','+items[1]+'\n')

    f.close()
    fanon.close()


def graph(G, fileName):
    fAnom = open(fileName,'r')
    i=0
    for line in fAnom:
        users = line.strip().split(',')
        left = int(users[0])
        right = int(users[1])

        G.add_edge(left,right)


def calculateCliques(fileName):
    G = nx.Graph()
    graph(G, fileName)
    f = open('cliqueNodes.csv','w')
    nodeset = set()
    cliqueList = list(nx.k_clique_communities(G,12))
    print(cliqueList)
    for clique in cliqueList:
        l = list(clique)
        #print(l)
        for nodes in l:
           nodeset.add(nodes)

    for nodes in nodeset:
        f.write(str(nodes)+'\n')

    f.close()

def cliqueUsers():
    f = open('cliqueNodes.csv','r')
    fanon = open('anonymNames.csv', 'r')
    fu = open('cliqueUserNames.csv','w')
    anonDict = dict()
    i=0
    for lines in fanon.readlines():
        linelist = lines.strip().split(',')
        anonDict[linelist[1]] = linelist[0]

    for lines in f.readlines():
        l = lines.strip()
        print(l)
        fu.write(anonDict[l]+'\n')

    fu.close()
    f.close()
    fanon.close()

def createLabels():
    graphUsers('cliqueUsers', 'cliqueUseredges.csv', 'anonymCliqueGraph.csv')
    G = nx.Graph()
    graph(G, 'cliqueUseredges.csv')
    nodes = G.nodes()
    #print(nodes)
    nodeDegree = nx.degree(G,nodes)
    print(nodeDegree)
    count = 0
    users = []
    fanon = open('anonymCliqueGraph.csv','r')
    fuday = open('lastGraphUsers.csv','w')
    fwithdeg = open('lastGraphUsersWithDegree.csv','w')
    anonDict = dict()
    for lines in fanon.readlines():
        linelist = lines.strip().split(',')
        anonDict[linelist[1]] = linelist[0]

    sorted_x = sorted(nodeDegree.items(), key=operator.itemgetter(1))
    print(sorted_x)
    for node in sorted_x:
        if node[1] > 2:
            count+=1
            users.append(anonDict[str(node[0])])
            fuday.write(anonDict[str(node[0])] + '\n')
            fwithdeg.write(anonDict[str(node[0])] + ',' + str(node[1]) + '\n')
    print(len(users))
    fuday.close()
    fwithdeg.close()

def cliqueUsertweetTable():
    fu = open('cliqueUserNames.csv','r')
    db = pymysql.connect(host='localhost',user='root', passwd='1234', db='interaction')
    cur = db.cursor()
    cur.execute('INSERT INTO cliqueUsers1 SELECT *FROM user_tweet WHERE 1 = 0')
    for lines in fu.readlines():
        l = lines.strip()
        cur.execute('INSERT INTO cliqueUsers1 SELECT * FROM user_tweet WHERE username = \'' + l + '\'' )

    db.commit()


graphUsers('user_tweet', 'retweetGraph.csv', 'anonymNames.csv')
cleanGraph()
calculateCliques('cleanedRetweetGraph.csv')
cliqueUsers()
cliqueUsertweetTable()
createLabels()
