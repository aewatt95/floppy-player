from DriveManager import DriveManager
from AudioManager import AudioManager
from LcdManager import LCDManager
from BurnHandler import BurnHandler
from LedManager import LedManager
from Common import State
import time
from datetime import datetime
class FloppyPlayer:

    def __init__(self):
        self.drive = DriveManager()
        self.audio = AudioManager()
        self.lcd = LCDManager()
        self.burnHandler = BurnHandler(self.lcd)
        self.burnHandler.start()
        self.state = State.RESET
        self.led = LedManager()

    def run(self):
        while True:
            try:
                if self.state == State.RESET:
                    self.handleReset()
                elif self.state == State.BURN:
                    self.handleBurn()
                elif self.state == State.IDLE:
                    self.handleIdle()
                elif self.state == State.LOADING:
                    self.handleLoading()
                elif self.state == State.PLAYING:
                    self.handlePlaying()
                elif self.state == State.END:
                    self.handleEnd()
                self.led.handleState(self.state)
            except KeyboardInterrupt:
                return 0
            except Exception as e:
                print("Crashed: " + str(e))
                self.state = State.END

    def handleBurn(self):
        print("-> BURN")
        if self.burnHandler.running == False:
            self.state = State.RESET
        else:
            time.sleep(1)

    def handleReset(self):
        print("-> RESET")
        self.audio.stop()
        self.drive.reset()
        self.drive.usb.seek(0,0)
        self.burnHandler.blocked = False
        self.audio = AudioManager()
        self.state = State.IDLE
        self.lcd.setUpper([" Floppy  Player "])
        self.lcd.lowerLine = ["  Insert  Disk  "]

    def handleIdle(self):
        print("-> IDLE")
        if self.drive.getDiskAvailable():
            self.burnHandler.blocked = True
            self.state = State.LOADING
        elif self.burnHandler.running:
            self.state = State.BURN
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
        self.state = State.PLAYING

    def handlePlaying(self):
        print("-> PLAYING")
        self.lcd.lowerLine = [f"{str(datetime.now() - self.startTime).split('.')[0][3:]}        B:{(self.audio.buffer.qsize())}"]
        if not self.audio.pipelineAlive():
            self.state = State.END
        if not self.audio.endFlag:
            nextData = self.drive.getNextData()
            if nextData:
                self.audio.pushData(nextData)
        else:
            if not self.drive.getDiskAvailable():
                self.state = State.RESET
            time.sleep(0.5)


    def handleEnd(self):
        print("-> END")
        self.drive.reset()
        self.lcd.lowerLine = ["   Eject Disk   "]
        if not self.drive.getDiskAvailable():
            self.state = State.RESET
        else:
            time.sleep(1)

player = FloppyPlayer()
player.run()
