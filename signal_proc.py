import struct
import numpy
import array
bands = [60, 120, 240, 480, 960, 1920, 3840, 7680, 15360, 22000]
samplingRate = 44100
import scipy.signal as sig

def complex_to_byte(x):
    y = bytes()
    for i in range(len(x)):
        y += (struct.pack("I", int(numpy.real(x[i])) % 0xFFFF))
    return y


def lowpass(N, w):
    y = []
    for n in range(N):
    #for n in range(int(-N/2),int(N/2)):
        if n == 0:
            y.append(w/numpy.pi)
        else:
            y.append(numpy.sin(w*n)/(numpy.pi*n))
    return y


def highpass(N, w):
    y = []
    for n in range(N):
    #for n in range(int(-N/2),int(N/2)):
        if n == 0:
            y.append(1-(w/numpy.pi))
        else:
            y.append(-numpy.sin(w*n)/(numpy.pi*n))
    return y


def passband(N, w1, w2):
    y = []
    for n in range(N):
    #for n in range(int(-N/2),int(N/2)):
        if n == 0:
            y.append((w2-w1)/numpy.pi)
            #y.append(1-((w2 - w1) / numpy.pi))
        else:
            y.append((numpy.sin(w2*n)-numpy.sin(w1*n))/(numpy.pi*n))
            #y.append((numpy.sin(w1*n)-numpy.sin(w2*n))/(numpy.pi*n))

    return y

def generate_filter(j, w, N):
    filter = []

    if j == 0:
        filter = lowpass(N, w)
    elif j == len(bands) - 1:
        filter = highpass(N, w)
    else:
        filter = passband(N, w * 0.8, w * 1.2)

    return filter

def hamming(M, alpha):
    y = []
    for n in range(int(-M/2), int(M/2)):
        if n == 0:
            y.append(0)
        else:
            y.append(alpha + (1-alpha)*numpy.cos(2*numpy.pi*n/M))


    return y

windowed_filters = {}

import random
from operator import add
import matplotlib.pyplot as plt
def processChunk(block, chunkSize):
    global windowed_filters, samplingRate
    # Transform input string into a list of integers and complete to a power of 2
    chunkList = array.array("H", block).tolist()
    if len(chunkList) < chunkSize:
        chunkList += ([0] * (chunkSize - len(chunkList)))

    # Transform list of integers into their fft
    #chunkFft = numpy.fft.fft(chunkList)
    #chunkIfft = numpy.fft.ifft(chunkFft)
    #processedBlock = complex_to_byte(chunkIfft)
    final_signal = [0] * chunkSize
    for j in range(len(bands)):
        if bands[j] not in windowed_filters.keys():
            fs = 44100*2
            ft = bands[j]/fs
            w = 2*numpy.pi*ft
            windows = hamming(101, 0.54)
            filters = generate_filter(j, w, 101)
            #plt.plot(windows)
            #plt.show()
            #plt.plot(filters)
            #plt.show()
            #windowed_filters[j] = sig.firwin(101, cutoff=ft, window='hann')
            windowed_filters[j] = [a*b for a,b in zip(filters,windows)]
            #fft_out = numpy.fft.fft(windowed_filters[j])
            #plt.semilogy(abs(fft_out))
            #plt.show()
            #plt.scatter(x=numpy.arange(start=0, stop=2 * numpy.pi, step= (2 * numpy.pi)/101), y=abs(fft_out))
            #plt.show()
            #fft_out = numpy.fft.fft(windowed_filters[j])
            #plt.scatter(x=numpy.arange(start=0, stop=2*numpy.pi, step=(2*numpy.pi)/(chunkSize/32)), y=abs(fft_out))
            #plt.show()
            #plt.scatter(x=range(1024), y=windows)
            #plt.show()
            #plt.scatter(x = range(1024), y = filters)
            #plt.show()
            #plt.scatter(x=range(1024), y = windowed_filters[j])
            #plt.show()

        after_process = numpy.convolve(chunkList, windowed_filters[j])
        #plt.plot(chunkList)
        #plt.show()
        #plt.plot(windowed_filters[j])
        #plt.show()
        #plt.plot(after_process)
        #plt.show()
        #fft_out = numpy.fft.fft(after_process)
        #plt.scatter(x=numpy.arange(start=0, stop=2 * numpy.pi, step=(2*numpy.pi)/chunkSize), y=abs(fft_out))
        final_signal = [x+y for x, y in zip (after_process, final_signal)]
    processedBlock = complex_to_byte(final_signal)
    #processedBlock = block



    #y = []
    #for band in bands:
    #    bandY = numpy.convolve(x, window() * filter(band))
    #    y += bandY
    #samples = [1] * 12
    samples = []
    for i in range(12):
        samples.append(random.randrange(1.0, 100.0, 10.0, int))
    return [processedBlock, samples]
