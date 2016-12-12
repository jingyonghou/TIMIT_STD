#!/usr/bin/bash
stage=1
core_num=18
keyword_dir="/home2/jyh705/feature/TIMIT_STD/KEYWORD_TEST/"
keyword_list_file="../lists/timit_test_keyword_all.list"
#keyword_list_file="keyword_debug.list"
test_dir="/home2/jyh705/feature/TIMIT_STD/TEST/"
test_list_file="../lists/timit_test.list"
fea_type="enpg4"
result_dir=${keyword_dir}dtw_${fea_type}/;
if [ $stage -le 1 ]; then
    mkdir -p $result_dir
    python script/split.py ${keyword_list_file} ${core_num}
    for i in `seq $core_num`; do
    {
        echo "./STD/dtw_std $keyword_dir timit_test_keyword_all.list${i} $test_dir $test_list_file $fea_type $result_dir $core_num"
        ./STD/dtw_std $keyword_dir timit_test_keyword_all.list${i} $test_dir $test_list_file $fea_type $result_dir $core_num
        rm timit_test_keyword_all.list${i}
    } &
    done
    wait
fi


echo "python script/evaluation.py $result_dir $keyword_list_file ../TEST/ $test_list_file"
python script/evaluation.py $result_dir $keyword_list_file ../TEST/ $test_list_file
