import sys
import numpy as np
import log
from dataIn import HTKFeat_read


class BaseEntity(object):
    "base class used to define some general property of keyword and utterance"
    
    __file_dir=None
    __file_id=None
    __feature_type=None
    __phone_type=None
    __wav_sampling_rate=None
    
    feature=None
    phone_num=None
    phone_position=None
    sampling_feature=None

    def __init__(self, file_dir, file_id, feature_type, phone_type="PHN39", wav_sampling_rate=16000):
        self.__file_dir = file_dir
        self.__file_id = file_id
        self.__feature_type = feature_type
        self.__phone_type = phone_type
        self.__wav_sampling_rate = wav_sampling_rate
        self.__frame_size = float(self.__wav_sampling_rate/1000*25)
        self.__frame_step = float(self.__wav_sampling_rate/1000*10)
        self.readFeats()

    def readFeats(self):
        feature_file_name = self.__file_dir + self.__file_id + "." + self.__feature_type
        self.feature = HTKFeat_read(feature_file_name).getall()

    def mvnFeats(self):
        mean = np.mean(self.feature, axis = 0)
        self.feature = self.feature - mean
        stdvar = np.std(self.feature, axis = 0)
        self.feature = self.feature / stdvar

    def normFeats(self):
        feature_len = self.feature.shape[0]
        mod = np.sqrt(np.sum(self.feature * self.feature, axis=1)).reshape(feature_len, 1)
        self.feature = self.feature / mod

    def point2frame(self, time_int):
        frame_index = int((time_int-self.__frame_size)/self.__frame_step) + 1
        if frame_index < 0:
            frame_index = 0
        if frame_index > self.feature.shape[0]-1:
            frame_index = self.feature.shape[0]-1
        return frame_index
        
    def initPhonePosition(self):
        self.phone_position = [] 
        phone_file_name = self.__file_dir + self.__file_id + "." + self.__phone_type
        phones_with_times = open(phone_file_name).readlines()
        s_time1, e_time1, phone1 = phones_with_times[0].strip().split()
        for j in range(len(phones_with_times)):
            s_time, e_time, phone = phones_with_times[j].strip().split()
            s_time_int = int(s_time)-int(s_time1)
            e_time_int = int(e_time)-int(s_time1)
            s_frame = self.point2frame(s_time_int)
            e_frame = self.point2frame(e_time_int)
            if e_frame <= s_frame:
                continue
            self.phone_position.append([s_frame, e_frame])
        self.validatePhonePosition()

    def validatePhonePosition(self):
        for i in range(len(self.phone_position)):
            if self.phone_position[i][0] > self.phone_position[i][1]:
                log.Error("phone position error")
            elif self.phone_position[i][0] == self.phone_position[i][1]:
                log.Warn("this phone only has one frame: "+ self.__file_id + " " + str(self.phone_position))
        
    def downSampling(self, sampling_type="median"):
        if self.phone_position == None and sampling_type != "uniform":
            self.initPhonePosition()

        if self.sampling_feature == None:
            samplingFunction = self.getSamplingFunction(sampling_type)
            self.sampling_feature = samplingFunction()
        else:
            log.Warn("repeat downsampling")

    def getSamplingFunction(self, sampling_type):
        sampling_type_enum={"median":self.medianSampling, "mean":self.meanSampling, "lastframe":self.lastframeSampling, "uniform":self.uniformSampling, "uniform_mean":self.uniformMeanSampling}
        if sampling_type_enum.has_key(sampling_type):
            return sampling_type_enum[sampling_type]
        else:
            log.Error("No such kind of sampling function")


    def medianSampling(self):
        index=[]
        for i in range(len(self.phone_position)):
            median = int((self.phone_position[i][0] + self.phone_position[i][1])/2)
            index.append(median)
        return self.feature[index, :]
 
    def meanSampling(self):
        mean_sampling_features = []
        for i in range(len(self.phone_position)):
            s_index = self.phone_position[i][0]
            e_index = self.phone_position[i][1]
            mean_feature = self.feature[s_index:e_index, :].mean(0).reshape(1, 30)
            #mean_feature = mean_feature / mean_feature.max()
            mean_sampling_features.append(mean_feature)
        return np.concatenate(mean_sampling_features)

    def lastframeSampling(self):
        index=[]
        for i in range(len(self.phone_position)):
            index.append(self.phone_position[i][1])
        return self.feature[index, :]

    def uniformSampling(self, step=5):
        index=[]
        for i in range(step, self.feature.shape[0], step):
            index.append(i)
        return self.feature[index, :]

    def uniformMeanSampling(self, step=5):
        mean_sampling_features = []
        for i in range(step, self.feature.shape[0], step):
            s_index = i-step
            e_index = i
            mean_feature = self.feature[s_index:e_index, :].mean(0).reshape(1, 30)
            mean_sampling_features.append(mean_feature)
        return np.concatenate(mean_sampling_features)

#============================================================================#
    def getPhoneNum(self):
        if self.phone_num != None:
            return self.phone_num
        elif self.phone_num == None and self.phone_position != None:
            self.phone_num = len(self.phone_position)
            return self.phone_num
        elif self.phone_num == None and self.phone_position == None:
            self.initPhonePosition()
            self.phone_num = len(self.phone_position)
            return self.phone_num

    def getFeats(self):
        if self.feature == None:
            readFeats()
        return self.feature

    def getDownSamplingFeats(self, sampling_type="median"):
        if self.sampling_feature != None:
            return self.sampling_feature
        elif self.sampling_feature == None and phone_position == None:
            initPhonePosition()
            self.downSampling(sampling_type)
            return self.sampling_feature
        else:
            self.downSampling(sampling_type)
            return self.sampling_feature

    def getFileId(self):
        return self.__file_id
