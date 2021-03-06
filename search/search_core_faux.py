#!/usr/bin/python
from Bio import Entrez
Entrez.email = 'A.N.Other@example.com'
import requests
import scholar
import argparse
import json
import search
import urllib2


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
            'Journal':None,
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
            if sep[0] in article.attrs:
                article.attrs[sep[0]]=sep[1]
        GScholarItems.append(article)
    return GScholarItems


'''
This module prints out the list of google scholar literature in Json Format
'''
def PrintInJson():
  
   JsFile = open("/home/ec2-user/reSearch/search/p80.j",'r')
   for line in JsFile.read().splitlines():
       print line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-q','--query', default=None,type=str,help='query search', required=True)
    parser.add_argument('-r','--rating',default=1,type=str, help='Collect user"s rating', required=False)


    #opts = parser.parse_args()

    #GScholarItems = make_GScholarItems(opts.query)
    PrintInJson()
    #opts.query  ## need regular expression s/AND/+/g s/NOT/-/g 

