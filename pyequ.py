import wave
import pyaudio
from multiprocessing import Process, Queue, Value, Manager, freeze_support
import time

from signal_proc import processChunk


# Process that reads chunks to fill a 5 block list
def blockReader(controlDictionary, outputQueue):
    while not controlDictionary["endOfProgramBool"]:
        if not controlDictionary["endOfMusic"]:
            wavFile = openWavFile(controlDictionary["wavName"])

            chunk = wavFile.readframes(controlDictionary["chunkSize"])
            outputQueue.put(chunk)

            while chunk:
                if controlDictionary["endOfMusic"]:
                    break
                while outputQueue.full():
                    pass
                chunk = wavFile.readframes(controlDictionary["chunkSize"])
                outputQueue.put(chunk)

            #controlDictionary["endOfMusic"] = True
        time.sleep(1)


# Process that processes blocks read and save in another list
def blockProcessor(controlDictionary, inputQueue, outputQueue):
    while not controlDictionary["endOfProgramBool"]:
        while not inputQueue.empty():
            block = inputQueue.get()

            processedBlockWithSamples = processChunk(block, controlDictionary["chunkSize"])

            while outputQueue.full():
                time.sleep(0.1)
            outputQueue.put(processedBlockWithSamples)
        time.sleep(1)


def openWavFile(wavName):
    wavFile = wave.open(wavName, "rb")
    return wavFile


def prepareStream(wavFile, pyaud, chunkSize):
    stream = pyaud.open(
        format=pyaud.get_format_from_width(wavFile.getsampwidth()),
        channels=1,  # for whatever reason, 2 channels don't work
        rate=int(wavFile.getframerate() * 4),  # the default framerate too is bugged
        frames_per_buffer=chunkSize,
        output=True
        )
    return stream

# Process that executes blocks already processed
def soundPlayer(controlDictionary, inputQueue, outputQueue):

    pyaud = pyaudio.PyAudio()
    while not controlDictionary["endOfProgramBool"]:
        if not controlDictionary["endOfMusic"]:
            stream = prepareStream(openWavFile(controlDictionary["wavName"]),
                                                        pyaud,
                                                        controlDictionary["chunkSize"]
                                                        )

            while not inputQueue.empty():
                if controlDictionary['endOfMusic']:
                    break

                if controlDictionary['playingBool']:
                    processedBlockWithSamples = inputQueue.get()
                    outputQueue.put(processedBlockWithSamples[1])
                    stream.write(processedBlockWithSamples[0])

            stream.stop_stream()
            stream.close()

        time.sleep(1)
    pyaud.terminate()


import bottle_server

def main():
    freeze_support()

    readBlocksQueue = Queue()
    processedBlocksQueue = Queue()
    sampleQueue = Queue()
    MAX_NUM_BLOCKS = 20
    manager = Manager()
    controlDictionary = manager.dict({
                                 "chunkSize": 1024,
                                 "endOfProgramBool": False,
                                 "endOfMusic": False,
                                 "playingBool": False,
                                 "wavFileNumber": 1,
                                 "wavName": "",
                                      })
    processes = [Process(target=blockReader, args=[controlDictionary, readBlocksQueue]),
                 Process(target=blockProcessor, args=[controlDictionary, readBlocksQueue, processedBlocksQueue]),
                 Process(target=soundPlayer, args=[controlDictionary, processedBlocksQueue, sampleQueue]),
                 Process(target=bottle_server.start_serv, args=[controlDictionary, readBlocksQueue, processedBlocksQueue, sampleQueue])]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


# Execute
if __name__ == '__main__':
    main()

    # profile.run('main()')
