#!/bin/bash

echo "category count for threshold = 1000: $(cat /workspace/datasets/shuffled_labeled_query_data_1000.txt | cut -d' ' -f1 | sort | uniq | wc -l)"
echo "category count for threshold = 10000: $(cat /workspace/datasets/shuffled_labeled_query_data_10000.txt | cut -d' ' -f1 | sort | uniq | wc -l)"