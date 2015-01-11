#!/usr/bin/env python

from Bio import Entrez
Entrez.email = 'A.N.Other@example.com'
import requests
import urllib


"""
Parse text from Google Scholar data
"""
class GScholarItem:
    def __init__(self, title, iid=0, authors="", abstract="", relevance=0):
        self.title = title
        self.iid = iid
        self.authors = authors.split()
        self.abstract = abstract
        self.relevance = relevance


"""
PubMed data for a publication
"""
class PubMedItem:
    def __init__(self, title, abstract, author_lst, affil_lst):
        self.title = title
        self.abstract = abstract
        self.author_lst = author_lst
        self.affil_lst = affil_lst


"""
Search Pubmed for publication, by title / authors
return pubmed id(s)
"""
def search_pubmed(gs_item):
    handle = Entrez.esearch(db="pubmed", term=gs_item.title, field="Title", retmax=2)
    record = Entrez.read(handle)
    pmids = record["IdList"]
    return pmids


"""
Retrieve Pubmed record (title, keywords, authors) for pubmed id
"""
def get_pubmed(pmid):
    # handle = Entrez.efetch(db='pubmed', id=pmid, retmode='text', rettype='abstract')
    #record = Entrez.read(handle)
    # return record
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    xml_data = Entrez.read(handle)[0]
    # article title
    title = xml_data["MedlineCitation"]['Article']['ArticleTitle']
    # article abstract
    abstract = xml_data['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
    # print abstract
    # article authors
    data_authors = xml_data["MedlineCitation"]['Article']['AuthorList']
    # print data_authors
    key = 'LastName'
    author_lst = [a[key] for a in data_authors if (key in a) and len(a[key]) > 0]

    # author affiliation
    aff_lst = []
    for i in range(len(data_authors)):
        aff_info = xml_data["MedlineCitation"]['Article']['AuthorList'][i]['AffiliationInfo']
        if len(aff_info) > 0:
            aff_lst.append(aff_info[0]['Affiliation'])
    #
    # print "{0} {1} {2}".format(abstract, ",".join(author_lst), ",".join(aff_lst))
    return PubMedItem(title, abstract, author_lst, aff_lst)



"""
Retrieve list of PubMed ids with datasets in GEO
#
# The following method is broken - does not retrieve PubMed ids for a limited number of GEO ids,
# errors out > 10K results!
# http://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html#ExampleIV
#
# Now using esearch to get all GEO ids first,
# then post them in batches to a WebEnv on server,
# the use the WebEnv to run the PubMed id query for each batch.
# 
"""
def get_pubmed_for_geo():
    # first get all the datasets from GEO
    hnd_1 = Entrez.esearch(db="gds", term="(gse[ETYP] OR gds[ETYP])",
        retstart=0, retmax=100000, usehistory="y")
    rec_1 = Entrez.read(hnd_1)
    id_lst = rec_1["IdList"]
    pmid_set = set()
    # request data in batches
    step = 100
    # for i in range(0, 100, 10):
    for i in range(0, len(id_lst), step):
        # print i
        idl = id_lst[i : (i+step)]
        # print idl[0]
        # post the list to WebEnv
        hnd_2 = Entrez.epost(db="gds", id=",".join(idl))
        rec_2 = Entrez.read(hnd_2)
        key = rec_2['QueryKey']
        env = rec_2['WebEnv']
        # then retrieve the Pubmed ids
        # http://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=gds&db=pubmed&query_key=X&WebEnv=ENTER_WEBENV_PARAMETER_HERE
        hnd_3 = Entrez.elink(dbfrom="gds", db="pubmed", query_key=key, WebEnv=env)
        rec_3 = Entrez.read(hnd_3)
        #
        data = rec_3[0]['LinkSetDb'][0]['Link']
        pmidl = [ data[i]["Id"] for i in range(len(data)) ]
        print "\n".join(set(pmidl))
        pmid_set = pmid_set.union(pmidl)
    #
    return list(pmid_set)


"""
Recognize biomedical ontology terms in text
"""
def annotate(text):
    text = urllib.quote( text.encode('utf-8') )
    url = "http://data.bioontology.org/annotator?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb&text={0}".format(text)
    r = requests.get(url)
    js = r.json()
    ann_lst = []
    for i in range(len(js)):
        ann = js[i].get("annotations")[0]["text"]
        ann_lst.append(ann.strip())
    return list(set(ann_lst))




def test_1():
    gs_item = GScholarItem("Cancer phenotype correlates with constitutional TP53 genotype")
    print ""
    print "Google Scholar paper title: '{0}'\n".format(gs_item.title)
    pm_ids = search_pubmed(gs_item)
    pmid = pm_ids[0]
    print "PubMed id: '{0}'\n".format(pmid)
    pm_rec = get_pubmed(pmid)
    print "PubMed record: '{0}, {1}, {2}, {3}'\n".format(pm_rec.title, pm_rec.abstract, pm_rec.author_lst, pm_rec.affil_lst)
    ann_lst = annotate(pm_rec.abstract)
    print "Annotated terms: '{0}'\n".format(", ".join(ann_lst))


def test_2():
    #
    pml = get_pubmed_for_geo()
    pml = sorted(pml)
    # print "\n".join(pml)


def main():
    test_2()


if __name__ == "__main__":
    main()
