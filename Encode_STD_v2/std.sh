keyword_dir=/home2/jyh705/feature/TIMIT_STD/KEYWORD_TEST/
keyword_list=../lists/timit_test_keyword_all.list
utterance_dir=/home2/jyh705/feature/TIMIT_STD/TEST/
utterance_list=../lists/timit_test.list
model_type=BLSTMP
tag="_3lstm_1dnn"
loss_type=frame #frame # boundary
left_encode_num=4
right_encode_num=3
truncated=0 #0 | 1
keyword_sampling_type="mean"
utterance_sampling_type="mean"

nj=18
feature_type=${model_type}${tag}_${loss_type}_${left_encode_num}_${right_encode_num}
distance_type="KL-divergence" # cosine | KL-divergence
result_dir="/home2/jyh705/feature/TIMIT_STD/KEYWORD_TEST/result_${feature_type}_${distance_type}/"

# write the cmd
echo "python Encode_STD_v2/std.py $keyword_dir $keyword_list $utterance_dir $utterance_list $left_encode_num $right_encode_num $feature_type $distance_type $keyword_sampling_type $utterance_sampling_type $result_dir $truncated"

mkdir ${result_dir}
python script/split.py $keyword_list $nj
for JOB in `seq $nj`; do
{
    python Encode_STD_v2/std.py $keyword_dir timit_test_keyword_all.list${JOB} $utterance_dir $utterance_list \
        $left_encode_num $right_encode_num $feature_type $distance_type $keyword_sampling_type \
        $utterance_sampling_type $result_dir $truncated
    rm timit_test_keyword_all.list${JOB}
} &
done
wait

echo "$model_type $loss_type $left_encode_num $right_encode_num $truncated"
python script/evaluation.py $result_dir $keyword_list ../TEST/ $utterance_list

