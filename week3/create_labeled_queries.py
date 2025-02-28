import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv

# Useful if you want to perform stemming.
import nltk
stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/labeled_query_data.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output
threshold = int(args.min_queries)

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[['category', 'query']]
df = df[df['category'].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.
from nltk.stem.snowball import SnowballStemmer
from re import compile
stemmer = SnowballStemmer("english")
RE_SPECIAL = compile('[_\/+-\.]')

def normalize_query(query: str) -> str:
    remove_unnecessary = lambda s: RE_SPECIAL.sub(' ', s)
    normalized_query = ' '.join(map(stemmer.stem, remove_unnecessary(query).lower().split()))
    return normalized_query

df['query'] = df['query'].map(normalize_query)

from functools import cache

@cache
def has_parent(category):
    return parents_df[parents_df['category'] == category].size > 0

def parent(category):
    return parents_df[parents_df['category'] == category].iloc[0]['parent']

def rollback_to_parent(series):
    vc = series[series.apply(has_parent)].value_counts()
    vc = vc[vc < threshold]
    if vc.size == 0:
        return (False, series)
    return (True, series.replace({bc: parent(bc) for bc in vc.index}))

has_bad, new_series = rollback_to_parent(df['category'])
while has_bad:
    df['category'] = new_series
    has_bad, new_series = rollback_to_parent(df['category'])

# Create labels in fastText format.
df['label'] = '__label__' + df['category']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df['category'].isin(categories)]
df['output'] = df['label'] + ' ' + df['query']
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)
