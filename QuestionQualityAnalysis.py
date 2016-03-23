import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from sklearn.metrics import classification_report
import numpy as np
import StackOverflowTextAnalysis as sota
from itertools import islice
import time
import multiprocessing
import concurrent.futures

def create_and_generate_features(body):
    return sota.StackOverflowTextAnalysis(body).generate_features()

if __name__ == '__main__':
    verybad_head = []
    bad_head = []
    good_head = []
    verygood_head = []

    N = 2000

    start_time = time.time()

    with open('data/questions-verybad.csv') as verybad_file:
        verybad = islice(csv.DictReader(verybad_file), N)
        verybad_head = [row['body'] for row in verybad]

    with open('data/questions-bad.csv') as bad_file:
        bad = islice(csv.DictReader(bad_file), N)
        bad_head = [row['body'] for row in bad]

    with open('data/questions-good.csv') as good_file:
        good = islice(csv.DictReader(good_file), N)
        good_head = [row['body'] for row in good]

    with open('data/questions-verygood.csv') as verygood_file:
        verygood = islice(csv.DictReader(verygood_file), N)
        verygood_head = [row['body'] for row in verygood]

    bodies = verybad_head + bad_head + good_head + verygood_head

    finished_loading_time = time.time()

    print("Loading data took {} seconds.".format(
        finished_loading_time - start_time
        )
    )

    start_feature_generation_time = time.time()

    p = multiprocessing.Pool()

    # features = [
    #     sota.StackOverflowTextAnalysis(body).generate_features() for body in bodies
    # ]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        features = executor.map(create_and_generate_features, bodies)

    finished_feature_generation_time = time.time()

    print("Generating features took {} seconds.".format(
        finished_feature_generation_time - start_feature_generation_time
        )
    )

    start_fit_transform_time = time.time()

    # tf = TfidfVectorizer()
    # X = tf.fit_transform(qe_head+qu_head)

    vectorizer = DictVectorizer()

    X = vectorizer.fit_transform(features)

    finished_fit_transform_time = time.time()

    print("Fit transform took {} seconds.".format(
        finished_fit_transform_time - start_fit_transform_time
        )
    )

    start_normalising_time = time.time()

    X = preprocessing.maxabs_scale(X)

    finished_normalising_time = time.time()

    print("Normalising took {} seconds.".format(
        finished_normalising_time - start_normalising_time
        )
    )

    Y = ['verybad'] * len(verybad_head) + ['bad'] * len(bad_head) + \
        ['good'] * len(good_head) + ['verygood'] * len(verygood_head)

    # print(X.shape)

    start_splitting_time = time.time()

    X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(
        X, Y, train_size=0.7, random_state=31)

    finished_splitting_time = time.time()

    print("Cross Validation splitting took {} seconds.".format(
        finished_splitting_time - start_splitting_time
        )
    )

    start_model_training_time = time.time()

    clf = RandomForestClassifier(n_estimators=10000, n_jobs=6)
    clf = clf.fit(X_train, Y_train)

    finished_model_training_time = time.time()

    print("Model Training took {} seconds.".format(
        finished_model_training_time - start_model_training_time
        )
    )

    start_predicting_time = time.time()

    predicted = clf.predict(X_test)

    finished_predicting_time = time.time()

    print("Predicting took {} seconds.".format(
        finished_predicting_time - start_predicting_time
        )
    )

    start_scoring_time = time.time()

    # score = clf.score(X_test, Y_test)
    report = classification_report(Y_test, predicted)

    finished_scoring_time = time.time()

    print("Model Scoring took {} seconds.".format(
        finished_scoring_time - start_scoring_time
        )
    )

    # print("Score =", score)

    print(report)
