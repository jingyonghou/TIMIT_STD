import sys
import numpy as np
from Keyword import Keyword
from Utterance import Utterance
import Distance
from DTW import subsequenceDTW
import log
def partial_matching(distance, phone_position, window_size):
    phone_num = len(phone_position)
    costs=[]
    for i in range(window_size, phone_num+1):
        s_frame = phone_position[i-window_size][0]
        e_frame = phone_position[i-1][1]
        cost, path = subsequenceDTW(distance[s_frame:e_frame, :])
        costs.append(cost)
    return min(costs)
    
def spoken_term_detection_dtw(keywords, utterances, distance_type, output_dir, window_size):
    for i in range(len(keywords)):
        keyword_feature = keywords[i].feature
        phone_num = keywords[i].getPhoneNum()
        phone_position = keywords[i].phone_position
        if phone_num<window_size:
            window_size_used = phone_num
        else:
            window_size_used = window_size

        output_file = output_dir + keywords[i].getFileId() + ".RESULT"
        fid = open(output_file, "w")
        for j in range(len(utterances)):
            utterance_feature = utterances[j].feature
            distance = Distance.distance(keyword_feature, utterance_feature, distance_type, sub_num=30)
            cost_min = partial_matching(distance, phone_position, window_size_used)
            fid.writelines(str(cost_min) + "\n")
        fid.close()
        log.Log("finished the std for keyword " + str(keywords[i].getFileId()))

def mvn_norm_feature(entities):
    for i in range(len(entities)):
        entities[i].mvnFeats()
        entities[i].normFeats()

if __name__=='__main__':
    if len(sys.argv) < 8:
        print("USAGE: python " + sys.argv[0] + " keyword_dir keyword_list utterance_dir utterance_list feature_type distance_type output_dir")
        exit(1)

    keyword_dir = sys.argv[1]
    keyword_list_file = sys.argv[2]
    utterance_dir = sys.argv[3]
    utterance_list_file = sys.argv[4]
    feature_type = sys.argv[5]
    distance_type = sys.argv[6]
    output_dir = sys.argv[7]

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
    if "mfc" in feature_type or "bnf" in feature_type:
        mvn_norm_feature(keywords)
        mvn_norm_feature(utterances)

    spoken_term_detection_dtw(keywords, utterances, distance_type, output_dir, 30)
        
