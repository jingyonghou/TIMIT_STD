import sys

if __name__=='__main__':
    if(len(sys.argv)<3):
        print("USAGE: python " + sys.argv[0] + " boundaryFile Dir")
        exit(1)
    boundaryFile = sys.argv[1]
    fileDir = sys.argv[2]
    
    boundaryLine = open(boundaryFile).readlines()
    for line in boundaryLine:
        fields = line.strip().split()
        file_id = fields[0];
        file_name = fileDir + file_id + ".phn_num";
        fid=open(file_name, "w")
        fid.writelines(str(len(fields)-1))
        fid.close()

