import json
from pprint import pprint
import search


class Request:
    def __init__(self, 


"""
Read JSON input data
"""
def read_json(fn):
    jf = open(fn)
    jd = json.load(jf)
    


"""
"""
def handle_requests(fn):
    
