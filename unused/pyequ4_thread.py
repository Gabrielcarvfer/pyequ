import wave
import pyaudio
import array
import numpy
from threading import Thread, Condition
import time
import struct
import scipy
import profile


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


def processChunk(x):
    y = []
    for band in bands:
        bandY = numpy.convolve(x, window() * filter(band))
        y += bandY
    return



chunkSize = 32768
wavFileName = "chilly_sample.wav"
wavFile = wave.open(wavFileName, "rb")
readBlockCondition = Condition()
processBlockCondition = Condition()
readBlocksList = []
processedBlocksList = []
MAX_NUM_BLOCKS = 200

# Process that reads chunks to fill a 5 block list
def blockReader():
    global readBlocksList, wavFile, readBlockCondition, endOfProgram

    readBlockCondition.acquire()
    chunk = wavFile.readframes(chunkSize)
    readBlocksList.append(chunk)
    readBlockCondition.release()

    while chunk:
        readBlockCondition.acquire()
        while len(readBlocksList) >= MAX_NUM_BLOCKS:
            readBlockCondition.wait()
        chunk = wavFile.readframes(chunkSize)
        readBlocksList.append(chunk)
        readBlockCondition.release()

    endOfProgram = True


#Process that processes blocks read and save in another list
def blockProcessor():
    global endOfProgram, readBlocksList, processedBlocksList, processBlockCondition,  readBlockCondition

    while not endOfProgram or len(readBlocksList) > 1:
        readBlockCondition.acquire()
        while len(readBlocksList) < 1:
            readBlockCondition.wait()
        block = readBlocksList[0]
        del readBlocksList[0]
        readBlockCondition.release()

        # Transform input string into a list of integers and complete to a power of 2
        chunkList = array.array("H", block).tolist()
        if len(chunkList) < chunkSize:
            chunkList += ([0] * (chunkSize - len(chunkList)))

        # Transform list of integers into their fft
        chunkFft = numpy.fft.fft(chunkList)
        chunkIfft = numpy.fft.ifft(chunkFft)
        chunkIfftBytes = complex_to_byte(chunkIfft)


        processBlockCondition.acquire()
        while len(processedBlocksList) >= MAX_NUM_BLOCKS:
            processBlockCondition.wait()
        processedBlocksList.append(chunkIfftBytes)
        processBlockCondition.notify()
        processBlockCondition.release()

    pass


# Process that executes blocks already processed
def soundPlayer():
    global processedBlocksList, endOfProgram, stream, pyaud, wavFile, processBlockCondition

    pyaud = pyaudio.PyAudio()
    stream = pyaud.open(format=pyaud.get_format_from_width(wavFile.getsampwidth()),
                        channels=wavFile.getnchannels(),
                        rate=wavFile.getframerate(),
                        output=True
                        )

    while not endOfProgram or len(processedBlocksList) > 0:
        processBlockCondition.acquire()
        if len(processedBlocksList) < 1:
            processBlockCondition.wait()

        block = processedBlocksList[0]
        del processedBlocksList[0]

        processBlockCondition.notify()
        processBlockCondition.release()

        stream.write(block)

    stream.stop_stream()
    stream.close()
    pyaud.terminate()


endOfProgram = False


def main():
    global wavFileName, wavFile, readBlockCondition, processBlockCondition



    processes = [Thread(target=blockReader),
                 Thread(target=blockProcessor),
                 Thread(target=soundPlayer)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


# Execute
if __name__ == '__main__':

    main()

    #profile.run('main()')