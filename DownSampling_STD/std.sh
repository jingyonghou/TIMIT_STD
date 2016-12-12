keyword_dir=/home2/jyh705/feature/TIMIT_STD/KEYWORD_TEST/
keyword_list=../lists/timit_test_keyword_all.list
utterance_dir=/home2/jyh705/feature/TIMIT_STD/TEST/
utterance_list=../lists/timit_test.list
nj=18

feature_type="sbnf"
distance_type="cosine" # cosine | KL-divergence

result_dir="/home2/jyh705/feature/TIMIT_STD/KEYWORD_TEST/dtw_result_${feature_type}_${distance_type}/"
mkdir ${result_dir}
python script/split.py $keyword_list $nj

echo "python DownSampling_STD/std.py $keyword_dir $keyword_list $utterance_dir $utterance_list $feature_type $distance_type $sampling_type $result_dir"
for JOB in `seq $nj`; do
{
    python DownSampling_STD/std.py $keyword_dir timit_test_keyword_all.list${JOB} $utterance_dir $utterance_list $feature_type $distance_type $result_dir
    rm timit_test_keyword_all.list${JOB}
} &
done
wait
echo "feature_type: $feature_type, distance_type: $distance_type dtw: $dtw"
python script/evaluation.py $result_dir $keyword_list ../TEST/ $utterance_list


