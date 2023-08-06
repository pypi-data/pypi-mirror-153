import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils import shuffle
from intentron.utils import *
from intentron.utils.fmt import *


def infer():
    data = shuffle(pd.read_csv('samples-2d.csv'))

    x = data.drop(columns=['label'])
    y = data['label']
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.67, random_state=42, shuffle=True)

    n = 9
    count = np.array(y_train.value_counts())
    activities = y_train.unique()
    # print(activities)
    colors = cm.rainbow(np.linspace(0, 1, 4))
    plt.figure(figsize=(10, 6))
    plt.bar(activities, count, width=0.3, color=colors)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(rotation=45, fontsize=12)
    # touch('img')
    # plt.savefig('img/counts.png')

    # accuracy_scores = np.zeros(n)
    labels = np.unique(y.tolist())

    # clf = SVC().fit(x_train, y_train)
    # pred = clf.predict(x_test)
    # accuracy = accuracy_score(y_test, pred) * 100
    # print('SVM accuracy: {}%'.format(accuracy))
    # confm = pd.DataFrame(confusion_matrix(y_test, pred))
    # confm.to_csv('/home/dm/Work/svm.csv')
    # print(np.unique(pred))
    # print(len(pred.unique()), len(labels), len(clf.classes_), confm.shape)
    # print(list(set(temp1) - set(temp2)))

    # disp = ConfusionMatrixDisplay(confusion_matrix=confm, display_labels=clf.classes_)
    # disp.plot()
    # plt.savefig('/home/dm/Work/svm.csv')

    clf = LogisticRegression(solver='lbfgs', class_weight='balanced', max_iter=10000).fit(x_train, y_train)
    pred = clf.predict(x_test)
    accuracy = accuracy_score(y_test, pred) * 100
    print('LR accuracy: {}%'.format(accuracy))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/lr.csv')
    log = open('/home/dm/Work/lr.txt', 'w')
    log.write(str(clf.classes_.tolist()))

    '''
    clf = RandomForestClassifier().fit(x_train, y_train)
    pred = clf.predict(x_test)
    accuracy = accuracy_score(y_test, pred) * 100
    print('RF accuracy: {}%'.format(accuracy))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/rf.csv')
    log = open('/home/dm/Work/rf.txt', 'w')
    log.write(str(clf.classes_.tolist()))

    clf = KNeighborsClassifier().fit(x_train, y_train)
    pred = clf.predict(x_test)
    accuracy = accuracy_score(y_test, pred) * 100
    print('KNN accuracy: {}%'.format(accuracy))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/knn.csv')
    log = open('/home/dm/Work/knn.txt', 'w')
    log.write(str(clf.classes_.tolist()))
    '''

    '''
    clf = GaussianProcessClassifier(1.0 * RBF(1.0)).fit(x_train, y_train)
    pred = clf.predict(x_test)
    accuracy = accuracy_score(y_test, pred) * 100
    print('RBF accuracy: {}%'.format(accuracy))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/rbf.csv')

    clf = GaussianNB().fit(x_train, y_train)
    pred= clf.predict(x_test)
    accuracy_scores[4] = accuracy_score(y_test, pred) * 100
    print('NB accuracy: {}%'.format(accuracy_scores[4]))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/nb.csv')

    clf = DecisionTreeClassifier(max_depth=7).fit(x_train, y_train)
    pred= clf.predict(x_test)
    accuracy_scores[6] = accuracy_score(y_test, pred) * 100
    print('DT accuracy: {}%'.format(accuracy_scores[6]))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/dt.csv')

    clf = AdaBoostClassifier().fit(x_train, y_train)
    pred= clf.predict(x_test)
    accuracy_scores[7] = accuracy_score(y_test, pred) * 100
    print('GB accuracy: {}%'.format(accuracy_scores[7]))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/gb.csv')

    clf = MLPClassifier(alpha=1, max_iter=10000).fit(x_train, y_train)
    pred= clf.predict(x_test)
    accuracy = accuracy_score(y_test, pred) * 100
    print('MLP accuracy: {}%'.format(accuracy))
    confm = pd.DataFrame(confusion_matrix(y_test, pred, labels=labels))
    confm.to_csv('/home/dm/Work/mlp.csv')
    '''

    '''
    plt.figure(figsize=(12, 8))
    colors = cm.rainbow(np.linspace(0, 1, n))
    labels = ['RBF', 'SVM', 'LR', 'KNN', 'NB', 'RF', 'DT', 'GB', 'MLP']
    print(len(labels), len(accuracy_scores), len(colors))
    plt.bar(labels, accuracy_scores, color = colors)
    plt.xlabel('Algorithm', fontsize=18)
    plt.ylabel('Accuracy', fontsize=18)
    plt.title('Accuracy of various algorithms', fontsize=20)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig('img/accuracy.png')
    '''


def infer_job(src, dst):
    infer()


if __name__ == '__main__':
    infer()
