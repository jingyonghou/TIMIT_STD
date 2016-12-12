for file in `cat list/timit_train.list`;
do 
    rm TRAIN/${file}.WAV
    mv TRAIN/${file}.WAVNEW TRAIN/${file}.WAV
done
