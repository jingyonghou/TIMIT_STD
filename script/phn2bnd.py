#!~/anaconda2/bin/python

import sys

if __name__=='__main__':
    if len(sys.argv) < 3:
        print("USAGE: python" + sys.argv[0] + "  keyword_dir keyword_list_file")
        exit(1)
    keyword_dir = sys.argv[1]
    keyword_list_file = sys.argv[2]

    keyword_list = open(keyword_list_file).readlines()

    for keyword_id in keyword_list:
        phn_list = open(keyword_dir + keyword_id.strip() + ".PHN").readlines()
        start_time, end_time, phone_id = phn_list[0].strip().split()  
        fid = open(keyword_dir + keyword_id.strip() + ".bnd", "w")
        bnd_times=[]
        bnd_times.append(0)
        for i in range(len(phn_list)):
            new_start_time, new_end_time, new_phone_id = phn_list[i].strip().split()
            next_bnd = int(((int(new_end_time)-int(start_time))-400) / 160 + 1)
            if next_bnd <= 0:
                print("warnning:bnd less than 0\n")
                continue
            bnd_times.append(next_bnd)
        fid.writelines(str(len(bnd_times)))
        for i in range(len(bnd_times)):
            fid.writelines( " " + str(bnd_times[i]))
        fid.writelines("\n")
        fid.close()
