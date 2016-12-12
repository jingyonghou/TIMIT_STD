#!/bin/bash
for phone_len in 9; 
do
    python evaluation.py ../KEYWORD_TEST/result_embedding_${phone_len}phone_cosine/ \
        ../lists/timit_test_keyword_all.list ../TEST/ ../lists/timit_test.list
done
