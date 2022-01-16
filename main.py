from DriveManager import DriveManager
from AudioManager import AudioManager
from LcdManager import LCDManager

import time
from datetime import datetime

class FloppyPlayer:
    class State: 
        RESET = 0
        IDLE = 1
        LOADING = 2
        PLAYING = 3
        END = 4
    
    def __init__(self):
        self.drive = DriveManager()
        self.audio = AudioManager()
        self.lcd = LCDManager()
        self.state = FloppyPlayer.State.RESET

    def run(self):
        while True:
            try:
                if self.state == FloppyPlayer.State.RESET:
                    self.handleReset()
                if self.state == FloppyPlayer.State.IDLE:
                    self.handleIdle()
                if self.state == FloppyPlayer.State.LOADING:
                    self.handleLoading()
                if self.state == FloppyPlayer.State.PLAYING:
                    self.handlePlaying()
                if self.state == FloppyPlayer.State.END:
                    self.handleEnd()
            except KeyboardInterrupt:
                return 0
            except Exception as e:
                print("Crashed: " + str(e))
                self.state = FloppyPlayer.State.END

    def handleReset(self):
        print("-> RESET")
        self.audio.stop()
        self.drive.reset()
        self.drive.usb.seek(0,0)
        self.audio = AudioManager()
        self.state = FloppyPlayer.State.IDLE
        self.lcd.setUpper([" Floppy  Player "])
        self.lcd.lowerLine = ["  Insert  Disk  "]

    def handleIdle(self):
        print("-> IDLE")
        if self.drive.getDiskAvailable():
            self.state = FloppyPlayer.State.LOADING
        else:
            time.sleep(1)

    def handleLoading(self):
        self.lcd.lowerLine = ["    Loading    "]
        nextData = self.drive.getNextData()
        meta = self.audio.getId3Tags(nextData)
        self.lcd.setUpper([meta["title"], meta["artist"]])
        self.audio.startAudioPipeline()
        self.startTime = datetime.now()
        self.audio.pushData(nextData)
        self.state = FloppyPlayer.State.PLAYING

    def handlePlaying(self):
        print("-> PLAYING")
        self.lcd.lowerLine = [f"{str(datetime.now() - self.startTime).split('.')[0][3:]}        B:{(self.audio.buffer.qsize())}"]
        nextData = self.drive.getNextData()
        if nextData:
            self.audio.pushData(nextData)
        else:
            self.state = FloppyPlayer.State.END

    def handleEnd(self):
        print("-> END")
        self.drive.reset()
        if  self.audio.buffer.qsize() > 0:
            self.lcd.lowerLine = [
                str(datetime.now() - self.startTime).split(".")[0][3:] + 
                "        ""B:" + 
                str(self.audio.buffer.qsize())]
        else:
            self.lcd.lowerLine = ["   Eject Disk   "]       
        if not self.drive.getDiskAvailable():
            self.state = FloppyPlayer.State.RESET
        else:
            time.sleep(1)
        

player = FloppyPlayer()
player.run()