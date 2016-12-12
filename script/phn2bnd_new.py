import sys

if __name__=='__main__':
    if(len(sys.argv)<3):
        print("USAGE: python " + sys.argv[0] + " boundaryFile Dir")
        exit(1)
    boundaryFile = sys.argv[1]
    fileDir = sys.argv[2]
    
    boundaryLine = open(boundaryFile).readlines()
    for line in boundaryLine:
        if '[' in line:
            fields = line.strip().split()
            file_id = fields[0];
            file_name = fileDir + file_id + ".bnd_wsj";
            fid=open(file_name, "w")
            boundary = fields[3];
            fid.writelines(boundary + " ")
        else:
            fields = line.strip().split()
            boundary = fields[1];
            fid.writelines(boundary + " ")

        if ']' in line:
            fid.close()
            continue

