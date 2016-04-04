import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn import preprocessing
from sklearn.metrics import classification_report
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import StackOverflowTextAnalysis as sota
from itertools import islice
import time
import concurrent.futures
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(cm, labels, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def print_top10(vectorizer, clf, class_labels):
    """Prints features with the highest coefficient values, per class"""
    feature_names = vectorizer.get_feature_names()
    for i, class_label in enumerate(class_labels):
        top10 = np.argsort(clf.coef_[i])[-10:]
        print("%s: %s" % (class_label,
              " ".join(feature_names[j] for j in top10)))


if __name__ == '__main__':
    labels = ['verybad', 'bad', 'good', 'verygood']

    verybad_head = []
    bad_head = []
    good_head = []
    verygood_head = []

    N = 1000

    start_time = time.time()

    with open('data/questions-verybad.csv') as verybad_file:
        verybad = islice(csv.DictReader(verybad_file), N)
        verybad_head = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in verybad
        ]

    with open('data/questions-bad.csv') as bad_file:
        bad = islice(csv.DictReader(bad_file), N)
        bad_head = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in bad
        ]

    with open('data/questions-good.csv') as good_file:
        good = islice(csv.DictReader(good_file), N)
        good_head = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in good
        ]

    with open('data/questions-verygood.csv') as verygood_file:
        verygood = islice(csv.DictReader(verygood_file), N)
        verygood_head = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in verygood
        ]

    questions = verybad_head + bad_head + good_head + verygood_head

    finished_loading_time = time.time()

    print("Loading data took {} seconds.".format(
        finished_loading_time - start_time
    )
    )

    start_feature_generation_time = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        features = executor.map(sota.create_and_generate_features, questions)

    finished_feature_generation_time = time.time()

    print("Generating features took {} seconds.".format(
        finished_feature_generation_time - start_feature_generation_time
    )
    )

    start_fit_transform_time = time.time()

    # tf = TfidfVectorizer()
    # X = tf.fit_transform(bodies)

    vectorizer = DictVectorizer()

    X = vectorizer.fit_transform(features)

    finished_fit_transform_time = time.time()

    print("Fit transform took {} seconds.".format(
        finished_fit_transform_time - start_fit_transform_time
    ))

    Y = ['verybad'] * len(verybad_head) + ['bad'] * len(bad_head) + \
        ['good'] * len(good_head) + ['verygood'] * len(verygood_head)

    start_splitting_time = time.time()

    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(
        X, Y, train_size=0.7, random_state=31, stratify=Y)

    finished_splitting_time = time.time()

    print("Cross Validation splitting took {} seconds.".format(
        finished_splitting_time - start_splitting_time
    ))

    start_normalising_time = time.time()

    X = preprocessing.maxabs_scale(X)
    #scaler = preprocessing.MaxAbsScaler()
    #scaler = preprocessing.MinMaxScaler()
    #X_train = scaler.fit_transform(X_train.todense())
    #X_test = scaler.transform(X_test.todense())

    finished_normalising_time = time.time()

    print("Normalising took {} seconds.".format(
        finished_normalising_time - start_normalising_time
    ))

    start_model_training_time = time.time()

    clf = RandomForestClassifier(
        n_estimators=10000, n_jobs=6, oob_score=True, random_state=50,
        max_features="auto", min_samples_leaf=50
    )

    #clf = MultinomialNB()

    #clf = svm.SVC(decision_function_shape='ovo')

    clf = clf.fit(X_train, Y_train)

    finished_model_training_time = time.time()

    print("Model Training took {} seconds.".format(
        finished_model_training_time - start_model_training_time
    ))

    start_predicting_time = time.time()

    predicted = clf.predict(X_test)

    finished_predicting_time = time.time()

    print("Predicting took {} seconds.".format(
        finished_predicting_time - start_predicting_time
    ))

    start_scoring_time = time.time()

    report = classification_report(Y_test, predicted)

    finished_scoring_time = time.time()

    print("Model Scoring took {} seconds.".format(
        finished_scoring_time - start_scoring_time
    ))

    print(report)

    #print_top10(vectorizer, clf, labels)

    matplotlib.rcParams.update({'font.size': 22})

    # Compute confusion matrix
    cm = confusion_matrix(Y_test, predicted)
    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization')
    print(cm)
    plt.figure()
    plot_confusion_matrix(cm, labels)

    # Normalize the confusion matrix by row (i.e by the number of samples
    # in each class)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print('Normalized confusion matrix')
    print(cm_normalized)
    plt.figure()
    plot_confusion_matrix(
        cm_normalized, labels, title='Normalized confusion matrix'
    )

    importances = clf.feature_importances_
    std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    feature_names = np.array([w[5:] for w in vectorizer.get_feature_names()])

    # Print the feature ranking
    print("Feature ranking:")
    for f in range(X.shape[1]):
        print("%d. %s (%f)" % (f + 1, feature_names[indices[f]], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), feature_names[indices], rotation='30')
    plt.xlim([-1, X.shape[1]])

    plt.show()
