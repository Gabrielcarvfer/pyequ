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
    after_process = []
    for x, y in zip(left_channel, right_channel):
        after_process.append((x, y))

    # Plota sinal de entrada e parcial processado
    # plot_signals(chunk, after_process, 250)

    # Envia band processada para fila
    return after_process


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
    for j in range(len(bands)):
        result.append(filter_band(j, bands, fs, chunk, gainTable))

    #result = Pool(2).starmap(filter_band, [[j, bands, fs, chunk, gainTable] for j in range(len(bands))])
    samples = []
    # Aplica filtro para cada banda
    for j in range(len(bands)):
        # Get max audio samples
        val1 = max([abs(x[0]) for x in result[j]])
        val2 = max([abs(x[1]) for x in result[j]])
        samples.append(max(val1, val2))

        # Soma dados parciais no container final, com os dois canais interpostos
        if len(final_signal) == 0:
            final_signal = result[j]
            # plot_signals(chunk, after_process, 250)
        else:
            fsig = final_signal
            final_signal = numpy.add(fsig, result[j])

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

    # Adjust collected samples
    for j in range(len(bands)):
        samples[j] = int(samples[j]*100/max16bitVal)
    return [processedBlock, samples]
