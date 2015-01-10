
from Bio import Entrez
Entrez.email = 'A.N.Other@example.com'
import requests


class GScholarItem:
    def __init__(self, title, authors="", abstract=""):
        self.title = title
        self.authors = authors.split()
        self.abstract = abstract


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
    handle = Entrez.esearch(db="pubmed", term=gs_item.title, field="Title")
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
"""
def annotate(text):
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


def main():
    test_1()


if __name__ == "__main__":
    main()
