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

            chunk = wavFile.readframes(2*controlDictionary["chunkSize"])
            outputQueue.put(chunk)

            while chunk and wavFile.tell():
                if controlDictionary["endOfMusic"]:
                    break
                while outputQueue.full():
                    pass
                chunk = wavFile.readframes(2*controlDictionary["chunkSize"])
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
        channels=2,  # for whatever reason, 2 channels don't work
        rate=int(wavFile.getframerate()),  # the default framerate too is bugged
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

def launch_player(controlDictionary, readBlocksQueue, processedBlocksQueue,  sampleQueue):

    processes = [Process(target=blockReader, args=[controlDictionary, readBlocksQueue]),
    Process(target=blockProcessor, args=[controlDictionary, readBlocksQueue, processedBlocksQueue]),
    Process(target=soundPlayer, args=[controlDictionary, processedBlocksQueue, sampleQueue]),]
    for process in processes:
        process.start()

    return processes


#import bottle_server
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

sampleQueue = []
def plotter(globalSampleQueue):
    global sampleQueue
    sampleQueue = globalSampleQueue


    def animate(frameno):
        global sampleQueue
        x = sampleQueue.get()
        n, _ = np.histogram(x, bins)#, normed=True)
        cmap = ['rosybrown',
                'red',
                'sienna',
                'gold',
                'olivedrab',
                'darkgreen',
                'darkcyan',
                'slategray',
                'navy',
                'orange',
                'darkviolet',
                'lightskyblue',
                ]
        i = 0
        for h, rect in zip(n, patches):
            rect.set_height(h)
            plt.setp(rect, 'facecolor', cmap[i])
            i += 1



    fig, ax = plt.subplots()
    x = sampleQueue.get()

    n, bins, patches = plt.hist(x, 10, alpha=0.75)

    ani = animation.FuncAnimation(fig, animate, blit=False, interval=100, repeat=False)
    plt.show()


def main():
    freeze_support()


    MAX_NUM_BLOCKS = 30000
    readBlocksQueue = Queue(maxsize=MAX_NUM_BLOCKS)
    processedBlocksQueue = Queue(maxsize=MAX_NUM_BLOCKS)
    sampleQueue = Queue(maxsize=MAX_NUM_BLOCKS)
    manager = Manager()
    controlDictionary = manager.dict({
                                 "chunkSize": 2048,
                                 "endOfProgramBool": False,
                                 "endOfMusic": False,
                                 "playingBool": True,
                                 "wavFileNumber": 3,
                                 "wavName": "samples/chilly_sample.wav",
                                      })
    processes = [Process(target=blockReader, args=[controlDictionary, readBlocksQueue]),
                 Process(target=blockProcessor, args=[controlDictionary, readBlocksQueue, processedBlocksQueue]),
                 Process(target=soundPlayer, args=[controlDictionary, processedBlocksQueue, sampleQueue]),
                 #Process(target=plotter, args=[sampleQueue])
                 ]
                 #Process(target=bottle_server.start_serv, args=[controlDictionary, readBlocksQueue, processedBlocksQueue, sampleQueue])]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    return


# Execute
if __name__ == '__main__':
    main()

    # profile.run('main()')
