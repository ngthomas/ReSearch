#!/usr/bin/env python

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
            gi = search.GScholarItem(a['title'], a['id'], abstract=a['abstract'], relevance=a['relevance'])
            article_lst.append(gi)
        #
    return Request(jd['id'], keyword_lst, article_lst)



"""
"""
def handle_request(req, fn, fn_bin="keyw_d.bin", fn_geo_txt="geo_pmids_unique.txt", fn_geo_bin="geo.bin"):
    # read GEO pubmed ids and filter/boost keywords based on that
    geo_pmids = set()
    try:
        geo_pmids = pickle.load(open(fn_geo_bin, "rb"))
    except:
        with open(fn_geo_txt, 'r') as in_f:
            for ln in in_f:
                ln = ln.strip()
                geo_pmids.add(ln)
        # save it
        pickle.dump(geo_pmids, open(fn_geo_bin, "wb"))
    #
    print len(geo_pmids)
    print list(geo_pmids)[0:4]

    # read keywords in
    keyw_d = []
    try:
        keyw_d = pickle.load(open(fn_bin, "rb"))
    except:
        pass
    
    for a in req.articles:
        print a.title
        pmidl = search.search_pubmed(a)
        print pmidl
        # use google scholar abstract by default
        abstract = a.abstract
        if len(pmidl) > 0:
            relev = float(a.relevance)
            p = pmidl[0]
            if p in geo_pmids and relev > 0:
                print "in_geo!"
                relev *= 1.5
            pm = search.get_pubmed(p)
            abstract = pm.abstract
        pprint(abstract)
        ann_lst = search.annotate(abstract)
        print ann_lst
        for t in ann_lst:
            if t not in keyw_d:
                keyw_d[t] = 0.0
            keyw_d[t] += float(relev)
            
    # write keywords out
    pickle.dump(keyw_d, open(fn_bin, "wb"))

    # write json w/ top keywords
    sort_items = sorted(keyw_d.items(), key=operator.itemgetter(1), reverse=True)
    sort_keys = [k[0] for k in sort_items]
    #
    print [(k, keyw_d[k]) for k in sort_keys]
    #
    with open(fn, 'w') as of:
        json.dump(sort_keys[1:10], of)
    
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
