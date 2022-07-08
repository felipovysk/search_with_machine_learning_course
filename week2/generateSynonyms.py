import argparse
import fasttext

parser = argparse.ArgumentParser(description='Filter categories by number of products.')
general = parser.add_argument_group("general")
general.add_argument('--model', default='/workspace/datasets/fasttext/title_model.bin')
general.add_argument("--input", default='/workspace/datasets/fasttext/top_words.txt',  help="The file containing the words to gather synonyms")
general.add_argument("--output", default='/workspace/datasets/fasttext/synonyms.csv', help="the file to output to")

args = parser.parse_args()
modelFile = args.model
inputFile = args.input
outputFile = args.output

model = fasttext.load_model(modelFile)

with open(inputFile, 'r') as words:
    with open(outputFile, 'w') as out:
        for word in words:
            line = word.strip()
            has_synonym = False
            for _, synonym in filter(lambda x: x[0] > 0.8, model.get_nearest_neighbors(word)):
                has_synonym = True
                line += f', {synonym}'
            if has_synonym:
                out.write(f'{line}\n')
