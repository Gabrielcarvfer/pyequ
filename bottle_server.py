from bottle import get, route, post, template, run, request, redirect, HTTPResponse
from multiprocessing import Process
from pyequ import launch_player
import json
samples = [1] * 12

readBlocksQueue = []
processedBlocksQueue = []
sampleQueue = []
controlDictionary = []
musicSamples = ["aha", "america", "chilly", "chilly_sample", "cutcopy", "duran", "lambert", "newell", "packer"]
playerProcess = None

@get("/")
def home():
    config_width = 10
    config_speed = 5
    return template('equalizer', config_width=config_width, config_speed=config_speed, music=musicSamples[controlDictionary["wavFileNumber"]])


@get("/samples")
def getSamples():
    global samples, sampleQueue

    if not sampleQueue.empty():
        samples = sampleQueue.get()

    return json.dumps({"samples": samples})


@route("/pause")
def pause(action):
    #pause
    global controlDictionary
    controlDictionary['playingBool'] = False
    redirect("/")

from pyequ import openWavFile, prepareStream

@route("/play")
@route("/play/<music>")
def postActions(music=0):
    global controlDictionary, readBlocksQueue, processedBlocksQueue, sampleQueue, musicSamples, playerProcess
    if not controlDictionary:
        redirect("/")

    if music == controlDictionary['wavFileNumber']:
        controlDictionary['playingBool'] = True

    else:
        controlDictionary['playingBool'] = False

        if playerProcess:
            playerProcess.terminate()

        # When all processes have blocks flushed, then set the new file to play
        controlDictionary['wavFileNumber'] = music
        controlDictionary['wavName'] = ("samples/%s.wav" % musicSamples[int(music)])

        playerProcess = Process(target=launch_player, args=(controlDictionary, readBlocksQueue, processedBlocksQueue, sampleQueue))
        playerProcess.daemon = True
        playerProcess.start()


        controlDictionary['playingBool'] = True

    redirect('/')

def start_serv(globalControlDictionary, globalReadBlocksQueue, globalProcessedBlocksQueue, globalSampleQueue):
    global readBlocksQueue, processedBlocksQueue, sampleQueue, controlDictionary, processes
    readBlocksQueue = globalReadBlocksQueue
    processedBlocksQueue = globalProcessedBlocksQueue
    sampleQueue = globalSampleQueue
    controlDictionary = globalControlDictionary

    run(host='localhost', port=8080)




