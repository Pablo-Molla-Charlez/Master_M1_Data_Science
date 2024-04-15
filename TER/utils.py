import re
import os
from tqdm import tqdm
import json
import pandas as pd


def get_citation_mapping(mapping_file):
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)
    for k, v in mapping.items():
        mapping[k] = [p["cited_id"] for p in v]
    return mapping


def get_doc_index(doc, corpus):
    return corpus.index(doc)


def load_corpus(corpus_path, text_type):
    # load json file
    with open(corpus_path, 'r') as f:
        corpus = json.load(f)
        print(f"Loaded {len(corpus)} {text_type} from {corpus_path}")

    app_ids = [doc['Application_Number']+doc['Application_Category'] for doc in corpus]

    cnt = 0 # count the number of documents without text
    texts = []  # list of texts
    ids_to_remove = []  # list of ids of documents without text, to remove them from the corpus

    if text_type == 'title':
        for doc in corpus:
            try:
                texts.append(doc['Content']['title'])
            except: # if the document does not have a title
                ids_to_remove.append(doc['Application_Number']+doc['Application_Category'])
                cnt += 1
        print(f"Number of documents without title: {cnt}")

    elif text_type == 'abstract':
        for doc in corpus:
            try:
                texts.append(doc['Content']['pa01'])
            except: # if the document does not have an abstract
                ids_to_remove.append(doc['Application_Number']+doc['Application_Category'])
                cnt += 1
        print(f"Number of documents without abstract: {cnt}")

    elif text_type == 'claim1':
        for doc in corpus:
            try:
                texts.append(doc['Content']['c-en-0001'])
            except: # if the document does not have claim 1
                ids_to_remove.append(doc['Application_Number']+doc['Application_Category'])
                cnt += 1
        print(f"Number of documents without claim 1: {cnt}")

    elif text_type == 'claims':
        # all the values with the key starting with 'c-en-', each element in the final list is a list of claims
        for doc in corpus:
            doc_claims = []
            for key in doc['Content'].keys():
                if key.startswith('c-en-'):
                    doc_claims.append(doc['Content'][key])
            if len(doc_claims) == 0:    # if the document does not have any claims
                ids_to_remove.append(doc['Application_Number']+doc['Application_Category'])
                cnt += 1
            else:
                texts.append(doc_claims)
        print(f"Number of documents without claims: {cnt}")

    elif text_type == 'description':
        # all the values with the key starting with 'p'
        for doc in corpus:
            doc_text = []
            for key in doc['Content'].keys():
                if key.startswith('p'):
                    doc_text.append(doc['Content'][key])
            if len(doc_text) == 0:  # if the document does not have any description
                ids_to_remove.append(doc['Application_Number']+doc['Application_Category'])
                cnt += 1
            else:
                texts.append(doc_text)
        print(f"Number of documents without description: {cnt}")

    elif text_type == 'fulltext':
        for doc in corpus:
            doc_text = list(doc['Content'].values())
            texts.append(doc_text)
        if cnt > 0:
            print(f"Number of documents without any text: {cnt}")

    else:
        raise ValueError("Invalid text type")

    if len(ids_to_remove) > 0:
        print(f"Removing {len(ids_to_remove)} documents without required text")
        for id_ in ids_to_remove[::-1]:
            idx = app_ids.index(id_)
            del app_ids[idx]

    return texts, app_ids


def read_index(index_file):
    # Load the input json file
    with open(index_file, 'r') as json_file:
        data = json.load(json_file)
    print(f"Loaded {len(data)} documents from {index_file}")

    data_accumulator = []
    for doc in data:
        for content_type, content in doc['Content'].items():
            # Create a dictionary for each row and append it to the list
            row_data = {
                'app_id': doc['Application_Number'] + doc['Application_Category'],
                'content_type': content_type, 
            }
            data_accumulator.append(row_data)

    # Create the DataFrame from the accumulated data list only once
    df = pd.DataFrame(data_accumulator, columns=['app_id', 'date', 'content_type'])
    return df