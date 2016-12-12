import sys
from dataIn import HTKFeat_read
from dataIn import HTKFeat_write

def Slice(begin_index, end_index, input_data, axis=1):
    if axis==1:
        return input_data[:, begin_index:end_index]
    elif axis==0:
        return input_data[begin_index:end_index, :]

if __name__=="__main__":
    if len(sys.argv) < 8:
        print("USAGE: " + sys.argv[0] + "data_dir data_list input_data_type output_data_type sub_num left_phone_num right_phone_num\n")
        exit(1)

    data_dir = sys.argv[1]
    data_lists = open(sys.argv[2]).readlines()
    input_data_type = sys.argv[3]
    output_data_type = sys.argv[4]
    sub_num = int(sys.argv[5])
    left_phone_num = int(sys.argv[6])
    right_phone_num = int(sys.argv[7])

    begin_index = sub_num * (left_phone_num-1)
    end_index = sub_num * left_phone_num

    for i in range(len(data_lists)):
        utterance_id = data_lists[i].strip()
        input_file = data_dir + utterance_id + "." + input_data_type
        data = HTKFeat_read(input_file).getall()
        slice_data = Slice(begin_index, end_index, data, axis=1)
        output_file = data_dir + utterance_id + "." + output_data_type
        HTK_file = HTKFeat_write(output_file, veclen=sub_num, sampPeriod=100000, paramKind=9)
        HTK_file.writeall(slice_data)
        HTK_file.close()

