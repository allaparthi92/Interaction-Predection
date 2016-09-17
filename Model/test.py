__author__ = 'AJAYKUMAR'

count =0
count1=0
count2=0
count3=0

f = open("prediction.txt","r")
label1 = f.readlines()

h = open("labels_100.txt","r")
label2 = h.readlines()

i =0
for line in label1:
    if (label2[i].strip()=="1" and label1[i].strip()=="1"):
        count = count+1
    if (label2[i].strip()=="1" and label1[i].strip()=="-1"):
        count1=count1+1
    if (label2[i].strip()=="-1" and label1[i].strip()=="1"):
        count2 = count2+1
    if (label2[i].strip()=="-1" and label1[i].strip()=="-1"):
        count3 = count3+1
    i = i+1

print(count)
print(count1)
print(count2)
print(count3)