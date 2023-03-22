import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import pinecone
from tqdm.auto import tqdm
from pprint import pprint

def setup():
    df = pd.read_feather("wiki-data-feather")
    device = torch.cuda.current_device() if torch.cuda.is_available() else None
    model_id = "dslim/bert-base-NER"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForTokenClassification.from_pretrained(model_id)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="max", device=device)
    retriever = SentenceTransformer('flax-sentence-embeddings/all_datasets_v3_mpnet-base', device=device)
    pinecone.init(api_key="a0f2860f-74e5-4765-a635-ec380db5aee8", environment="us-central1-gcp")
    index = pinecone.Index("ner-search")
    return df, nlp, retriever, index

def extract_named_entities(nlp, text_batch):
    # extract named entities using the NER pipeline
    extracted_batch = nlp(text_batch)
    entities = []
    # loop through the results and only select the entity names
    for text in extracted_batch:
        ne = [entity["word"] for entity in text]
        entities.append(ne)
    return entities

def search_pinecone(nlp, retriever, index, query):
    # extract named entities from the query
    ne = extract_named_entities([query])[0]
    # create embeddings for the query
    xq = retriever.encode(query).tolist()
    # query the pinecone index while applying named entity filter
    xc = index.query(xq, top_k=10, include_metadata=True, filter={"named_entities": {"$in": ne}})
    # extract article titles from the search result
    r = [x["metadata"]["title"] for x in xc["matches"]]
    return ne, r

def run_search(string):
    df, nlp, retriever, index = setup()
    query = string
    ne, result = search_pinecone(nlp, retriever, index, query)
    data = []
    for x in result:
        data.append(df['title_text'][int(x)])
    return ne, data