__author__ = 'VamshiKrishna'

import random

def prune():
    f = open('featuresinput.csv','r')
    fw = open('pruned.txt','w')
    count = 0
    oneCount = 0
    for lines in f.readlines():
        l = lines.strip().split(',')
        if l[len(l)-1] == '1':
            oneCount+=1
            fw.write(lines)

    print(oneCount)

    f.close()
    f = open('featuresinput.csv','r')
    for lines in f.readlines():
        l = lines.strip().split(',')
        if count % 40 == 0 and l[-1] == '-1':
            fw.write(lines)
            count+=1
        elif l[-1] == '-1':
            count+=1
    fw.close()



def randomize():
    f = open("pruned.txt","r")
    f3 = open("shuffle.txt","w")
    #f1 = open("features.txt","w")
    #f2 = open("labels_new.txt","w")
    list = []
    for line in f:
        list.append(line)
    random.shuffle(list)
    for line in list:
        f3.write(line)
    f3.close()

prune()
randomize()

def testSet():
    f = open('shuffle.txt','r')
    fs = open('trainSet.txt','w')
    fw = open('testSet.txt','w')
    count=0
    for lines in f.readlines():
        if count < 100:
            fw.write(lines)
        else:
            fs.write(lines)
        count+=1

    fs.close()
    fw.close()

testSet()

def formatSet(fileName, featureFileName, labelFileName):
    f = open(fileName,'r')
    ffeature = open(featureFileName,'w')
    flabels = open(labelFileName,'w')

    for lines in f.readlines():
        l = lines.strip().split(',')
        flabels.write(l[-1]+'\n')
        ffeature.write(l[0]+','+ l[1]+','+ l[2]+','+ l[3]+','+ l[4]+ '\n')

    flabels.close()
    ffeature.close()

formatSet('trainSet.txt', 'trainFeatures.txt', 'trainLables.txt')
formatSet('testSet.txt', 'testFeatures.txt', 'testLables.txt')