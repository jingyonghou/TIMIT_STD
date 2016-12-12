#!/usr/bin/python

import sys
import numpy as np
import wave
import scipy.signal as signal

def readwave(wavFileName):
	#open the wav file
	f=wave.open(wavFileName, "rb")
	#read the pareameter of wav
	params=f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	if ((nchannels!=1) | (sampwidth!=2) | (framerate!=16000)):
		print 'the wav file may not normal:wavID '+wavFileName+' channels: '+str(nchannels)+' sampwidth:'+str(sampwidth) + ' framerate:' + str(framerate)+'\n'
	#get the wave data(bytes data)
	str_data=f.readframes(nframes)
	f.close()    
	#get the wave data(PCM data)
	if sampwidth==2:
		wave_data = np.fromstring(str_data,dtype=np.short)
	elif sampwidth==1:
		wave_data = np.framstring(str_data,dtype=np.int8)
	if nchannels==2:
		wave_data.shape=-1, 2
	wave_data=wave_data.T
	return wave_data

def writewave(wavFileName, data, nchannels, sampwidth, framerate):
	#open to write file
	f=wave.open(wavFileName, "wb")
	f.setnchannels(nchannels)
	f.setsampwidth(sampwidth)
	f.setframerate(framerate)
	#writeifle
	str_data=data.tostring()
	f.writeframes(str_data)
	f.close()

