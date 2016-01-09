"""
Compute onset times from time-domain audio data
Spectra are computed as necessary
Supported methods:
- Time-domain: energy
- Spectral: flux
"""
from mir import Energy
from mir import SpectralFlux

import numpy
from numpy import NaN, Inf, arange, isscalar, array, asarray

import matplotlib.pyplot as plt

def onsets(audioData, method='energy'):
	onsets = []
	if method == 'energy':
		onsets =  onsetsByEnergy(audioData)
	elif method == 'flux':
		onsets = onsetsByFlux(audioData)

	return onsets


def onsetsByEnergy(audioData, frameSize = 512, threshold = 1):
	"""
	Compute onsets by using dEnergy (time-domain)
	"""
	e = Energy.energy(audioData, frameSize)
	dE = Energy.dEnergy(audioData, frameSize)
	peaks = peakPicking(dE, 2048, threshold)

	return peaks

def onsetsByFlux(audioData, frameSize = 1024):
	"""
	Compute onsets by using spectral flux
	"""
	frames = audioData.frames(frameSize)

	# Compute the spectra of each frame
	spectra = [f.spectrum() for f in frames]

	# Compute the spectral flux
	flux = SpectralFlux.spectralFlux(spectra, rectify=True)

	peaks = peakPicking(flux, windowSize = 10, threshold = 1e6)
	peaks = [frameSize * p for p in peaks]

	return peaks

def peakPicking(onsets, windowSize = 1024, threshold = 1):

	peaks = []
	
	peaks = peaksAboveAverage(onsets, windowSize)
	return peaks

def peaksAboveAverage(data, windowSize):
	"""
	Find peaks by the following method:
	- Compute the average of all the data
	- Using a non-sliding window, find the max within each window
	- If the windowed max is above the average, add it to peaks
	"""

	data = numpy.array(data)

	peaks = []

	dataAverage = numpy.average(data)
	dataAverage = dataAverage * 1

	slideAmount = windowSize / 2

	start = 0
	end = windowSize
	while start < len(data): 
		#print "Start: " + str(start)
		#print "End:   " + str(end)
		windowMax = data[start:end].max()  
		windowMaxPos = data[start:end].argmax()

		if windowMax > dataAverage:
			if (start + windowMaxPos) not in peaks:
				peaks.append(start + windowMaxPos)

		start = start + slideAmount
		end = end + slideAmount
	
	return peaks
