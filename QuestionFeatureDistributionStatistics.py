import csv
import numpy as np
import StackOverflowTextAnalysis as sota
from itertools import islice
import time
import concurrent.futures

np.set_printoptions(precision=4)

if __name__ == '__main__':
    labels = ['verybad', 'bad', 'good', 'verygood']

    verybad = []
    bad = []
    good = []
    verygood = []

    N = 5000

    start_time = time.time()

    with open('data/questions-verybad.csv') as verybad_file:
        verybad = islice(csv.DictReader(verybad_file), N)
        verybad = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in verybad
        ]

    with open('data/questions-bad.csv') as bad_file:
        bad = islice(csv.DictReader(bad_file), N)
        bad = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in bad
        ]

    with open('data/questions-good.csv') as good_file:
        good = islice(csv.DictReader(good_file), N)
        good = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in good
        ]

    with open('data/questions-verygood.csv') as verygood_file:
        verygood = islice(csv.DictReader(verygood_file), N)
        verygood = [
            {
                'body': row['body'],
                'title': row['title']
            }
            for row in verygood
        ]

    finished_loading_time = time.time()

    print("Loading data took {} seconds.".format(
        finished_loading_time - start_time
    ))

    start_feature_generation_time = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
        verygood_features = executor.map(sota.create_and_generate_features, verygood)
        good_features = executor.map(sota.create_and_generate_features, good)
        bad_features = executor.map(sota.create_and_generate_features, bad)
        verybad_features = executor.map(sota.create_and_generate_features, verybad)

    finished_feature_generation_time = time.time()

    print("Generating features took {} seconds.".format(
        finished_feature_generation_time - start_feature_generation_time
    ))

    verygood_features = list(verygood_features)
    good_features = list(good_features)
    bad_features = list(bad_features)
    verybad_features = list(verybad_features)

    keys = verygood_features[0].keys()

    vg_features = {}
    g_features = {}
    b_features = {}
    vb_features = {}

    start_stats_generation_time = time.time()

    for key in keys:
        vg_features[key] = [row[key] for row in verygood_features]
        g_features[key] = [row[key] for row in good_features]
        b_features[key] = [row[key] for row in bad_features]
        vb_features[key] = [row[key] for row in verybad_features]

    for key in sorted(keys, key=str.lower):
        vg_median = np.around(np.median(vg_features[key]), decimals=2)
        vg_mean = np.around(np.mean(vg_features[key]), decimals=2)
        vg_std = np.around(np.std(vg_features[key]), decimals=2)

        g_median = np.around(np.median(g_features[key]), decimals=2)
        g_mean = np.around(np.mean(g_features[key]), decimals=2)
        g_std = np.around(np.std(g_features[key]), decimals=2)

        b_median = np.around(np.median(b_features[key]), decimals=2)
        b_mean = np.around(np.mean(b_features[key]), decimals=2)
        b_std = np.around(np.std(b_features[key]), decimals=2)

        vb_median = np.around(np.median(vb_features[key]), decimals=2)
        vb_mean = np.around(np.mean(vb_features[key]), decimals=2)
        vb_std = np.around(np.std(vb_features[key]), decimals=2)

        print(key[5:].replace("_", " "), " & ",
            vg_median, " & ", vg_mean, " & ", vg_std, " & ",
            g_median, " & ", g_mean, " & ", g_std, " & ",
            b_median, " & ", b_mean, " & ", b_std, " & ",
            vb_median, " & ", vb_mean, " & ", vb_std, " \\\\ ",
        )

    finished_stats_generation_time = time.time()

    print("Generating statistics took {} seconds.".format(
        finished_stats_generation_time - start_stats_generation_time
    ))