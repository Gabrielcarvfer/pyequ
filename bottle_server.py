from bottle import get, route, post, template, run, request, redirect
import json
samples = [1] * 12

readBlocksQueue = []
processedBlocksQueue = []
sampleQueue = []
controlDictionary = []
musicSamples = ["aha", "america", "chilly", "chilly_sample", "cutcopy", "duran", "lambert", "newell", "packer"]


@get("/")
def home():
    config_width = 10
    config_speed = 5
    return template('equalizer', config_width=config_width, config_speed=config_speed)


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
    controlDictionary['cleanBool'] = False
    redirect("/")

from pyequ import openWavFile, prepareStream


@post("/play")
def postActions():
    global controlDictionary, readBlocksQueue, processedBlocksQueue, sampleQueue, musicSamples
    if not controlDictionary:
        redirect("/")

    if request.forms.get('music') == controlDictionary['wavFileNumber']:
        controlDictionary['playingBool'] = True

    else:
        # Pause music playing
        controlDictionary['endOfMusic'] = True
        controlDictionary['playingBool'] = False

        # Flush queues
        while not readBlocksQueue.empty():
            readBlocksQueue.get()

        while not processedBlocksQueue.empty():
            processedBlocksQueue.get()

        while not sampleQueue.empty():
                sampleQueue.get()

        # When all processes have blocks flushed, then set the new file to play
        musNum = request.forms.get('music')
        if musNum == None:
            musNum = 0
        controlDictionary['wavFileNumber'] = musNum
        controlDictionary['wavName'] = ("samples/%s.wav" % musicSamples[int(musNum)])

        controlDictionary["endOfMusic"] = False
        controlDictionary['playingBool'] = True

    redirect('/')

def start_serv(globalControlDictionary, globalReadBlocksQueue, globalProcessedBlocksQueue, globalSampleQueue):
    global readBlocksQueue, processedBlocksQueue, sampleQueue, controlDictionary
    readBlocksQueue = globalReadBlocksQueue
    processedBlocksQueue = globalProcessedBlocksQueue
    sampleQueue = globalSampleQueue
    controlDictionary = globalControlDictionary

    run(host='localhost', port=8080)


