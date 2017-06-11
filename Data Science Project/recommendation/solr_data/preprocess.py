import os
import re
import sys
import json
from collections import defaultdict

stoplist = set([stopword.strip() for stopword in open("stoplist.txt")])
BASE_DIR = "solr_data"

def solr2txt(file_name):
    """
    This method is to convert json file from solr
    in text files
    """
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)

    data = json.loads(open(file_name).read())
    for doc in data['response']['docs']:
        site_name = doc['source']
        title = doc['title']
        doc_id = doc['id']
        crawled_date = doc['crawled_date']

        if 'details' not in doc:
            continue

        details = doc['details']

        dir_to_save = os.path.join(BASE_DIR, site_name)

        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)

        file_to_save = os.path.join(dir_to_save, doc_id)
        file_to_save += ".txt"

        with open(file_to_save, "w") as output:
            output.write(crawled_date + "\n")
            output.write(title + "\n")
            output.write(details)

        print "Done Saving: %s, %s" % (site_name, doc_id)

def word_count(file_name):
    """
    Given a file_name compute word counts
    """
    result = defaultdict(int)
    word_re = re.compile(r'\w+', re.IGNORECASE)
    for line in open(file_name).readlines():
        line = line.lower()
        for token in word_re.findall(line):
            if token not in stoplist:
                result[token] += 1
    return result

def cleanup_files(dir_name):
    """
    This function is used to iterate over all 
    files in a given directory and get it to a
    form where it will be used later in the processing
    """
    result = []
    for current_file in os.listdir(dir_name):
        file_to_read = os.path.join(dir_name, current_file)
        features = word_count(file_to_read)
        result.append({file_to_read: features})
    return result


