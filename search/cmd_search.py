#!/usr/bin/env python

from collections import defaultdict, OrderedDict
import pickle
import operator
import json
from pprint import pprint

import search


class Request:
    def __init__(self, rid, keywords, articles):
        self.rid = rid
        self.keywords = keywords
        self.articles = articles


"""
Read JSON input data
"""
def read_json(fn):
    with open(fn) as jf:
        jd = json.load(jf)
        #
        keyword_lst = jd['keywords']
        #
        j_articles = jd['articles']
        article_lst = []
        for a in j_articles:
            gi = search.GScholarItem(a['title'], a['id'], relevance=a['relevance'])
            article_lst.append(gi)
        #
    return Request(jd['id'], keyword_lst, article_lst)



"""
"""
def handle_request(req, fn, fn_bin="keyw_d.bin"):
    # read GEO pubmed ids and filter/boost keywords based on that

    # read keywords in
    keyw_d = defaultdict(lambda: 0)
    try:
        keyw_d = pickle.load(open(fn_bin, "rb"))
    except:
        pass
    
    for a in req.articles:
        print a.title
        pmidl = search.search_pubmed(a)
        print pmidl
        if len(pmidl) > 0:
            p = pmidl[0]
            pm = search.get_pubmed(p)
            ann_lst = search.annotate(pm.abstract)
            print ann_lst
            for t in ann_lst:
                keyw_d[t] += int(a.relevance)
            
    # write keywords out
    sort_x = sorted(keyw_d.items(), key=operator.itemgetter(1), reverse=True)
    keyw_d = OrderedDict(sort_x)
    print keyw_d
    pickle.dump(keyw_d, open(fn_bin, "wb"))

    # write json w/ top keywords
    with open(fn, 'w') as of:
        json.dump(keyw_d.keys()[1:10], of)
    
    return keyw_d



def test_1():
    x = read_json("mock_data.txt")
    print x.articles[2].title
    

def test_2():
    x = handle_request(read_json("data_in.json"), "data_out.json")
    # print x


def main():
    test_2()


if __name__ == "__main__":
    main()
