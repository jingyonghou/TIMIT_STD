# TIMIT_STD
## Description
All the code is about STD under TIMIT data set, including several different version of STD code and also with different methods.

## Method
* STD 
     full DTW STD code using C++
* Partial_STD 
     phone boundary based partial STD code using C++
* DownSampling_STD 
    phone boundary based feature reduction using several different downsampling methods, including:
    ** median
    ** mean
    ** uniform
    ** uniform mean
* Encode_STD_v2
    using BLSTM encoder based feature to do STD, also supporting above downsampling options.
