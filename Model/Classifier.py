__author__ = 'AJAYKUMAR'

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

traindata = np.loadtxt(open("Trainfeatures.txt","rb"),delimiter=",")
trainlabels = np.loadtxt(open("Trainlabels.txt","rb"),delimiter=",")
testdata = np.loadtxt(open("features_100.txt","rb"),delimiter=",")

print(len(traindata[:,0]))
print(len(traindata[0,:]))
print(len(trainlabels))

train = [x[0:] for x in traindata]
test = [x[0:] for x in testdata]

k_fold = cross_validation.KFold(len(train), n_folds=5)
for t, i in k_fold:
    print('Train: %s | test: %s' % (len(t), len(i)))

rfc = RandomForestClassifier(n_estimators=10)

accuracy1 = cross_validation.cross_val_score(rfc, train, trainlabels, cv=k_fold, n_jobs = 1)

rfc.fit(train,trainlabels)
np.savetxt('prediction.txt', rfc.predict(test),fmt='%d')

print(accuracy1)
print(accuracy1.mean())