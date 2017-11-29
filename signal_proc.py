import struct
import numpy
import scipy.signal as sig
import random
import matplotlib.pyplot as plt
from multiprocessing import Pool

#bands = [27.5,
#         55,
#         110,
#         220,
#         440,
#         880,
#         1760,
#         3520,
#         7040,
#         14080,
#         ]
bands = [32,
         64,
         125,
         250,
         500,
         1000,
         2000,
         4000,
         8000,
         16000,
         ]


windowed_filters = {}
windowed_filters_fft = {}
overlapped_chunks = {}

max16bitVal = 65535/2

filler = numpy.asarray([0.0] * 4900)


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

def generate_filter(j, w, N):
    global bands, windowed_filters

    if j not in windowed_filters.keys():
        if j == 0:
            filter = lowpass(N, w)
        elif j == len(bands) - 1:
            filter = highpass(N, w)
        else:
            filter = passband(N, w * 0.65, w * 1.55)
        windowed_filters[j] = filter
        windowed_filters_fft[j] = numpy.fft.fft(filter)
    return

def hamming(M, alpha):
    y = []
    for n in numpy.arange(M):
    #for n in range(int(-M/2), int(M/2)):
        if n == 0:
            y.append(1)
        else:
            y.append(alpha + (1-alpha)*numpy.cos(2*numpy.pi*n/M))
    return y


def filter_channels(band, chunk, gain=1):
    global windowed_filters, windowed_filters_fft
    #Linear convolution -> generates noise because of blocking
    #return numpy.multiply(numpy.convolve(windowed_filters[band], [x[channel] for x in chunk[:]]), gain)

    #Circular convolve with FFT, using with overlap and add
    left_filtered  = numpy.multiply(numpy.convolve(windowed_filters[band], [x[0] for x in chunk[:]], mode='full'), gain)
    right_filtered = numpy.multiply(numpy.convolve(windowed_filters[band], [x[1] for x in chunk[:]], mode='full'), gain)

    return [ left_filtered[:len(chunk)], #First N parts
            right_filtered[:len(chunk)],
             left_filtered[len(chunk):len(left_filtered)], #Part that is going to be overlapped on next block
            right_filtered[len(chunk):len(right_filtered)]
            ]



def filter_band(j, bands, nyquistFrequency, chunk, gainTable):
    ft = bands[j] / nyquistFrequency
    w = 2 * numpy.pi * ft
    M = 100

    # Se filtro da banda ainda não foi calculado, calcule
    generate_filter(j, w, M + 1)  # sig.firwin(M+1, cutoff=ft, window='hann')
    #sig.freqz(windowed_filters)

    # Processa canal esquerdo e direito
    filtered_band_and_overlaps  = filter_channels(band=j, chunk=chunk, gain=gainTable[j])

    # Envia band processada para fila
    return filtered_band_and_overlaps #after_process


from multiprocessing import Queue, Process
def processChunk(block, chunkSize, samplingRate, gainTable):
    global windowed_filters, overlapped_chunks

    # Preenche ultimo bloco com zeros para manter tamanho
    if len(block) < chunkSize:
        chunk = numpy.concatenate((block, numpy.asarray([(0, 0)] * (chunkSize-len(block)))))
    else:
        chunk = block

    if len(overlapped_chunks) == 0:
        for j in range(len(bands)):
            overlapped_chunks[j] = numpy.asarray([[0]*chunkSize,[0]*chunkSize])

    # Frequência de Nyquist
    fs = samplingRate / 2
    final_signal = []
    result = []

    # Aplica filtro para cada banda
    for j in numpy.arange(len(bands)):
        res = filter_band(j, bands, fs, chunk, gainTable)
        resulting_left  = numpy.add(res[0], overlapped_chunks[j][0])
        resulting_right = numpy.add(res[1], overlapped_chunks[j][1])
        overlapped_chunks[j][0] = numpy.concatenate((res[2], filler))
        overlapped_chunks[j][1] = numpy.concatenate((res[3], filler))
        result.append([resulting_left,resulting_right])

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

    #if valmaxright > max16bitVal:
    #    adjust = (max16bitVal / valmaxright)
    #    for x in numpy.arange(len(final_signal[1])):
    #        final_signal[1][x] *= adjust

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
    return [processedBlock, samples], after_process
