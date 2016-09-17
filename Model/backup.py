__author__ = 'AJAYKUMAR'

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation

traindata = np.loadtxt(open("features_random.txt","rb"),delimiter=",")
result = np.loadtxt(open("labels_new_random.txt","rb"),delimiter=",")
testdata = np.loadtxt(open("features_test.txt","rb"),delimiter=",")

print(len(traindata[:,0]))
print(len(traindata[0,:]))
print(len(result))

train = [x[0:] for x in traindata]
test = [x[0:] for x in testdata]

'''
X_train, X_test, y_train, y_test = cross_validation.train_test_split(train,result , test_size=0.2, random_state=0)
rfc = RandomForestClassifier(n_estimators=10).fit(X_train,y_train)
sc = rfc.score(X_test, y_test)
print(sc)
'''


k_fold = cross_validation.KFold(len(train), n_folds=5)
for t, i in k_fold:
    print('Train: %s | test: %s' % (len(t), len(i)))

rfc = RandomForestClassifier(n_estimators=10)

accuracy1 = cross_validation.cross_val_score(rfc, train, result, cv=k_fold, n_jobs = 1)

rfc.fit(train,result)
np.savetxt('final.txt', rfc.predict(test),fmt='%d')

print(accuracy1)
print(accuracy1.mean())__author__ = 'AJAYKUMAR'
