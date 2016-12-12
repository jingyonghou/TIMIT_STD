import sys
import scipy.io.wavfile as wave
from numpy import fromfile

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("split.py datadir datalist")
    datadir =  sys.argv[1]
    datalist = sys.argv[2]
    sampleRate = 16000 #Hz
    fid = open(datalist)
    filenames = fid.readlines()
    fid.close()
    for filename in filenames:
        fid = open(datadir + filename.strip() + '.WAV', 'rb')
        fid.seek(1024)#skip the 1024byte header
        samples = fromfile(fid, dtype = '<h')
        fid.close()
        wave.write(datadir + filename.strip() + '.WAVNEW', sampleRate, samples)
