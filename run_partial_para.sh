#!/usr/bin/bash

core_num=18
keyword_dir="/home2/jyh705/feature/TIMIT_STD/KEYWORD_TEST/"
keyword_list_file="../lists/timit_test_keyword_all.list"
#keyword_list_file="keyword_debug.list"
test_dir="/home2/jyh705/feature/TIMIT_STD/TEST/"
test_list_file="../lists/timit_test.list"
fea_type="enpg4"
result_dir=${keyword_dir}_partial_dtw_${fea_type}/;
mkdir -p $result_dir
python script/split.py ${keyword_list_file} ${core_num}
for phone_num in 5 6 7 8 9 10 11; do
    echo "./Partial_STD/partial_dtw_std $keyword_dir ${keyword_list_file} $test_dir $test_list_file $fea_type $result_dir $phone_num $core_num"
    for i in `seq $core_num`; do
    {
        ./Partial_STD/partial_dtw_std $keyword_dir timit_test_keyword_all.list${i} $test_dir \
            $test_list_file $fea_type $result_dir $phone_num $core_num
    } &
    done
    wait
    echo "$fea_type $phone_num"
    python script/evaluation.py $result_dir $keyword_list_file ../TEST/ $test_list_file
done
rm timit_test_keyword_all.list*
