import subprocess
import threading
import queue
import ffmpeg
import time
import json

AUDIO_SERVER = "pulse"

class AudioManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.endFlag = False
        self.playFlag = False
        self.buffer = queue.Queue()

    def getId3Tags(self, data):
        probeCommand = f"ffprobe -print_format json=compact=1 -show_format -loglevel quiet -i -".split(" ")
        probeProcess = subprocess.Popen(probeCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        probeProcess.stdin.write(data)
        out, err = probeProcess.communicate()
        result = json.loads(out.decode("utf-8"))
        print(result)
        if "tags" in result["format"]:
            return result["format"]["tags"]
        else:
            return {"title": "No title", "artist": "No artist"}


    def stop(self):
        self.endFlag = True
        self.killAudioPipeline()
        while self.is_alive():
            time.sleep(1)

    def pushData(self, data):
        print("Received Data")
        self.buffer.put(data)
        if not self.playFlag:
            self.playFlag = True
            self.start()

    def startAudioPipeline(self):
        # In my personal setup, multiple network attached pulseserver are running over the network.
        # The unit running this code does not provide audio output by itself.
        # Restarting pulseaudio ensures correct detection of network attached pulseservers
        # TODO: Add general audio server config 
        subprocess.run("systemctl restart pulseaudio.service".split(" "))
        subprocess.run("pactl set-default-sink 1".split(" "))
        self.audioProcess = (ffmpeg
            .input("pipe:")
            .filter("dynaudnorm", p=0.71, m=100, s=12, g=15)
            .output("pipe:", format="wav")
            .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=False)
        )
        self.playerProcess = subprocess.Popen(f"aplay -q -t wav --fatal-errors -D {AUDIO_SERVER}".split(" "), 
            stdin=self.audioProcess.stdout)

    def run(self):
        while not self.endFlag:
            if(self.pipelineAlive()):
                if(self.buffer.qsize() > 0):
                    self.audioProcess.stdin.write(self.buffer.get())
                else:
                    time.sleep(1)
            else:
                self.endFlag = True

    def killAudioPipeline(self):
        try:
            self.audioProcess.kill()
            self.audioProcess = None
        except Exception:
            # TODO: Add better handling for stopping the audio pipeline
            pass

    def pipelineAlive(self):
        try:
            return self.audioProcess.poll() == None and self.playerProcess.poll() == None
        except Exception:
            return False
