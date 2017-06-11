import os
import sys
import pickle
import operator
from preprocess import cleanup_files

N = 10
MIN_THRESHOLD = 0.25
IGNORE_EXTENSIONS = ['txt', 'py', 'py~', 'pkl', 'pyc']

# This is set which implies we want to generate files 
MAPR_MODE = True

if MAPR_MODE:
    file_to_save = open("input.txt", "w")

def build_dataset(base_dir):
    """
    This method is used to build a dataset given list of
    stories
    """
    final_dataset = []

    for current in os.listdir(base_dir):
        if len(current.split(".")) > 0 and current.split(".")[-1] not in IGNORE_EXTENSIONS:
            final_dataset += cleanup_files(os.path.join(base_dir, current))
            print "Completed Processing:%s" % current
    return final_dataset


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


def gen_recommendations(dataset):
    """
    This function outputs actual recommendations
    """
    for i in dataset:
        scores = {}
        for j in dataset:
            if i != j:
                a, b = i.keys()[0], j.keys()[0]
                
                if MAPR_MODE:
                    row = "%s\t%s\n" % (a, b)
                    file_to_save.write(row)
                    continue

                if b not in scores:
                    sim_score = jaccard(i.values()[0], j.values()[0])
                    scores[b] = sim_score
        row = "%s" % i.keys()[0]
        sorted_scores = sorted(scores.items(), key=lambda value: value[1], reverse=True)

        i = 0
        result = {}
        result[row] = []
        for candidate, sim_score in sorted_scores:
            if sim_score > MIN_THRESHOLD:
                result[row].append((candidate, sim_score))
                i += 1

            if i >= N:
                break

        if len(result[row]) > 0:
            print result

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print "Please specify input directory"
        sys.exit(-1)
    else:
        base_dir = sys.argv[1]
        features = build_dataset(base_dir)
        pickle.dump(features, open("features.pkl", "wb"))
        print "Genereated features pickle file" 
        gen_recommendations(features)
        
        if MAPR_MODE:
            print "Generate input for MapReduce"
