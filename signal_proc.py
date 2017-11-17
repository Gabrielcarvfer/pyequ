import struct
import numpy
import array

def complex_to_byte(x):
    y = bytes()
    for i in range(len(x)):
        #y += (struct.pack(">I",int(numpy.real(x[i])) % 0xFFFF)) #bigendian
        y += (struct.pack("I", int(numpy.real(x[i])) % 0xFFFF))
    return y


def lowpass(freqC, numPoints):
    for i in range(numPoints):
        pass
    pass


def highpass(freqC, numPoints):
    pass


def passband(freqC1, freqC2, numPoints):
    pass


# Calculate filter
def filter(x):
    return


# Calculate window
def window(x):
    return x


bands = [60, 120, 240, 480, 960, 1920, 3840, 7680, 15360, 30720]

def processChunk(block, chunkSize):
    # Transform input string into a list of integers and complete to a power of 2
    chunkList = array.array("H", block).tolist()
    if len(chunkList) < chunkSize:
        chunkList += ([0] * (chunkSize - len(chunkList)))

    # Transform list of integers into their fft
    chunkFft = numpy.fft.fft(chunkList)
    chunkIfft = numpy.fft.ifft(chunkFft)
    processedBlock = complex_to_byte(chunkIfft)

    #y = []
    #for band in bands:
    #    bandY = numpy.convolve(x, window() * filter(band))
    #    y += bandY
    return processedBlock