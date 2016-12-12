#!/bin/bash
CORENUM=20
for feature in vtln_k_2048_gpg;
do
	rm ../data/QUESST2015-dev/dev_queries/*.result
	#1_1 do normal DTW with query dev  with $feature 
	/usr/bin/time -f '%E' ./dtw_std ./quesst2015_dev_test.list ./quesst2015_audio_test.list ${feature} 20
	echo 'have done the quess15_dev DTW with feature $feature'
	#get std xml file, already get T1, T2, T3, alldev
	mkdir -p ../scoring/out/DTW_${feature}_T1/
	mkdir -p ../scoring/out/DTW_${feature}_T2/
	mkdir -p ../scoring/out/DTW_${feature}_T3/
	mkdir -p ../scoring/out/DTW_${feature}_dev/
	
	python stdlist_gen.py ../../list/quesst2015_dev_T1.list 2.5959 ../scoring/out/DTW_${feature}_T1/
	python stdlist_gen.py ../../list/quesst2015_dev_T2.list 2.5959 ../scoring/out/DTW_${feature}_T2/
	python stdlist_gen.py ../../list/quesst2015_dev_T3.list 2.5959 ../scoring/out/DTW_${feature}_T3/
	python stdlist_gen.py ../../list/quesst2015_dev.list 2.5959 ../scoring/out/DTW_${feature}_dev/
	#get the result awtv, mwtv, mxcn, axcn 
    	. ../scoring/score-TWV-Cnxe.sh ../scoring/out/DTW_${feature}_T1/ ../scoring/groundtruth_quesst2015_dev_T1/ 0.1
	. ../scoring/score-TWV-Cnxe.sh ../scoring/out/DTW_${feature}_T2/ ../scoring/groundtruth_quesst2015_dev_T2/ 0.1
	. ../scoring/score-TWV-Cnxe.sh ../scoring/out/DTW_${feature}_T3/ ../scoring/groundtruth_quesst2015_dev_T3/ 0.1
	. ../scoring/score-TWV-Cnxe.sh ../scoring/out/DTW_${feature}_dev/ ../scoring/groundtruth_quesst2015_dev/ 0.1
	#mv .result file to a new direction
	mkdir -p ../dev_result_DTW_${feature}/
	mv ../data/QUESST2015-dev/dev_queries/*.result ../dev_result_DTW_${feature}/

	#1_2 do normal DTW with query eval  with feature czpg
	#/usr/bin/time -f '%E' ./dtw_std quesst14_eval.list audio.list ${feature} 20
	#echo 'have done the quess14_dev DTW with feature $feature'
	#
	#mkdir -p ../scoring/DTW_${feature}_eval/
	#
	#python stdlist_gen.py quesst14_eval.list 2.5959 ../scoring/DTW_${feature}_eval/
	#mkdir -p ../eval_result_DTW_${feature}/
	#. ../scoring/score-TWV-Cnxe.sh ../scoring/DTW_${feature}_eval/ ../scoring/groundtruth_quesst14_eval/ 0.1
	#mv ../eval_queries/*.result ../eval_result_DTW_${feature}/
done

