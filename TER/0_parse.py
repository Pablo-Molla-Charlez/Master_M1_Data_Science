#]!/usr/bin/env python3

import re
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections
from elasticsearch import helpers
import xml.etree.ElementTree as ET




INDEX_APPL = "ep_patent_applications5"
INDEX_CIT = "ep_patent_citations5"


def gendata(records, index, type):
    for k, v in records.items():
        yield {
            "_index": index,
            "_id": k,
            "_source": v
        }



def extract_classifications(line):
    #words = line.split("\t")[6].split(" ")
    #indices = [i for i, x in enumerate(words) if "<classification-ipcr><text>" in x]
    #return [words[i][words[i].find("<classification-ipcr><text>")+27:words[i].find("<classification-ipcr><text>")+31] for i in indices]

    classifications_list = []
    start_classification = line.find("<classifications-ipcr>")
    #print(line[start_classification:])
    relative_end_classification = line[start_classification:].find("</classifications-ipcr>")+23
    classification_string = line[start_classification:start_classification+relative_end_classification]
    try:
        treeRoot = ET.fromstring(classification_string)
        for classifications in treeRoot.findall('classification-ipcr'):
            for classification in classifications:
              classifications_list.append(classification.text)
    except:
        print("error classification for line: " + classification_string)

    return classifications_list
    # try:
    #     treeRoot = ET.fromstring(classification_string)
    #     for classifications in treeRoot.findall('classification-ipcr'):
    #         for classification in classifications:
    #             classification_text = classification.text
    #             if classification_text.startswith("A"):
    #                 classifications_list.append(classification.text)
    #             elif classification_text.startswith("G"):
    #                 classifications_list.append(classification.text)
    # except:
    #     print("error classification for line: " + classification_string)
    # starting_letter = [classification[0] for classification in classifications_list]
    # if "A" in starting_letter and "G" in starting_letter:
    #     return classifications_list
    # else:
    #     return []


def from_citationIDs_to_application_number(line):
    pattern_patcit = re.compile('patcit dnum="[A-Z]{2}[A-Z\d]+"')
    result_patents = [elem[13:-1] for elem in pattern_patcit.findall(line)]
    return result_patents

def extract_citationIDs(application_identifier, line):
    words = line.split("\t")[7].split(" ")
    indices = [i for i, x in enumerate(words) if "sr-cit" in x]
    return [application_identifier + "_" + words[i][words[i].find("sr-cit")+6:words[i].find("sr-cit")+10] for i in indices]

def normalize_claims(claims):
    normalized_claims = []
    for claim in claims.split(","):
        if "-" not in claim:
            normalized_claims.append(int(claim))
        else:
            for number in range(int(claim.split("-")[0]),int(claim.split("-")[1])+1):
                normalized_claims.append(number)
    #print("Normalize_claims:", normalized_claims)
    return normalized_claims

def extract_citation_entry(citation_id, searchreport_line, application_number_and_category):
    # gibt vollen Eintrag fuer citation Tabelle zurueck
    #Finde Citation Abschnitt Start und relativ zum Start das Ende
    citation = {}
    start_citation = searchreport_line.find("<citation id=\"sr-cit"+citation_id[-4:]) #26
   # print(searchreport_line[start_citation:])
    relative_end_citation = searchreport_line[start_citation:].find("</citation>")+11
    citation_string = searchreport_line[start_citation:start_citation+relative_end_citation]

    try:
        treeRoot = ET.fromstring(citation_string)
    except:
        #print("error citation for line: "+citation_string)
        return citation

    treeRoot.findall('category')

    last_category = ""
    for element in treeRoot:
        #print(element, element.tag, element.attrib, element.text)
        if element.tag == "category":
            last_category =element.text
        elif element.tag == "rel-claims":
            for category in last_category.split(","):
                citation.update({"category"+"_"+category:normalize_claims(element.text)})
        elif element.tag == "rel-passage":
            for category in last_category.split(","):
                for passage in element:
                    old_rel_passage = citation.get("rel-passage"+ "_"+ category)
                    if old_rel_passage == None:
                        old_rel_passage=""
                    citation.update({"rel-passage"+"_"+category:old_rel_passage + passage.text})
        elif element.tag == "patcit":
            citation.update({"original_patent_id":application_number_and_category})
            citation.update({"dnum":element.attrib["dnum"]})
            citation.update({"url":element.attrib["url"]})
            for subelement in element:
                if subelement.tag == "document-id":
                    for child in subelement:
                        if child.tag == "country":
                            citation.update({"country":child.text})
                        elif child.tag == "doc-number":
                            citation.update({"doc-number":child.text})
                        elif child.tag == "kind":
                            citation.update({"kind":child.text})
                        elif child.tag == "name":
                          citation.update({"name":child.text})
                        elif child.tag == "date":
                          citation.update({"date":child.text})
        elif element.tag == "nplcit":
            citation.update({"nplcit": "true"})

    #logge, falls wir kategorie ohne related claim haben
    """if last_category != "" and "rel-passage"+"_"+last_category.split(",")[0] not in citation.keys():
        print("Kategorie ohne rel-passage, Citation ID/String: " + citation_id + " / " + citation_string)"""
    return citation

def main(file):
    f = open(file, "r", encoding="utf8", errors='ignore')
    lines = f.readlines()
    records = {}
    citations = {}
    pattern_en = re.compile("\t20(1[0-9]|20)-\d{2}-\d{2}\ten\t")
    flag_d = False
    flag_c = False
    flag_t = False
    flag_a = False
    flag_am = False
    flag_ams = False
    temp_record = {}
    for line in lines:
        if re.search(pattern_en, line):
            if "\tTITLE\t" in line:
                if flag_c:
                    flag_a = False
                    flag_d = False
                    flag_c = False
                    application_identifier = line.split("EP\t")[1].split("\ten\t")[0].replace("\t","")
                    application_title = line.split("\tTITLE\t")[1][2:] 
                    flag_t = True
                    temp_record = {}
                else:
                    application_identifier = line.split("EP\t")[1].split("\ten\t")[0].replace("\t","")
                    application_title = line.split("\tTITLE\t")[1][2:] 
                    flag_t = True
            if "\tABSTR\t" in line and flag_t:
                application_abstract = line.split("\tABSTR\t")[1]
                flag_a = True
            if "\tDESCR\t" in line and flag_t:
                application_number = line.split("EP\t")[1].split("\t")[0]
                application_category = line.split("EP\t")[1].split("\t")[1]
                application_date = line.split("EP\t")[1].split("\t")[2]
                if not flag_a:
                    temp_record = {
                        application_identifier : {
                            "application_number": application_number,
                            "application_category": application_category,
                            "application_date": application_date,
                            "title": application_title,
                            "description": line.split("\tDESCR\t")[1][7:]
                        }
                    }
                    flag_d = True
                    if application_date == "":
                        #print("Skipping entry, missing date: " + application_identifier)
                        continue
                elif flag_a:
                    temp_record = {
                        application_identifier : {
                            "application_number": application_number,
                            "application_category": application_category,
                            "application_date": application_date,
                            "title": application_title,
                            "abstract": application_abstract,
                            "description": line.split("\tDESCR\t")[1][7:]
                        }
                    }
                    flag_d = True
                    if application_date == "":
                        #print("Skipping entry, missing date: " + application_identifier)
                        continue
            if "\tCLAIM\t" in line and flag_d and application_identifier in temp_record:
                flag_c = True
                temp_record[application_identifier]["claims"] = line.split("\tCLAIM\t")[1][7:] 
            if "\tAMEND\t" in line and flag_c and application_identifier in temp_record:
                
                application_amend = line.split("\tAMEND\t")[1]
                temp_record[application_identifier]["amended_claims"] = application_amend
                #flag_am = True # need to reset
            if "\tACSTM\t" in line and application_identifier in temp_record:
                
                application_amended_statements = line.split("\tACSTM\t")[1]
                temp_record[application_identifier]["amended_claims_statements"] = application_amended_statements
                #flag_ams = True
            if  "\tSRPRT\t" in line and application_identifier in temp_record:
                # if extract_classifications(line):
                    # and extract_citationIDs(application_identifier, line):
                temp_record[application_identifier]["citation_ipcr_classification"] = extract_classifications(line)
                temp_record[application_identifier]["citation_ids"] = extract_citationIDs(application_identifier, line)
                temp_record[application_identifier]["citation_application_number"] = from_citationIDs_to_application_number(line)
                application_number_and_category = application_number + application_category
                for citation_id in temp_record[application_identifier]["citation_ids"]:
                    #print("evaluate citation id: "+citation_id)
                    citations[citation_id] = extract_citation_entry(citation_id, line.split("\tSRPRT\t")[1], application_number_and_category)
            if "\tPDFEP\t" in line and application_identifier in temp_record:
                application_url = line.split("\tPDFEP\t")[1]
                temp_record[application_identifier]["publication_url"] = application_url
            if  application_identifier in temp_record: # and "citation_ids"
                records.update(temp_record)

    print(f"File {file} finished")
    upload(records, INDEX_APPL, "patent_eu")
    upload(citations, INDEX_CIT, "citation_eu")



def createIndexPatentApplications():
    # Elasticsearch
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
                "properties": {
                    "application_number": {
                        "type": "keyword"
                    },
                    "application_category": {
                        "type": "keyword"
                    },
                    "application_date": {
                        "type": "date"
                    },
                    "title": {
                        "type": "text"
                    },
                    "abstract": {
                        "type": "text"
                    },
                    "description": {
                        "type": "text"
                    },
                    "claims": {
                        "type": "text"
                    },
                    "amended_claims": {
                        "type": "text"
                    },
                    "amended_claims_statements": {
                        "type": "text"
                    },
                    "citation_ipcr_classification": {
                        "type": "keyword"
                    },
                    "citation_ids": {
                        "type": "keyword"
                    },
                    "citation_application_number": {
                        "type": "keyword"
                    },
                    "publication_url": {
                        "type": "text"
                    }
                }
            }
        }


    es = Elasticsearch(hosts=['http://localhost:9200/'])
    response = es.indices.create(index=INDEX_APPL, ignore=400, body=settings)

    print(response)

def createIndexCitations():
    # Elasticsearch
    #https://www.epo.org/law-practice/legal-texts/html/guidelines/e/b_x_9_2.htm
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "index.mapping.ignore_malformed": True
        },
        "mappings": {
                "properties": {
                    "original_patent_id": {
                        "type": "keyword"
                    },
                    "dnum": {
                        "type": "keyword"
                    },
                    #"publication_url": {
                    #   "type": "text"
                    #},
                    "country": {
                        "type": "keyword"
                    },
                    "kind":{
                        "type": "keyword"
                    },
                    #"doc_number": {
                    #   "type": "keyword"
                    #},
                    "name": {
                        "type": "text"
                    },
                    "date": {
                        "type": "date"
                    },
                    "category_X": {
                        "type": "integer"
                    }
                    ,
                    "category_P": {
                        "type": "integer"
                    }
                    ,
                    "category_A": {
                        "type": "integer"
                    }
                    ,
                    "category_D": {
                        "type": "integer"
                    }
                    ,
                    "category_Y": {
                        "type": "integer"
                    }
                    ,
                    "category_L": {
                        "type": "integer"
                    }
                    ,
                    "category_O": {
                        "type": "integer"
                    }
                    ,
                    "category_T": {
                        "type": "integer"
                    }
                    ,
                    "category_E": {
                        "type": "integer"
                    },
                    "rel-passage_X": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_P": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_A": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_D": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_Y": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_L": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_O": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_T": {
                        "type": "text"
                    }
                    ,
                    "rel-passage_E": {
                        "type": "text"
                    }
                    ,
                    "nplcit" : {
                        "type": "boolean"
                    }
                }
            }
        }

    es = Elasticsearch(hosts=['http://localhost:9200/'])
    response = es.indices.create(index=INDEX_CIT, ignore=400, body=settings)

    print(response)

def upload(records, index, type):
    # Elasticsearch
    client = Elasticsearch(
        "http://localhost:9200/",
    )
    # client = connections.create_connection(hosts=['http://localhost:9200/'])
    client_with_options = client.options(request_timeout=200)
    res = helpers.bulk(client_with_options, gendata(records, index, type),index=index, chunk_size=1000)

    print(res)


if __name__ == '__main__':
    createIndexPatentApplications()
    createIndexCitations()
    # #"/san2/data/websci/usPatents/epo-gcp/EP0000000.txt","/san2/data/websci/usPatents/epo-gcp/EP0100000.txt","/san2/data/websci/usPatents/epo-gcp/EP0200000.txt","/san2/data/websci/usPatents/epo-gcp/EP0300000.txt","/san2/data/websci/usPatents/epo-gcp/EP0400000.txt","/san2/data/websci/usPatents/epo-gcp/EP0500000.txt","/san2/data/websci/usPatents/epo-gcp/EP0600000.txt","/san2/data/websci/usPatents/epo-gcp/EP0700000.txt","/san2/data/websci/usPatents/epo-gcp/EP0800000.txt","/san2/data/websci/usPatents/epo-gcp/EP0900000.txt","/san2/data/websci/usPatents/epo-gcp/EP1000000.txt", "/san2/data/websci/usPatents/epo-gcp/EP1100000.txt","/san2/data/websci/usPatents/epo-gcp/EP1200000.txt","/san2/data/websci/usPatents/epo-gcp/EP1300000.txt","/san2/data/websci/usPatents/epo-gcp/EP1400000.txt","/san2/data/websci/usPatents/epo-gcp/EP1500000.txt",
    files = [
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1000000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1100000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1200000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1300000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1400000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1500000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1600000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1700000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1800000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP1900000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2000000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2100000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2200000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2300000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2400000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2500000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2600000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2700000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2800000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP2900000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3000000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3100000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3200000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3300000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3400000.txt",
         "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3500000.txt",
        "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3600000.txt",
        "/bigstorage/ter/ep-fulltext-for-text-analytics/EP3700000.txt"
    ]
    # #files = ["/Users/nicolashoeck/Downloads/SampleData.txt"]
    for file in files:
        print("start file: "+file)
        main(file)



