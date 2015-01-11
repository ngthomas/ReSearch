from Bio import Entrez
Entrez.email = 'A.N.Other@example.com'
import requests
import urllib
from django.utils.encoding import smart_str
from unidecode import unidecode

"""
PubMed data for a publication
"""
class PubMedItem:
    def __init__(self, title, abstract, journal, authors, affil_lst, year, url):
        self.title = title
        self.abstract = abstract
        self.journal = journal
        self.authors = authors
        self.affil_lst = affil_lst
        self.year = year
        self.url = url


"""
Search Pubmed for publication, by title / authors
return pubmed id(s)
"""
def search_pubmed(query):
    query = ' OR '.join(query.split(' '))
    handle = Entrez.esearch(db="pubmed", term=query, retmax=10)
    record = Entrez.read(handle)
    pmids = record["IdList"]
    return pmids


"""
Retrieve Pubmed records (title, keywords, authors) for pubmed ids
"""
def get_pubmed(pmids):
    # handle = Entrez.efetch(db='pubmed', id=pmid, retmode='text', rettype='abstract')
    #record = Entrez.read(handle)
    # return record
    handle = Entrez.efetch(db='pubmed', id=pmids, retmode='xml')
    records = []
    for pmid, paper_xml in zip(pmids, Entrez.read(handle)):
        try:
            title = paper_xml["MedlineCitation"]['Article']['ArticleTitle']
        except:
            continue
        try:
            abstract = paper_xml['MedlineCitation']['Article']['Abstract']['AbstractText'][0].replace('"', "'")
        except:
            abstract = 'Abstract is missing.'
        try:
            author_data = paper_xml["MedlineCitation"]['Article']['AuthorList']
            authors = []
            for entry in author_data:
                author = ''
                if 'ForeName' in entry and len(entry['ForeName']) > 0:
                    author = entry['ForeName']
                elif 'Initials' in entry and len(entry['Initials']) > 0:
                    author += ' ' + entry['Initials']
                if 'LastName' in entry and len(entry['LastName']) > 0:
                    author += ' ' + entry['LastName']
                authors.append(author)
        except:
            authors = ['Author data missing']
        
        year = paper_xml["MedlineCitation"]['Article']['Journal']['JournalIssue']['PubDate']['Year']
        url = 'http://www.ncbi.nlm.nih.gov/pubmed/' + pmid
         # author affiliation
        aff_lst = []
        for i in range(len(author_data)):
            aff_info = paper_xml["MedlineCitation"]['Article']['AuthorList'][i]['AffiliationInfo']
            if len(aff_info) > 0:
                aff_lst.append(aff_info[0]['Affiliation'])

        journal = paper_xml['MedlineCitation']['Article']['Journal']['Title']
        records.append(PubMedItem(title, abstract, journal, authors, aff_lst, year, url))
    return records

def convertRecordsToJSON(records):
    xml_record_list = []
    for record in records:
        xml_record = '{"Author":"' + ', '.join(record.authors) + '", "URL": "' + record.url + '", "Journal": "' + record.journal + '", "Title": "' + record.title + '", "Excerpt": "' + record.abstract + '", "Year": "' + record.year +'"}'
        xml_record = smart_str(xml_record)
        xml_record_list.append(xml_record)
    return '{"articles": [' + ', '.join(xml_record_list) + ']}'

def get_json_from_pubmed(query):
    return convertRecordsToJSON(get_pubmed(search_pubmed(query)))
