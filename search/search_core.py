
from Bio import Entrez
Entrez.email = 'A.N.Other@example.com'
import requests
import scholar
import argparse
import json



"""
Parse text from Google Scholar data
"""
class GScholarItem:
    def __init__(self):
        self.attrs = {
            'Title':None,
            'URL': None,
            'Year':None, 
            'Author':None,
            'Citations':0,
            'Excerpt':None,
        }
    def add_attrs(self, feature, value):
        self.attrs[feature] = value

'''
Creates an array of Google Scholar Items given query search
'''

def make_GScholarItems(query_search):

    GScholarItems = []
    parseField = scholar.get_scholar(query_search)

    for line in parseField:
        items=line.split("\n")
        article=GScholarItem()
        for item in items: 
            sep = item.split("----")
            article.attrs[sep[0]]=sep[1]
        GScholarItems.append(article)
    return GScholarItems


def PrintInJson(scholar_obj):

   newList = list()
   for article in scholar_obj:
         newList.append(article.attrs)
   print newList

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-q','--query', default=None,type=str,help='query search')
    parser.add_argument('-r','--rating',default=1,type=str, help='')
    opts = parser.parse_args()

    GScholarItems = make_GScholarItems(opts.query)
    PrintInJson(GScholarItems)
    #opts.query  ## need regular expression s/AND/+/g s/NOT/-/g 

