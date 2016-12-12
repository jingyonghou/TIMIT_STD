#/usr/bin/env python
# coding:utf-8

#author: jingyong 2015/11/14
#last revise: jingyonghou 2016/08/18, fixed the bug in function writeKeywordPhone
#description: this program used to extract keyword in timit, using two set,
#one called test set and another called train set using .WAV
#.PHN .WRD files of each sentence
#input: finddir(string) findlist(string) extractdir(string) extractlist(string) keyworddir(string)
#output: extracted different keyword numbers(write the extracted keyword to the Designated keyword dir)
#example: extract_keyword TEST/ list/timit_test.list TRAIN/ list/timit_train.list KEYWORD_TEST/
import sys
from numpy  import fromfile
import scipy.io.wavfile as wave

def writeKeywordPhone(kPhone,fPhone,st,ed):
    fid = open(fPhone)
    lines = fid.readlines()
    fid.close()
    s_times=[]
    e_times=[]
    phone_ids=[]
    for line in lines:
        s_time, e_time, phone_id=line.strip().split()
        s_times.append(s_time)
        e_times.append(e_time)
        phone_ids.append(phone_id)

    for i in range(len(phone_ids)):
        if s_times[i] == st:
            locS = i
            break;
    for i in range(locS, len(phone_ids)):
        if e_times[i] == ed:
            locE = i
            break;
    if locS>=0 and locE>=0 and locE>=locS:
        fid = open(kPhone,'wb')
        for i in range(locS, locE+1):
            fid.write(lines[i])
        fid.close()
    else:
        print("some thing wrong when we writeKeywordPhone")

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("split.py  TEST/ list/timit_test.list TRAIN/ list/timit_train.list KEYWORD_TEST/")

    finddir=sys.argv[1]
    findlist=sys.argv[2]
    extractdir=sys.argv[3]
    extractlist=sys.argv[4]
    keyworddir=sys.argv[5]
    vocabulary = dict()
    sampleRate = 16000	#Hz
    LeastDura = 0.35*sampleRate # the least duration time is 0.35s

    fid = open(findlist)
    wrdfiles = fid.readlines()
    fid.close()
    for f in wrdfiles:
        fid = open(finddir + f.strip()+'.WRD')
        lines = fid.readlines()
        fid.close()
        for line in lines:
            t_start,t_end,word = line.split()
            if int(t_end) - int(t_start) + 1 >= LeastDura and len(word)>=6:
                if vocabulary.has_key(word):
                    vocabulary[word]+=1
                else:
                    vocabulary[word]=1
    #读取了test中所有的可以以作为关键词的单词以及该单词出现的次数

    fid = open(extractlist)
    traindir=extractdir
    wrdfiles = fid.readlines()
    fid.close()

    record = dict() # to record how many times certain word samples have been extracted
    # 某个单词

    for f in wrdfiles:
        #
        fid = open(extractdir + f.strip()+'.WRD')
        lines = fid.readlines()
        fid.close()
        for line in lines:
            t_start,t_end,word = line.split()
            if int(t_end) - int(t_start) + 1 >= LeastDura and len(word)>=6:
                if vocabulary.has_key(word) and vocabulary[word]>=5:
                    # read the NIST format wav
                    if(word=='withdraw'):
                        print(f)
                    sampleRate, samples=wave.read(extractdir + f.strip()+'.WAV', False)
                    if record.has_key(word):
                        filename = keyworddir + word + '_'+str(record[word])
                        record[word]+=1
                    else:
                        filename = keyworddir + word + '_0'
                        record[word]=1
                    print t_start,t_end,word,f
                    wave.write(filename+'.WAV',sampleRate,samples[int(t_start):int(t_end)])
                    writeKeywordPhone(filename+'.PHN', extractdir + f.strip() + '.PHN', t_start, t_end)
    print(str(len(record))+' diffrent words in all are extracted')
