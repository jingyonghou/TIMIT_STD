#!/usr/bin/python
# oupput the time duration of a list of wav files in totally
import sys
from scipy.io.wavfile import read

if len(sys.argv) < 2:
	print "USEGE: filelist"
	exit(1)
filename = sys.argv[1]
fid = open(filename)
filelist = fid.readlines()
fid.close()

time_s = 0

for f in filelist:
	rate,data = read(f.strip()+'.wav')
	time_s += len(data)/float(rate)

print time_s
	
