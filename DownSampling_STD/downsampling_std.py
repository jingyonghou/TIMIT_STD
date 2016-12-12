import sys
import numpy as np
from Keyword import Keyword
from Utterance import Utterance
import Distance
from DTW import subsequenceDTW
import log
def get_fix_vector(feature, window_size):
    compare_matrix = []
    feature_len = feature.shape[0]
    feature_dim = feature.shape[1]
    
    for i in range(window_size, feature_len+1):
        compare_matrix.append(feature[i-window_size:i, :].reshape(1, window_size*feature_dim))
    if window_size > feature_len:
        new_vector = np.concatenate([np.tile(feature[0,:], [window_size-feature_len, 1]) , feature])
        compare_matrix.append(new_vector.reshape(1, window_size*feature_dim))
    return np.concatenate(compare_matrix)

def spoken_term_detection(keywords, utterances, distance_type, output_dir, window_size):
    for i in range(len(keywords)):
        keyword_sampling_feature = keywords[i].sampling_feature
        feature_len = keyword_sampling_feature.shape[0]
        if feature_len < window_size:
            window_size_used = feature_len
        else:
            window_size_used = window_size
        keyword_sampling_feature_vector = get_fix_vector(keyword_sampling_feature, window_size_used)
        output_file = output_dir + keywords[i].getFileId() + ".RESULT"
        fid = open(output_file, "w")
        for j in range(len(utterances)):
            utterance_sampling_feature = utterances[j].sampling_feature
            utterance_sampling_feature_vector = get_fix_vector(utterance_sampling_feature, window_size_used)
            distance = Distance.distance(keyword_sampling_feature_vector, utterance_sampling_feature_vector, distance_type, sub_num=30)
            fid.writelines(str(distance.min()) + "\n")
        fid.close()
        log.Log("finished the std for keyword " + str(keywords[i].getFileId()))

def partial_matching(distance, window_size):
    height = distance.shape[0]
    costs=[]
    for i in range(window_size, height+1):
        cost, path = subsequenceDTW(distance[i-window_size:window_size, :])
        costs.append(cost)
    return min(costs)
    
def spoken_term_detection_dtw(keywords, utterances, distance_type, output_dir, window_size):
    for i in range(len(keywords)):
        keyword_sampling_feature = keywords[i].sampling_feature
        feature_len = keyword_sampling_feature.shape[0]
        if feature_len<window_size:
            window_size_used = feature_len
        else:
            window_size_used = window_size

        output_file = output_dir + keywords[i].getFileId() + ".RESULT"
        fid = open(output_file, "w")
        for j in range(len(utterances)):
            utterance_sampling_feature = utterances[j].sampling_feature
            distance = Distance.distance(keyword_sampling_feature, utterance_sampling_feature, distance_type, sub_num=30)
            cost_min = partial_matching(distance, window_size_used)
            fid.writelines(str(cost_min) + "\n")
        fid.close()
        log.Log("finished the std for keyword " + str(keywords[i].getFileId()))

def mvn_norm_feature(entities):
    for i in range(len(entities)):
        entities[i].mvnFeats()
        entities[i].normFeats()

def sampling(entities, sampling_type):
    for i in range(len(entities)):
        entities[i].downSampling(sampling_type)

if __name__=='__main__':
    if len(sys.argv) < 10:
        print("USAGE: python " + sys.argv[0] + " keyword_dir keyword_list utterance_dir utterance_list feature_type distance_type sampling_type output_dir [dtw_mod]")
        exit(1)

    keyword_dir = sys.argv[1]
    keyword_list_file = sys.argv[2]
    utterance_dir = sys.argv[3]
    utterance_list_file = sys.argv[4]
    feature_type = sys.argv[5]
    distance_type = sys.argv[6]
    sampling_type = sys.argv[7]
    output_dir = sys.argv[8]
    DTW_mod = int(sys.argv[9])

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

    sampling(keywords, sampling_type)
    sampling(utterances, sampling_type)

    if (DTW_mod==False):
        spoken_term_detection(keywords, utterances, distance_type, output_dir, 30)
    else:
        spoken_term_detection_dtw(keywords, utterances, distance_type, output_dir, 30)
        
