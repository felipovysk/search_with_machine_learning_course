import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Filter categories by number of products.')
general = parser.add_argument_group("general")
general.add_argument("--minProducts", default=500,  help="The minimum amount of products a category must have")
general.add_argument("--input", default='/workspace/datasets/fasttext/labeled_products.txt',  help="The file containing the labeled products")
general.add_argument("--output", default='/workspace/datasets/fasttext/pruned_labeled_products.txt', help="the file to output to")

args = parser.parse_args()
minimumProducts = args.minProducts
inputFile = args.input
outputFile = args.output

df = pd.read_csv(inputFile, header=None, names=["str"])

df = df.str.str.split(' ', n=1, expand=True)
df = df.groupby(0).filter(lambda x: len(x) >= minimumProducts)

df.to_csv(outputFile, sep='\t', header=None, index=False)