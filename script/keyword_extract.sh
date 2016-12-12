rm -r ../KEYWORD_TEST/
mkdir ../KEYWORD_TEST/
python keyword_extract.py ../TEST/ ../lists/timit_test.list ../TRAIN/ ../lists/timit_train.list ../KEYWORD_TEST/
find ../KEYWORD_TEST -name *.WAV |sed -e 's:../KEYWORD_TEST/::g' -e 's:.WAV::' |sort > ../lists/timit_test_keyword_all.list
#python keyword_extract.py TRAIN/ list/timit_train.list TEST/ list/timit_test.list KEYWORD_TRAIN/
