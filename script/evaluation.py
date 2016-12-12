
"""
Created on Fri Dec 20 11:49:45 2013

@author: MatlabUser
@modified by jingyonghou@nwpu-aslp.org 2015/11/22
"""
import numpy as np
import sys

def longest_common_substring(s1, s2):   # not dynamic programing, just brute force way.
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]

def relevant(querylistitem,doc):
    ind_s = querylistitem.rfind('/')
    ind_e = querylistitem.rfind('_')
    query = querylistitem.strip()[ind_s+1:ind_e]
    fid = open(doc.strip()+'.WRD')
    lines = fid.readlines()
    fid.close()
    for line in lines:
        word = line.split()[2]
        lcs = longest_common_substring(word,query)
        #print 'linelength:'+str(len(lcs)) +'\t' + 'query ' + '"' + query + '"' + ' length: ' + str(len(query))
        #print 'ratio: ' + str(float(len(lcs))/len(query))
        if float(len(lcs))/len(query)>=0.8 :
            #if word != query:
            #    print("Warnning: " + word + ", " + query + "\n" )
            return True
    return False

def evaluate(costlist, test_dir, doclist, keyword_dir, querylist):
    '''
    costlist = [query_1_list,...,query_n_list]
    doclist: the path list for the every doc
    querylist: the path list for the querys
    '''
    PatNset = []
    APset = []
    Pat10set = []
    for i in range(0,len(querylist)):
        ranklist = np.array(costlist[i]).argsort()
        # percision[i] = num_rele/(i+1),num_rele is the number of the hits in the first i
        Precision = []
        num_rele = 0.0
        sum_precision = 0.0
        #print 'query' + str(i) + ':' + str(len(ranklist));
        for j in range(0,len(ranklist)):
            doc = doclist[ranklist[j]]
            isRele = False
            if relevant(keyword_dir+querylist[i], test_dir+doc):
                #print 'true'
                num_rele = num_rele+1
                isRele = True
            Precision.append(num_rele/(j+1))
            if isRele == True:
                sum_precision += Precision[-1]
#                print j+1,Precision[-1]
        #ind_s = querylist[i].rfind('/')
        #ind_e = querylist[i].rfind('_')
        #word = querylist[i].strip()[ind_s+1:ind_e]
        #fid = open("std_out.log","a")
        #fid.write("The hit numbers in the first 500 utterances for keyword " +  word + " :\t " + str(Precision[499]*500) + "/" + str(num_rele)+"\t"+ str(Precision[499]*500/num_rele) +"\n")
        #fid.close()
        Pat10set.append(Precision[9])
        N = int(num_rele)
        #print querylist[i].strip()[31:-2],N
        PatNset.append(Precision[N-1])
        APset.append(sum_precision/N)
        #print(str(Pat10set[-1]) + " " + str(PatNset[-1]) + " " + str(APset[-1]))
        print(str(APset[-1]) + "\t" + str(PatNset[-1]) + "\t" + str(Pat10set[-1]))

    num_of_querys = len(querylist)
    MAP = sum(APset)/num_of_querys
    PatN = sum(PatNset)/num_of_querys
    Pat10 = sum(Pat10set)/num_of_querys
#    print PatNset
#    print Pat10set
    return MAP,PatN,Pat10


if __name__=='__main__':
    if len(sys.argv) < 5:
        print 'USAGE: result_dir keywordlist  test_dir testlist'
        exit(1)

    result_dir = sys.argv[1]
    fid = open(sys.argv[2])
    keywordlist = fid.readlines()
    fid.close()

    test_dir = sys.argv[3]
    fid = open(sys.argv[4])
    testlist = fid.readlines()
    fid.close()

    costlist = []
    for keyword in keywordlist:
        result_fid = open(result_dir + keyword.strip() + ".RESULT")
        resList = result_fid.readlines()
        result_fid.close();
        scoreList = [];
        for res in resList:
            #testID,tbeg,dur,score = res.strip().split();
            score = res.strip();
            scoreList.append(float(score));
        costlist.append(scoreList);
    MAP,PatN,Pat10 = evaluate(costlist, test_dir, testlist, result_dir, keywordlist)
    print('MAP=%.3f PatN=%.3f Pat10=%.3f'%(MAP,PatN,Pat10))

