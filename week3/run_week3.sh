#!/bin/bash

label_queries() {
    local threshold=$1
    local normal_out_file="/workspace/datasets/labeled_query_data_${threshold}.txt"
    local shuffled_out_file="/workspace/datasets/shuffled_labeled_query_data_${threshold}.txt"
    echo "saving labeled queries with threshold ${threshold} in ${normal_out_file}"
    python3 week3/create_labeled_queries.py --min_queries $threshold --output $normal_out_file
    shuf $normal_out_file > $shuffled_out_file
}

train_and_test() {
    local threshold=$1
    local model_name="/workspace/models/$2_${threshold}"
    echo "creating ${model_name}"
    local shuffled_in_file="/workspace/datasets/shuffled_labeled_query_data_${threshold}.txt"
    local query_count=$(wc -l $shuffled_in_file | cut -d' ' -f1)
    local train_size=$(( $query_count * 1 / 10 ))
    local test_size=$(( $query_count * 1 / 10 ))
    local train_file="${shuffled_in_file}${train_size}"
    local test_file="${shuffled_in_file}t${test_size}"
    head -n $train_size $shuffled_in_file > $train_file
    tail -n $test_size $shuffled_in_file > $test_file
    echo "running fasttext with ${*:3}, train size is $train_size"
    #~/fastText-0.9.2/fasttext supervised -input $train_file -output $model_name ${@:3}
    for i in {1,3,5};
        do echo "testing @$i, test size is $test_size";
        ~/fastText-0.9.2/fasttext test "${model_name}.bin" $test_file $i;
    done
}

full_run() {
    local threshold=$1
    echo "starting run with threshold $threshold"
    #label_queries $threshold
    train_and_test $threshold default_model
    train_and_test $threshold lr0.4_model -lr 0.4
    train_and_test $threshold lr0.4_epoch10_model -lr 0.4 -epoch 10
}

full_run 1000
full_run 10000