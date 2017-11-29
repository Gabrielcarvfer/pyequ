import wave
import pyaudio
from multiprocessing import Process, Queue, Value, Manager, freeze_support
import time
import scipy.io.wavfile as wavfile
import numpy

from signal_proc import processChunk


# Process that reads chunks to fill a 5 block list
def blockReader(controlDictionary, outputQueue):
    while not controlDictionary["endOfMusic"]:

        sr, data = wavfile.read(controlDictionary["wavName"], "r")
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
    while not controlDictionary["endOfMusic"] or not inputQueue.empty():
        while not inputQueue.empty():
            block = inputQueue.get()

            processedBlockWithSamples, afterProcess = processChunk(block, controlDictionary["chunkSize"], controlDictionary["samplingRate"], gainTable)
            outputData += afterProcess
            while outputQueue.full():
                time.sleep(0.1)
            outputQueue.put(processedBlockWithSamples)
        time.sleep(5)

    wavfile.write("output.wav", 44100, numpy.asarray(outputData,dtype=numpy.int16))
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

    pyaud = pyaudio.PyAudio()
    inputWav = openWavFile(controlDictionary["wavName"])
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


if __name__ == '__main__':
    freeze_support()
    def main():
        MAX_NUM_BLOCKS = 300
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
                                     "wavFileNumber": 3,
                                     "wavName": "samples/chilly_sample.wav",
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

    import profile
    # Execute

    main()

    #profile.run('main()')
