#!/bin/bash

FT_DIR=/workspace/datasets/fasttext
ASSESSMENT_DIR=week2

# LEVEL 1
echo 'Running level 1...'

python week2/createContentTrainingData.py --output $FT_DIR/labeled_products.txt
python $ASSESSMENT_DIR/filterCategories.py --input $FT_DIR/labeled_products.txt --output $FT_DIR/pruned_labeled_products.txt --minProducts 500
shuf $FT_DIR/pruned_labeled_products.txt > $FT_DIR/shuffled_labeled_products.txt
head -n10000 $FT_DIR/shuffled_labeled_products.txt > $FT_DIR/training_data.txt
tail -n10000 $FT_DIR/shuffled_labeled_products.txt > $FT_DIR/test_data.txt
~/fastText-0.9.2/fasttext supervised -input $FT_DIR/training_data.txt -output $FT_DIR/product_classifier -wordNgrams 2 -lr 1.0 -epoch 25
~/fastText-0.9.2/fasttext test $FT_DIR/product_classifier.bin $FT_DIR/test_data.txt 1

# LEVEL 2
echo 'Running level 2...'

cut -d$'\t' -f2- $FT_DIR/shuffled_labeled_products.txt > $FT_DIR/normalized_titles.txt
~/fastText-0.9.2/fasttext skipgram -input $FT_DIR/normalized_titles.txt -output $FT_DIR/title_model -minCount 20 -epoch 25
~/fastText-0.9.2/fasttext nn $FT_DIR/title_model.bin

# LEVEL 3
echo 'Running level 3...'

cat $FT_DIR/normalized_titles.txt | tr " " "\n" | grep "...." | sort | uniq -c | sort -nr | head -1000 | grep -oE '[^ ]+$' > $FT_DIR/top_words.txt
python3 $ASSESSMENT_DIR/generateSynonyms.py
docker cp $FT_DIR/synonyms.csv opensearch-node1:/usr/share/opensearch/config/synonyms.csv
./index-data.sh -r -p /workspace/search_with_machine_learning_course/week2/conf/bbuy_products.json
python3 utilities/query.py --synonyms