__author__ = 'imsparsh'

# http://www.phy.mtu.edu/~suits/notefreqs.html
# Physics of Music - Notes
# Frequencies for equal-tempered scale
# Speed of sound = 345 m/s = 1130 ft/s = 770 miles/hr
# Note Frequency (Hz)  Wavelength (cm)

import os, sys

def frequencyDict(scale):
    notefreqs = list() # list for complete info of each note in dict()
    frequencyDict = dict() # maps frequency to note
    notes = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    # scale for A4: 440.0 hz, downscale to 57 for C0
    exponent = -57
    for ndx in range(0,9):
        for note in notes:
            frequency = (1.059463094359 ** exponent) * scale
            exponent += 1
            freqDict = dict()
            if '#' in note:
                noteSplit = note.split('/')
                freqDict['note'] = noteSplit[0]+str(ndx)+'/'+noteSplit[1]+str(ndx)
                frequencyDict[str(frequency)] = str(noteSplit[0]+str(ndx)+'/'+noteSplit[1]+str(ndx))
            else:
                freqDict['note'] = note+str(ndx)
                frequencyDict[str(frequency)] = str(note+str(ndx))
            freqDict['frequency'] = frequency
            notefreqs.append(freqDict)
    return notefreqs, frequencyDict

def main():
    import pickle
    notefreqs, freqDict = frequencyDict(440.0)
    freq = open('frequency.pickle','wb')
    pickle.dump(notefreqs, freq)
    freq.close()
    freq = open('frequencyDict.pickle','wb')
    pickle.dump(freqDict, freq)
    freq.close()

if __name__ == "__main__":
    #main()
