__author__ = "imsparsh"
success = "DONE"
print("Importing Modules..")
from mir import *
from  mir import Pitch
import os, sys, json, time
import pyaudio
import numpy as np
import pickle
print(success)

CHANNELS = 1
CHUNK = 1024 * 2
INTERVAL = .01
RATE = 44100

class InputStream:

	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.stream = None

	def __del__(self):
		if self.p:
			self.p.terminate()

	def open_stream(self):
		self.stream = self.p.open(format=pyaudio.paInt16,
								  channels=CHANNELS,
								  rate=RATE,
								  input=True,
								  output=False,
								  frames_per_buffer=CHUNK)

	def close_stream(self):
		self.stream.close()

	def listen_recognise(self):
		if not self.stream:
			raise Exception('Stream is closed.')
		while True:
			string_audio_data = self.stream.read(CHUNK)
			audio_data = np.fromstring(string_audio_data, dtype=np.int16)
			audio_data = audio_data.astype('float32') / 32767.0
			audioFile = audio_data.view(AudioFile)
			
                        audioFile.sampleRate = RATE
                        audioFile.channels = 1
                        audioFile.format = pyaudio.paFloat32
			recognise(audioFile)
			
			time.sleep(INTERVAL)

def calc_frequency(audio):
    frames = audio.frames(1024)
    spectra = frames[0].spectrum()
    frequency = Pitch.getFrequency(spectra)
    return frequency

def find_closest(valList, target):
    #valList must be sorted
    minV, maxV = 0.0, 9999999.999999
    for val in valList:
        maxV = val
        if val > target:
            break
        minV = val
    if abs(maxV - target) > abs(minV - target):
        return minV
    else:
        return maxV
        

def recognise(audio):
    frequency = calc_frequency(audio)
    closestFrequency = find_closest(frequencyList, frequency)
    if closestFrequency not in frequencyList:
        note = "Rest"
    else:
        note = frequencyDict[str(closestFrequency)]
    print note
    
def run():
    global frequencyDict, frequencyList
    print("")
    print("Loading pickle")
    pk = open('frequencyDict.pickle',"rb")
    frequencyDict = pickle.load(pk)
    pk.close()
    partialFreq = frequencyDict.keys()
    frequencyList = list()
    [frequencyList.append(float(item)) for item in partialFreq]
    frequencyList = sorted(frequencyList)
    print(success)
    I = InputStream()
    I.open_stream()
    I.listen_recognise()

if __name__ == "__main__":
    run()
