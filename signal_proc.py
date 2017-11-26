import struct
import numpy
import scipy.signal as sig
import random
import matplotlib.pyplot as plt
from multiprocessing import Pool

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
    for n in numpy.arange(N):
        if n == 0:
            y.append(w/numpy.pi)
        else:
            y.append(numpy.sin(w*n)/(numpy.pi*n))
    return y

def highpass(N, w):
    y = []
    for n in numpy.arange(N):
        if n == 0:
            y.append(1-(w/numpy.pi))
        else:
            y.append(-numpy.sin(w*n)/(numpy.pi*n))
    return y

def passband(N, w1, w2):
    y = []
    for n in numpy.arange(N):
        if n == 0:
            y.append((w2-w1)/numpy.pi)
            #y.append(1-((w2 - w1) / numpy.pi))
        else:
            y.append((numpy.sin(w2*n)-numpy.sin(w1*n))/(numpy.pi*n))
            #y.append((numpy.sin(w1*n)-numpy.sin(w2*n))/(numpy.pi*n))

    return y
windowed_filters = {}

def generate_filter(j, w, N):
    global bands, windowed_filters

    if j not in windowed_filters.keys():
        if j == 0:
            filter = lowpass(N, w)
        elif j == len(bands) - 1:
            filter = highpass(N, w)
        else:
            filter = passband(N, w * 0.75, w * 1.25)
        windowed_filters[j] = filter
    else:
        filter = windowed_filters[j]
    return filter

def hamming(M, alpha):
    y = []
    for n in numpy.arange(M):
    #for n in range(int(-M/2), int(M/2)):
        if n == 0:
            y.append(1)
        else:
            y.append(alpha + (1-alpha)*numpy.cos(2*numpy.pi*n/M))


    return y




def filter_channel(filter, chunk, channel, gain=1):
    return numpy.multiply(sig.convolve(filter, [x[channel] for x in chunk[:]]), gain)


def filter_band(j, bands, nyquistFrequency, chunk, gainTable):
    ft = bands[j] / nyquistFrequency
    w = 2 * numpy.pi * ft
    M = 100

    # Se filtro da banda ainda não foi calculado, calcule
    windowed_filters = generate_filter(j, w, M + 1)  # sig.firwin(M+1, cutoff=ft, window='hann')
    sig.freqz(windowed_filters)

    # Processa canal esquerdo e direito
    left_channel = filter_channel(windowed_filters, chunk, 0, gainTable[j])
    right_channel = filter_channel(windowed_filters, chunk, 1, gainTable[j])

    # Junta canais
    #after_process = []
    #for x, y in zip(left_channel, right_channel):
    #    after_process.append((x, y))

    # Plota sinal de entrada e parcial processado
    # plot_signals(chunk, after_process, 250)

    # Envia band processada para fila
    return [left_channel, right_channel] #after_process


from multiprocessing import Queue, Process
def processChunk(block, chunkSize, samplingRate, gainTable):
    global windowed_filters

    # Preenche ultimo bloco com zeros para manter tamanho
    if len(block) < chunkSize:
        chunk = numpy.concatenate((block, numpy.asarray([(0, 0)] * (chunkSize-len(block)))))
    else:
        chunk = block

    # Frequência de Nyquist
    fs = samplingRate / 2
    final_signal = []
    result = []

    # Aplica filtro para cada banda
    for j in numpy.arange(len(bands)):
        result.append(filter_band(j, bands, fs, chunk, gainTable))

    samples = []
    valmaxleft = 0
    valmaxright = 0
    # Aplica filtro para cada banda
    for j in numpy.arange(len(bands)):
        # Get max audio samples
        val1 = numpy.max(numpy.absolute(result[j][0]))
        val2 = numpy.max(numpy.absolute(result[j][1]))
        samples.append(numpy.max([val1, val2]))

        # Soma dados parciais no container final, com os dois canais interpostos
        if len(final_signal) == 0:
            final_signal = result[j]
            # plot_signals(chunk, after_process, 250)
        else:
            fsig = final_signal
            final_signal = numpy.add(fsig, result[j])

    valmaxleft = numpy.max(numpy.absolute(final_signal[0]))
    valmaxright = numpy.max(numpy.absolute(final_signal[1]))

    # Normalize signal
    if valmaxleft > max16bitVal:
        adjust = (max16bitVal / valmaxleft)
        for x in numpy.arange(len(final_signal[0])):
            final_signal[0][x] *= adjust

    if valmaxright > max16bitVal:
        adjust = (max16bitVal / valmaxright)
        for x in numpy.arange(len(final_signal[1])):
            final_signal[1][x] *= adjust

    # Plota sinais de entrada e saída
    #plot_signals(chunk, final_signal, 1000)

    after_process = []
    for x,y in zip(final_signal[0], final_signal[1]):
       after_process.append((x, y))


    # Transforma array em stream wav
    processedBlock = complex_to_byte(after_process)

    # Adjust collected samples
    for j in range(len(bands)):
        samples[j] = int(samples[j]*100/max16bitVal)
    return [processedBlock, samples]
