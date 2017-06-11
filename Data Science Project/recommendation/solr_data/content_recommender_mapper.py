#!/usr/bin/python
import sys
import pickle

MIN_THRESHOLD = 0.25

def jaccard(wc_1, wc_2):
    """
    This function is used to compute similarity between two
    dictionary of word counts
    """
    set_wc_1 = set(wc_1.keys())
    set_wc_2 = set(wc_2.keys())

    if len(set_wc_1.intersection(set_wc_2)) == 0:
        return float(0)
    else:
        return (len(set_wc_1.intersection(set_wc_2)) / float(len(set_wc_1.union(set_wc_2))))

features = pickle.load(open("features.pkl", "rb"))
all_features = {}

for x in features:
    k, v = x.keys()[0], x.values()[0]
    all_features[k] = v

for line in sys.stdin:
    try:
        a, b = line.strip().split("\t")
        features_a, features_b = all_features[a], all_features[b]
        sim_score = jaccard(features_a, features_b)
        if sim_score > MIN_THRESHOLD:
            print "%s\t%s\t%f" % (a, b, sim_score)
    except:
        continue

        
