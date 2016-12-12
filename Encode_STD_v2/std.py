import sys
import numpy as np
from Keyword import Keyword
from Utterance import Utterance
import Distance
import log
def spoken_term_detection_truncated(keywords, utterances, left_encode_num, right_encode_num, distance_type, output_dir):
    for i in range(len(keywords)):
        keyword_sampling_feature = keywords[i].sampling_feature
        keyword_phone_num = keyword_sampling_feature.shape[0]
        (left_position, right_position) = get_truncated_position(keyword_phone_num, left_encode_num, right_encode_num)
        keyword_indexes_selected = get_real_indexes(range(keyword_phone_num), left_encode_num, right_encode_num)
        keyword_sampling_feature_selected = keyword_sampling_feature[keyword_indexes_selected, :]
        output_file = output_dir + keywords[i].getFileId() + ".RESULT"
        fid = open(output_file, "w")
        for j in range(len(utterances)):
            utterance_sampling_feature = utterances[j].sampling_feature
            utterance_phone_num = utterance_sampling_feature.shape[0]
            utterance_indexes_selected = get_real_indexes(range(utterance_phone_num), left_encode_num, right_encode_num)
            utterance_sampling_feature_selected = utterance_sampling_feature[utterance_indexes_selected, :]
            distance = Distance.distance(keyword_sampling_feature_selected[:, left_position:right_position], utterance_sampling_feature_selected[:, left_position:right_position], distance_type, sub_num=40)
            fid.writelines(str(distance.min()) + "\n")
        fid.close()
        log.Log("finished the std for keyword " + str(keywords[i].getFileId()))\

def spoken_term_detection(keywords, utterances, left_encode_num, right_encode_num, distance_type, output_dir):
    for i in range(len(keywords)):
        keyword_sampling_feature = keywords[i].sampling_feature
        keyword_phone_num = keyword_sampling_feature.shape[0]
        keyword_indexes_selected = get_real_indexes(range(keyword_phone_num), left_encode_num, right_encode_num)
        keyword_sampling_feature_selected = keyword_sampling_feature[keyword_indexes_selected, :]
        output_file = output_dir + keywords[i].getFileId() + ".RESULT"
        fid = open(output_file, "w")
        for j in range(len(utterances)):
            utterance_sampling_feature = utterances[j].sampling_feature
            utterance_phone_num = utterance_sampling_feature.shape[0]
            utterance_indexes_selected = get_real_indexes(range(utterance_phone_num), left_encode_num, right_encode_num)
            utterance_sampling_feature_selected = utterance_sampling_feature[utterance_indexes_selected, :]
            distance = Distance.distance(keyword_sampling_feature_selected, utterance_sampling_feature_selected, distance_type, sub_num=40)
            fid.writelines(str(distance.min()) + "\n")
        fid.close()
        log.Log("finished the std for keyword " + str(keywords[i].getFileId()))\

def get_truncated_position(phone_num, left_encode_num, right_encode_num):
    encode_num = left_encode_num + right_encode_num
    if phone_num < encode_num:
            if right_encode_num == 0:
                left_phone_num = phone_num
                right_phone_num = 0
            else:
                left_phone_num = phone_num//2 + 1
                right_phone_num = phone_num//2 - 1 + phone_num%2
            left_jump = left_encode_num - left_phone_num
            right_jump = right_encode_num - right_phone_num
            left_position = left_jump * PHONE_LEN
            right_position = (encode_num - right_jump) * PHONE_LEN
        else:
            left_position = 0
            right_position = encode_num * PHONE_LEN
    return (left_position, right_position)

def get_real_indexes(indexes, left_encode_num, right_encode_num):
    if len(indexes) > left_encode_num + right_encode_num:
        return indexes[left_encode_num-1 : len(indexes)-right_encode_num]
    elif right_encode_num == 0:
        return [indexes[-1]]
    else:
        return [indexes[len(indexes)//2]]

def sampling(entities, sampling_type):
    for i in range(len(entities)):
        entities[i].downSampling(sampling_type)

if __name__=='__main__':
    if len(sys.argv) < 13:
        print("USAGE: python " + sys.argv[0] + " keyword_dir keyword_list  utterance_dir utterance_list left_encode_num, right_encode_num, feature_type distance_type keyword_sampling_type utterance_sampling_type output_dir truncated_mod")
        exit(1)
    keyword_dir = sys.argv[1]
    keyword_list_file = sys.argv[2]
    utterance_dir = sys.argv[3]
    utterance_list_file = sys.argv[4]
    left_encode_num = int(sys.argv[5])
    right_encode_num = int(sys.argv[6])
    feature_type = sys.argv[7]
    distance_type = sys.argv[8]
    keyword_sampling_type = sys.argv[9]
    utterance_sampling_type = sys.argv[10]
    output_dir = sys.argv[11]
    truncated_mod = int(sys.argv[12])
    # read keyword and do downsampling
    keyword_lists = open(keyword_list_file).readlines()
    keywords = []
    for i in range(len(keyword_lists)):
        keyword_id = keyword_lists[i].strip()
        new_entity = Keyword(keyword_dir, keyword_id, feature_type, phone_type="PHN39", wav_sampling_rate=16000)
        keywords.append(new_entity)

    # read utterance and do downsampling
    utterance_lists = open(utterance_list_file).readlines()
    utterances = []
    for i in range(len(utterance_lists)):
        utterance_id = utterance_lists[i].strip()
        new_entity = Utterance(utterance_dir, utterance_id, feature_type, phone_type="PHN39", wav_sampling_rate=16000)
        utterances.append(new_entity)

    # down sampling of keyword and utterance
    sampling(keywords, keyword_sampling_type)
    sampling(utterances, utterance_sampling_type)
    if (truncated_mod==False):
        spoken_term_detection(keywords, utterances, left_encode_num, right_encode_num, distance_type, output_dir)
    else:
        spoken_term_detection_truncated(keywords, utterances, left_encode_num, right_encode_num, distance_type, output_dir)
