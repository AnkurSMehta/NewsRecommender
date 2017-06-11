import sys
from collections import defaultdict

def gen_recommendations(file_to_process):
    """
    This function will read output from Hadoop which will
    be in following format
    source, dest, similarity_score
    
    as an output it will generate a pickle file
    """
    results = defaultdict(lambda: defaultdict(float))
    
    with open(file_to_process) as feed:
        for row in feed.readlines():
            source, candidate, score = row.strip().split("\t")
            score = float(score)
            results[source][candidate] = score
    return results

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print "Please specify input directory"
        sys.exit(-1)
    else:
        file_to_process = sys.argv[1]
        results = gen_recommendations(file_to_process)
        print "Total Unique:%d" % len(results)
        for source in results:
            print source
            sorted_scores = sorted(results[source].items(), key=lambda value: value[1], reverse=True)
            for candidate, score in sorted_scores:
                print "\t%s\t%s" % (candidate, score)
