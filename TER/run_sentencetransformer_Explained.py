# Requirements
import sys
import argparse
import json
import os
import numpy as np
import torch
import sentence_transformers
from sentence_transformers import SentenceTransformer, util
import time
from utils import *



def main():
    parser = argparse.ArgumentParser(description='Rank documents using BM25')
    parser.add_argument('--corpus', type=str, help='Path to the corpus file', nargs='+', default=['./DATASETS_JSON/Content_JSONs/Cited_2020_Uncited_2010-2019_Cleaned_Content_22k/CLEANED_CONTENT_DATASET_cited_patents_by_2020_uncited_2010-2019.json'])
    parser.add_argument('--queries', type=str, help='Path to the queries file', default='./DATASETS_JSON/Content_JSONs/Citing_2020_Cleaned_Content_12k/CLEANED_CONTENT_DATASET_citing_patents_2020.json')
    parser.add_argument('--model_name', type=str, default='AI-Growth-Lab/PatentSBERTa', help='Name of the model to use', required=False)
    parser.add_argument('--embedding_file', type=str, default='/bigstorage/you/rag_project/embeddings_precalculated/embeddings_PatentSBERTa_mean.npy', help='Name of the file to save the embeddings to', required=False)
    parser.add_argument('--n', type=int, default=100, help='Number of documents to return', required=False)
    parser.add_argument('--query_type', choices=['title', 'abstract', 'claim1', 'claims', 'description', 'fulltext'], default='abstract', help='Type of patent text of the query')
    parser.add_argument('--rerank', action='store_true', help='Whether to rerank the top n documents using cross-encoder')
    parser.add_argument('--output_dir', type=str, help='Path to the output directory', default='./results')
    args = parser.parse_args()


    # Load corpus
    corpus, app_ids = [], []
    for corpus_path in args.corpus:
        corpus_, app_ids_ = load_corpus(corpus_path, args.query_type)
        corpus.extend(corpus_)
        app_ids.extend(app_ids_)
    print(f"Loaded {len(corpus)} documents from {args.corpus}")

    # Load queries
    queries, query_ids = load_corpus(args.queries, args.query_type)
    print(f"Loaded {len(queries)} queries from {args.queries}")



    # load the model
    model = SentenceTransformer(args.model_name)

    # load the cross-encoder for reranking
    if args.rerank:
        from sentence_transformers import CrossEncoder
        cross_encoder = CrossEncoder(args.model_name)

    # if the embeddings are precomputed
    if args.embedding_file:
        # load the embeddings
        all_corpus_embeddings = torch.from_numpy(np.load(args.embedding_file))
        print(f"Loaded {all_corpus_embeddings.shape[0]} embeddings from {args.embedding_file}")

        # create empty dataframe to store the index
        index_df = pd.DataFrame(columns=['app_id', 'content_type'])
        for corpus_path in args.corpus:
            index_df = index_df._append(read_index(corpus_path), ignore_index=True)

        if args.query_type == "title":
            target_index = index_df[index_df['content_type'] == 'title'].index
        elif args.query_type == "abstract":
            target_index = index_df[index_df['content_type'] == 'pa01'].index
        elif args.query_type == "claim1":
            target_index = index_df[index_df['content_type'] == 'c-en-0001'].index
        elif args.query_type == "claims":
            target_index = index_df[index_df['content_type'].str.startswith('c-en-')].index
        elif args.query_type == "description":
            target_index = index_df[index_df['content_type'].str.startswith('p')].index
        elif args.query_type == "fulltext":
            target_index = index_df.index
        corpus_embeddings = all_corpus_embeddings[target_index]

    else:
        # encode the corpus and the queries
        if args.query_type in ['claims', 'description', 'fulltext']:   # types of queries that are lists of sentences
            # encode each sentence separately and average the embeddings
            corpus_embeddings = torch.zeros(len(corpus), model.get_sentence_embedding_dimension())
            for i, doc in tqdm(enumerate(corpus), total=len(corpus), desc="Encoding corpus"):
                doc_sentences_embeddings = model.encode(doc, convert_to_tensor=True, show_progress_bar=False, batch_size=64)
                corpus_embeddings[i] = doc_sentences_embeddings.mean(axis=0)
        else:
            corpus_embeddings = model.encode(corpus, convert_to_tensor=True, show_progress_bar=True, batch_size=64)
    corpus_embeddings = corpus_embeddings.to('cuda')


    # encode the queries
    if args.query_type in ['claims', 'description', 'fulltext']:
        query_embeddings = torch.zeros(len(queries), model.get_sentence_embedding_dimension())
        for j, query_sents in tqdm(enumerate(queries), total=len(queries), desc="Encoding queries"):
            query_sents_embeddings = model.encode(query_sents, convert_to_tensor=True, show_progress_bar=False, batch_size=64)
            query_embeddings[j] = query_sents_embeddings.mean(axis=0)
    else:
        query_embeddings = model.encode(queries, convert_to_tensor=True, show_progress_bar=True, batch_size=64)
    query_embeddings = query_embeddings.to('cuda')
    

    results = {}

    for query_text, query_embedding, query_id in tqdm(zip(queries, query_embeddings, query_ids), total=len(queries)):
        # compute the cosine similarity
        query_embedding = query_embedding.unsqueeze(0)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0].cpu()

        # Sort the results in decreasing order and get the first n results
        top_n_index = np.argsort(-cos_scores).numpy()[:args.n]

        if args.rerank:
            # rerank the top n documents using cross-encoder with the same model
            top_n_docs = [corpus[i] for i in top_n_index]
            
            # create pairs of query and document
            pairs = [[query_text, doc] for doc in top_n_docs]

            # rerank the top n documents
            rerank_scores = cross_encoder.predict(pairs, show_progress_bar=False, batch_size=64)
            top_n_index = np.argsort(-rerank_scores)[:args.n]

        # Get the pub_ids of the top n documents
        top_n_pub_ids = [app_ids[i] for i in top_n_index]
        results[query_id] = top_n_pub_ids


    # save results in a file
    with open("/bigstorage/Pablo_TER/test.json", 'w') as f:
        json.dump(results, f)
        #'./{args.output_dir}/{args.model_name.split("/")[-1]}_{args.query_type}_results_{"rerank" if args.rerank else "no_rerank"}


if __name__ == "__main__":
    start_time = time.time()  # Start timing
    
    main()  # Execute the main function
    
    end_time = time.time()  # End timing
    execution_time = end_time - start_time  # Calculate the elapsed time
    
    print(f"The main function took {execution_time} seconds to execute.")
