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
from sklearn.cross_validation import StratifiedKFold, permutation_test_score
from sklearn.externals.six import StringIO
import html
import pydotplus
from sklearn.tree import export_graphviz
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def plot_confusion_matrix(cm, labels, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar(shrink=0.7)
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels)
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

if __name__ == '__main__':
    labels = ['verybad', 'bad', 'good', 'verygood']

    verybad_head = []
    bad_head = []
    good_head = []
    verygood_head = []

    N = 4900

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
    ))

    start_feature_generation_time = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        features = executor.map(sota.create_and_generate_features, questions)

    finished_feature_generation_time = time.time()

    print("Generating features took {} seconds.".format(
        finished_feature_generation_time - start_feature_generation_time
    ))

    start_fit_transform_time = time.time()

    vectorizer = DictVectorizer()

    X = vectorizer.fit_transform(features)

    print(X.shape)

    finished_fit_transform_time = time.time()

    print("Fit transform took {} seconds.".format(
        finished_fit_transform_time - start_fit_transform_time
    ))

    Y = np.array(['bad'] * (len(verybad_head)+len(bad_head)) + ['good'] * (len(good_head)+len(verygood_head)))

    print(Y.shape)

    start_splitting_time = time.time()

    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(
        X, Y, train_size=0.7, random_state=31, stratify=Y)

    finished_splitting_time = time.time()

    print("Cross Validation splitting took {} seconds.".format(
        finished_splitting_time - start_splitting_time
    ))

    start_normalising_time = time.time()

    #X = preprocessing.maxabs_scale(X)
    #scaler = preprocessing.MaxAbsScaler()
    #scaler = preprocessing.MinMaxScaler()
    #X_train = scaler.fit_transform(X_train.todense())
    #X_test = scaler.transform(X_test.todense())

    finished_normalising_time = time.time()

    print("Normalising took {} seconds.".format(
        finished_normalising_time - start_normalising_time
    ))

    start_model_training_time = time.time()

    '''
    clf = RandomForestClassifier(
        n_estimators=100, n_jobs=6, oob_score=True, random_state=50,
        max_features="auto", min_samples_leaf=50
    )
    '''

    clf = RandomForestClassifier(
        n_estimators=1000, n_jobs=6, oob_score=True, random_state=50#, max_depth=7
    )

    '''
    cv = StratifiedKFold(Y)

    score, permutation_scores, pvalue = permutation_test_score(
        clf, X, Y, scoring="accuracy", cv=cv, n_permutations=50, n_jobs=3
    )

    print("Classification score %s (pvalue : %s)" % (score, pvalue))

    print(permutation_scores)
    '''

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

    report = classification_report(Y_test, predicted, target_names=labels)

    finished_scoring_time = time.time()

    print("Model Scoring took {} seconds.".format(
        finished_scoring_time - start_scoring_time
    ))

    print(report)

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    feature_names = np.array([html.escape(w) for w in vectorizer.get_feature_names()])

    '''
    for i, rf_tree in enumerate(clf.estimators_):
        dot_data = StringIO()
        export_graphviz(
            rf_tree,
            dot_data,
            feature_names=feature_names,
            class_names=labels
        )
        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        graph.set_bgcolor('transparent')
        graph.write_png('./visualized_trees/' + 'tree_' + str(i) + '.png')
    '''

    # Print the feature ranking
    print("Feature ranking:")
    for f in range(X.shape[1])[:100]:
        print("%d. %s (%f)" % (f + 1, feature_names[indices[f]], importances[indices[f]]))

    matplotlib.rcParams.update({'font.size': 32})

    # Compute confusion matrix
    cm = confusion_matrix(Y_test, predicted)
    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization')
    print(cm)
    plt.figure(figsize=(16, 16))
    plot_confusion_matrix(cm, labels)
    plt.savefig('graphs/questions_confusion_matrix.png', dpi=100, transparent=True, bbox_inches='tight')

    # Normalize the confusion matrix by row (i.e by the number of samples
    # in each class)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print('Normalized confusion matrix')
    print(cm_normalized)
    plt.figure(figsize=(16, 16))
    plot_confusion_matrix(
        cm_normalized, labels, title='Normalized confusion matrix'
    )
    plt.savefig('graphs/questions_confusion_matrix_normalized.png', dpi=100, transparent=True, bbox_inches='tight')

    top_importances = (importances[indices])[:40]
    top_names = (feature_names[indices])[:40]

    # Plot the feature importances of the forest
    plt.figure(figsize=(24, 20))
    plt.title("Feature Importances")
    plt.barh(range(len(top_importances)), top_importances,
           color='#539DCC', ecolor='r', align="center") # xerr=std[indices],
    plt.yticks(range(len(top_importances)), top_names)
    plt.ylim([-1, len(top_importances)])
    plt.gca().invert_yaxis()
    plt.savefig('graphs/questions_feature_importances.png', dpi=100, transparent=True)

    plt.show()
