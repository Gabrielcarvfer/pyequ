import wave
import pyaudio
import array
import numpy
from multiprocessing import Process, Condition, freeze_support, Queue, Value
import time
import struct
import scipy
import profile

freeze_support()
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
        bandY = numpy.convolve(x, window(x) * filter(band))
        y += bandY
    return

MAX_NUM_BLOCKS = 5

wavFileName= "chilly_sample.wav"




# Process that reads chunks to fill a 5 block list
def blockReader(sharedData):
    global endOfProgram

    chunk = sharedData["wavFile"].readframes(sharedData["chunkSize"])
    sharedData["readBlocksList"].put(chunk)
    written = False

    while chunk:
        while not written:
            if not sharedData["readBlocksList"].full():
                sharedData["readBlocksList"].put(chunk)
                written = True
            else:
                time.sleep(1)
        chunk = sharedData["wavFile"].readframes(sharedData["chunkSize"])
        written = False

    endOfProgram = True


# Process that processes blocks read and save in another list
def blockProcessor(sharedData):
    global endOfProgram

    while not endOfProgram or not sharedData["readBlockCondition"].empty():
        block = sharedData["readBlockList"].get()

        # Transform input string into a list of integers
        chunkList = array.array("H", block).tolist()
        if len(chunkList) < sharedData["chunkSize"]:
            chunkList += ([0] * (sharedData["chunkSize"] - len(chunkList)))

        # Transform list of integers into their fft
        chunkFft = numpy.fft.fft(chunkList)
        chunkIfft = numpy.fft.ifft(chunkFft)
        chunkIfftBytes = complex_to_byte(chunkIfft)

        while sharedData["processedBlocksList"].full():
            time.sleep(1)
        sharedData["processedBlocksList"].put(chunkIfftBytes)


# Process that executes blocks already processed
def soundPlayer(sharedData):
    global endOfProgram

    pyaud = pyaudio.PyAudio()
    stream = pyaud.open(format=pyaud.get_format_from_width(sharedData["wavFile"].getsampwidth()),
                        channels=sharedData["wavFile"].getnchannels(),
                        rate=sharedData["wavFile"].getframerate(),
                        output=True
                        )

    while not endOfProgram or not sharedData["processedBlocksList"].empty():
        block = sharedData["processedBlocksList"].get()

        stream.write(block)

    stream.stop_stream()
    stream.close()
    pyaud.terminate()


endOfProgram = Value('b', False)


def main():
    sharedData = {
        "chunkSize": 32768,
        "wavFile": wave.open(wavFileName, "rb"),
        "readBlockCondition": Condition(),
        "processBlockCondition": Condition(),
        "maxNumBlocks": MAX_NUM_BLOCKS,
        "readBlocksList": Queue(MAX_NUM_BLOCKS),
        "processedBlocksList": Queue(MAX_NUM_BLOCKS),
    }

    processes = [Process(target=blockReader, args=[sharedData]),
                 Process(target=blockProcessor, args=[sharedData]),
                 Process(target=soundPlayer, args=[sharedData])]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


# Execute
if __name__ == '__main__':
    freeze_support()
    main()

    #profile.run('main()')