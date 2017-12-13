import wave
import pyaudio
from multiprocessing import Process, Queue, Value, Manager, freeze_support
import time
import scipy.io.wavfile as wavfile
import numpy

from signal_proc import processChunk


# Process that reads chunks to fill a 5 block list
def blockReader(controlDictionary, outputQueue):
    while (not controlDictionary["musicSelected"]):
        continue

    while not controlDictionary["endOfMusic"]:

        sr, data = wavfile.read(controlDictionary["wavName"]+".wav", "r")
        controlDictionary["samplingRate"] = sr
        chunksList = numpy.split(data, [i*controlDictionary["chunkSize"] for i in range(1,int(len(data)/controlDictionary["chunkSize"])+1)])
        for chunk in chunksList:
            outputQueue.put(chunk)

        time.sleep(1)
        controlDictionary["endOfMusic"] = True

    return


# Process that processes blocks read and save in another list
def blockProcessor(controlDictionary, inputQueue, outputQueue, gainTable):
    outputData = []
    #inputData = []
    while (not controlDictionary["musicSelected"]):
        continue

    while not controlDictionary["endOfMusic"] or not inputQueue.empty():
        while not inputQueue.empty():
            block = inputQueue.get()
            #inputData += list(block)
            processedBlockWithSamples, afterProcess = processChunk(block, controlDictionary["chunkSize"], controlDictionary["samplingRate"], gainTable)
            outputData += afterProcess
            while outputQueue.full():
                time.sleep(0.1)
            outputQueue.put(processedBlockWithSamples)
        time.sleep(5)
    #Save audio file
    wavfile.write(controlDictionary["wavName"]+"_output.wav", 44100, numpy.asarray(outputData, dtype=numpy.int16))
    return


def openWavFile(wavName):
    wavFile = wave.open(wavName, "rb")
    return wavFile


def prepareStream(wavFile, pyaud, chunkSize):
    stream = pyaud.open(
        format=pyaud.get_format_from_width(wavFile.getsampwidth()),
        channels=1,  # for whatever reason, 2 channels don't work
        rate=int(wavFile.getframerate()*4),  # the default framerate too is bugged
        frames_per_buffer=chunkSize,
        output=True
        )
    return stream


# Process that executes blocks already processed
def soundPlayer(controlDictionary, inputQueue, outputQueue, readBlocksQueue):
    while( not controlDictionary["musicSelected"]):
        continue

    pyaud = pyaudio.PyAudio()
    inputWav = openWavFile(controlDictionary["wavName"]+".wav")
    stream = prepareStream(inputWav,
                                                pyaud,
                                                controlDictionary["chunkSize"]
                                                )
    while not controlDictionary["endOfMusic"] or not inputQueue.empty() or not readBlocksQueue.empty():
        while not inputQueue.empty() or not readBlocksQueue.empty():
            if controlDictionary['playingBool']:
                processedBlockWithSamples = inputQueue.get()
                outputQueue.put(processedBlockWithSamples[1])
                stream.write(processedBlockWithSamples[0])
            else:
                continue
        time.sleep(10)
    stream.stop_stream()
    stream.close()

    time.sleep(1)
    pyaud.terminate()
    return



def main():
    MAX_NUM_BLOCKS = 5
    readBlocksQueue = Queue(maxsize=MAX_NUM_BLOCKS)
    processedBlocksQueue = Queue(maxsize=MAX_NUM_BLOCKS)
    sampleQueue = Queue(maxsize=MAX_NUM_BLOCKS)
    manager = Manager()
    controlDictionary = manager.dict({
                                 "chunkSize": 5000,
                                 "samplingRate": 44100,
                                 "endOfProgramBool": False,
                                 "endOfMusic": False,
                                 "playingBool": False,
                                 "musicSelected": False,
                                 "wavName": "samples/penguin",
                                      })

    gainTable = manager.list([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    import equi

    processes = [Process(target=blockReader, args=[controlDictionary, readBlocksQueue]),
                 #Process(target=blockProcessor, args=[controlDictionary, readBlocksQueue, processedBlocksQueue, gainTable]),
                 Process(target=soundPlayer, args=[controlDictionary, processedBlocksQueue, sampleQueue, readBlocksQueue]),
                 Process(target=equi.qt_load, args=[gainTable, sampleQueue, controlDictionary])
                 ]

    for process in processes:
        process.start()

    blockProcessor(controlDictionary, readBlocksQueue, processedBlocksQueue, gainTable)

    for process in processes:
        process.join()

    return



def fftFile(file):
    inputSr, inputData = wavfile.read(file, "r")
    if (len(inputData) < 11510000):
        temp = inputData
        filler = numpy.asarray([0.0, 0.0] * (11510000 - len(inputData)))
        inputData = numpy.concatenate(temp, filler)
    leftChannelIn = [x[0] for x in inputData[:]]
    hIn = numpy.fft.fft(leftChannelIn)
    return hIn


def checkDiff(wavFile):
    inputSr, inputData = wavfile.read(wavFile + ".wav", "r")
    outputSr, outputData = wavfile.read(wavFile + "_output_nohamming.wav", "r")
    diffSr, diffData = wavfile.read(wavFile + "_diff_nohamming.wav", "r")

    blockSize = 5000

    chunksInput = numpy.split(inputData, [i * blockSize for i in range(1, int(len(inputData) / blockSize) + 1)])
    chunksOutput = numpy.split(outputData, [i * blockSize for i in range(1, int(len(outputData) / blockSize) + 1)])
    chunksDiff = numpy.split(diffData, [i * blockSize for i in range(1, int(len(diffData) / blockSize) + 1)])
    for i in range(len(chunksInput)):
        leftChannelIn = [x[0] for x in chunksInput[i][:]]
        leftChannelOut = [x[0] for x in chunksOutput[i][:]]
        leftChannelDiff = [x[0] for x in chunksDiff[i][:]]

        # Plot difference between input and output data
        import scipy.signal as sig

        w = numpy.fft.fftfreq(blockSize, d=1 / 22050)
        hIn = numpy.fft.fft(leftChannelIn)
        hOut = numpy.fft.fft(leftChannelOut)
        hDiff = numpy.fft.fft(leftChannelDiff)

        # w = numpy.fft.fftfreq(11510000, d=1 / 22050)
        # inputData = []
        #
        # from multiprocessing import Pool
        # p = Pool(3)
        # ffts = p.starmap(fftFile, [[wavFile+".wav"], [wavFile+"_output.wav"], [wavFile+"_diff.wav"]])

        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.title('Signal spectrum')
        ax1 = fig.add_subplot(111)
        plt.plot(numpy.abs(w), 20 * numpy.log10(abs(hIn)), 'b')
        plt.plot(numpy.abs(w), 20 * numpy.log10(abs(hOut)), 'g')
        plt.plot(numpy.abs(w), 20 * numpy.log10(abs(hDiff)), 'r')
        plt.ylabel('Amplitude [dB]', color='b')
        plt.xlabel('Frequency [Hz]')


if __name__ == '__main__':
    freeze_support()
    #main()
    checkDiff("./samples/luke")



