import struct
import numpy
import array
bands = [55,
         110,
         220,
         440,
         880,
         1760,
         3520,
         7040,
         14080,
         18065]

from multiprocessing import Process, Queue

import scipy.signal as sig

max16bitVal = 65535/2

def plot_signals(sig1, sig2, samples):
    plt.subplot(2, 1, 1)
    plt.plot(sig1[:samples])
    plt.subplot(2, 1, 2)
    plt.plot(sig2[:samples])
    plt.show()
    return


def complex_to_byte(x):
    y = bytes()
    for i in range(len(x)):
        y += (struct.pack("I", int(x[i][0]) % 0xFFFF))
        y += (struct.pack("I", int(x[i][1]) % 0xFFFF))
    return y


def lowpass(N, w):
    y = []
    for n in range(N):
        if n == 0:
            y.append(w/numpy.pi)
        else:
            y.append(numpy.sin(w*n)/(numpy.pi*n))
    return y

def highpass(N, w):
    y = []
    for n in range(N):
        if n == 0:
            y.append(1-(w/numpy.pi))
        else:
            y.append(-numpy.sin(w*n)/(numpy.pi*n))
    return y

def passband(N, w1, w2):
    y = []
    for n in range(N):
        if n == 0:
            y.append((w2-w1)/numpy.pi)
            #y.append(1-((w2 - w1) / numpy.pi))
        else:
            y.append((numpy.sin(w2*n)-numpy.sin(w1*n))/(numpy.pi*n))
            #y.append((numpy.sin(w1*n)-numpy.sin(w2*n))/(numpy.pi*n))

    return y

def generate_filter(j, w, N):
    global bands
    filter = []

    if j == 0:
        filter = lowpass(N, w)
    elif j == len(bands) - 1:
        filter = highpass(N, w)
    else:
        filter = passband(N, w * 0.75, w * 1.25)

    return filter

def hamming(M, alpha):
    y = []
    for n in range(M):
    #for n in range(int(-M/2), int(M/2)):
        if n == 0:
            y.append(1)
        else:
            y.append(alpha + (1-alpha)*numpy.cos(2*numpy.pi*n/M))


    return y

windowed_filters = {}


def filter_channel(filter, chunk, channel, gain):
    return sig.convolve(filter, [x[channel] for x in chunk[:]]) * (1 + gain)

import random
from operator import add
import matplotlib.pyplot as plt
def processChunk(block, chunkSize, samplingRate, gainTable):
    global windowed_filters

    # Preenche ultimo bloco com zeros para manter tamanho
    if len(block) < chunkSize:
        chunk = numpy.concatenate((block, numpy.asarray([(0, 0)] * (chunkSize-len(block)))))
    else:
        chunk = block

    final_signal = [(0, 0)] * chunkSize

    # Frequência de Nyquist
    fs = samplingRate / 2

    # Aplica filtro para cada banda
    for j in range(len(bands)):
        ft = bands[j] / fs
        w = 2 * numpy.pi * ft
        M = 100

        # Se filtro da banda ainda não foi calculado, calcule
        if j not in windowed_filters.keys():
            windowed_filters[j] = generate_filter(j, w, M+1)#sig.firwin(M+1, cutoff=ft, window='hann')
            sig.freqz(windowed_filters[j])

        left = Queue()
        right = Queue()

        # Processa canal esquerdo e direito
        left_channel = filter_channel(windowed_filters[j], chunk, 0, gainTable[j])
        right_channel = filter_channel(windowed_filters[j], chunk, 1, gainTable[j])

        # Junta canais
        after_process = []
        for x,y in zip(left_channel, right_channel):
                after_process.append((x, y))

        # Plota sinal de entrada e parcial processado
        #plot_signals(chunk, after_process, 250)

        # Soma dados parciais no container final, com os dois canais interpostos
        if j == 0:
            final_signal = after_process
            #plot_signals(chunk, after_process, 250)
        else:
            fsig = final_signal
            final_signal = numpy.add(fsig, after_process)

        pass

    # Normalize signal
    val1 = max([abs(x[0]) for x in final_signal[:]])
    val2 = max([abs(x[1]) for x in final_signal[:]])

    if val1 > max16bitVal or val2 > max16bitVal:
        fsig = final_signal
        final_signal = []
        for x in fsig[:]:
            final_signal.append((int(x[0]*max16bitVal/val1), int(x[1]*max16bitVal/val2)))

    # Plota sinais de entrada e saída
    #plot_signals(chunk, final_signal, 1000)

    # Transforma array em stream wav
    processedBlock = complex_to_byte(final_signal)

    #y = []
    #for band in bands:
    #    bandY = numpy.convolve(x, window() * filter(band))
    #    y += bandY
    #samples = [1] * 12
    samples = []
    for i in range(10):
            samples.append(random.randrange(1.0, 100.0, 10.0, int))
    return [processedBlock, samples]
