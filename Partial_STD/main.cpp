//=============================================================================
//
// File Name: Lab1.cpp
// Written by: Peng Yang
// Last Revise: Jingyong Hou
// Email: pengyang@nwpu-aslp.org
//
//=============================================================================
#include <infra.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <thread>
#include "HtkFile.h"
#include "Dataset.h"
#include "partial_DTW.h"
#define MISPAR_GADOL_MEOD (1000000000);

using namespace std;
//this function is used to score for one query as the function name told
//parameter: 
//input : query_id //string
//		  test_size //int
//		  featureType //string
//output: test //the out put matrix
int score_for_one_query(const string &query_dir, const string& query_id, \
                        infra::matrix* test, int test_size, const string& featureType, \
                        const string& result_dir, int phone_num) {
	//define a query matrix
	infra::matrix query;
    IntVector bnd_vector;
	string queryFileName = query_dir + query_id + "." + featureType;
    string bndFileName = query_dir + query_id + ".bnd";
    bnd_vector.read(bndFileName); 
    //cout << query_id <<  " finished" << endl;
	//read  query file from queryFileName use vad_label as query matrix
	if (!read_htk(queryFileName, query)) {
		return EXIT_FAILURE;
	}
	
    //if the feature type is mfc  mvn normalization
	if (featureType.find("fbank") != std::string::npos || featureType.find("mfc") != std::string::npos ||
        featureType.find("sbnf") != std::string::npos) {
		mvn(query);
    }
	
	if (featureType.find("fbank") != std::string::npos || featureType.find("mfc") != std::string::npos ||
        featureType.find("sbnf") != std::string::npos) {
	    normalizeFea(query);
    }
    
    //normal DTW	
	ofstream ofs((result_dir + query_id + ".RESULT").c_str());

	// run over the test set				
	for (int i = 0; i < test_size; i++) {
	//	dynamic programming between query and test[i]
		unsigned long height = query.height();
		unsigned long width = test[i].height();
		infra::matrix dist(height, width);
		
		computeDist(query, test[i], dist, featureType);
		float score = subsequnceDTW(dist, bnd_vector, phone_num);
		ofs << score << endl;
	}

	ofs.close();

	return EXIT_SUCCESS;
}

int main(int argc, char *argv[]) {	
	if(argc < 8) {
		cerr<<"USAGE: queryDir queryListFile testDir testListFile featureType  resultDir num_cpu_core" << endl;
		return EXIT_FAILURE;
	}

	string queryDir;
    string queryListFile;
    string testDir;
	string testListFile;
	string featureType;
    string resultDir;
	int numCpuCore;
    int phone_num;

	queryDir = string(argv[1]);
    queryListFile = string(argv[2]);
	testDir = string(argv[3]);
    testListFile = string(argv[4]);
	featureType = string(argv[5]);
    resultDir = string(argv[6]);
    phone_num = atoi(argv[7]);
    numCpuCore = atoi(argv[8]);
    
	StringVector queryList;
	queryList.read(queryListFile);

	StringVector testList;
	testList.read(testListFile);
	
	// read test set
    infra::matrix* test = new infra::matrix[testList.size()];
	for (int i = 0; i < testList.size(); i++) {
		string testFileName(testDir + testList[i] + "." + featureType);
		if (!read_htk(testFileName, test[i])) {
			return EXIT_FAILURE;
		}

	    if (featureType.find("fbank") != std::string::npos || featureType.find("mfc") != std::string::npos ||
            featureType.find("sbnf") != std::string::npos) {
			mvn(test[i]);
        }

	    if (featureType.find("fbank") != std::string::npos || featureType.find("mfc") != std::string::npos ||
            featureType.find("sbnf") != std::string::npos) {
			normalizeFea(test[i]);
        }
	}	

    //debug the function of score_for_one_query()
	for (int i =0;i<queryList.size();i++){
	    score_for_one_query(queryDir, queryList[i], test, testList.size(), featureType, resultDir, phone_num);
	}	
	
    // for each of the query files
	//for ( int i=0; i < queryList.size(); i += numCpuCore) {
	//	
	//    unsigned count_thread = 0;
	//	int j=i;
	//	thread t[numCpuCore];
	//	while( count_thread < numCpuCore && j < queryList.size() ) {
	//		t[count_thread] = thread(score_for_one_query, queryDir, queryList[j], test, testList.size(), featureType, resultDir);
	//		j++;
	//		count_thread++;
	//	}	
    //    
	//	for (int c = 0; c < count_thread; c++) {
	//		t[c].join();
    //    }
	//}	
	delete [] test;
	return EXIT_SUCCESS;
}

