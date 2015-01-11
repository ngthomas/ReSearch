
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
    jf = open(fn)
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
def handle_request(req_lst):
    for req in req_lst:
        
    return



"""
"""
def test_1():
    x = read_json("mock_data.txt")
    print x.articles[2].title
    


def main():
    test_1()


if __name__ == "__main__":
    main()
