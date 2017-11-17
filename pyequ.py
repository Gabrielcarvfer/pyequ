import wave
import pyaudio
from multiprocessing import Process, Queue, Value, freeze_support
import time

from signal_proc import processChunk


# Process that reads chunks to fill a 5 block list
def blockReader(endOfProgram, chunkSize, wavFileName, outputQueue):
    wavFile = wave.open(wavFileName, "rb")

    chunk = wavFile.readframes(chunkSize)
    outputQueue.put(chunk)

    while chunk:
        while outputQueue.full():
            pass
        chunk = wavFile.readframes(chunkSize)
        outputQueue.put(chunk)

    endOfProgram = True


# Process that processes blocks read and save in another list
def blockProcessor(endOfProgram, chunkSize, inputQueue, outputQueue):
    while not endOfProgram or not inputQueue.empty():
        block = inputQueue.get()

        processedBlock = processChunk(block, chunkSize)

        while outputQueue.full():
            time.sleep(0.1)
        outputQueue.put(processedBlock)


# Process that executes blocks already processed
def soundPlayer(endOfProgram, chunkSize, wavFileName, inputQueue):
    wavFile = wave.open(wavFileName, "rb")

    pyaud = pyaudio.PyAudio()
    stream = pyaud.open(format=pyaud.get_format_from_width(wavFile.getsampwidth()),
                        channels=1,  # for whatever reason, 2 channels don't work
                        rate=int(wavFile.getframerate() * 4),  # the default framerate too is bugged
                        frames_per_buffer=chunkSize,
                        output=True
                        )

    while not endOfProgram or not inputQueue.empty():
        block = inputQueue.get()
        stream.write(block)

    stream.stop_stream()
    stream.close()
    pyaud.terminate()


def main():
    freeze_support()
    chunkSize = 1024
    samples = ["aha",
               "america",
               "chilly",
               "chilly_sample",
               "cutcopy",
               "duran",
               "lambert",
               "newell",
               "packer"
               ]
    wavFileName = "samples/" + samples[6] + ".wav"
    readBlocksQueue = Queue()
    processedBlocksQueue = Queue()
    MAX_NUM_BLOCKS = 20

    endOfProgram = Value('b', False)
    processes = [Process(target=blockReader, args=(endOfProgram, chunkSize, wavFileName, readBlocksQueue)),
                 Process(target=blockProcessor, args=(endOfProgram, chunkSize, readBlocksQueue, processedBlocksQueue)),
                 Process(target=soundPlayer, args=(endOfProgram, chunkSize, wavFileName, processedBlocksQueue))]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


# Execute
if __name__ == '__main__':
    main()

    # profile.run('main()')
