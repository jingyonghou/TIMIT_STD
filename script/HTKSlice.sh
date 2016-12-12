
#USAGE: script/HTKSlice.py data_dir data_list input_data_type output_data_type sub_num left_phone_num right_phone_num
input_data_type=BLSTMP_2lstm_1dnn_frame_4_3
output_data_type=enpg4
test_data_dir=/home2/jyh705/feature/TIMIT_STD/TEST/
test_data_list_file=../lists/timit_test.list
keyword_data_dir=/home2/jyh705/feature/TIMIT_STD/KEYWORD_TEST/
keyword_data_list_file=../lists/timit_test_keyword_all.list
PHONE_NUM=40

echo "script/HTKSlice.py $test_data_dir $test_data_list_file $input_data_type $output_data_type $PHONE_NUM 4 3"
python script/HTKSlice.py $test_data_dir $test_data_list_file $input_data_type $output_data_type $PHONE_NUM 4 3

echo "script/HTKSlice.py $keyword_data_dir $keyword_data_list_file $input_data_type $output_data_type $PHONE_NUM 4 3"
python script/HTKSlice.py $keyword_data_dir $keyword_data_list_file $input_data_type $output_data_type $PHONE_NUM 4 3

