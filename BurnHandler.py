from flask import Flask, render_template, redirect, request
from LcdManager import LCDManager
import threading
import subprocess
import time
import os
import shutil
import socket

distance = 0.1

class BurnHandler(threading.Thread):
    def __init__(self, lcdManager: LCDManager = None):
        threading.Thread.__init__(self)
        self.app = Flask(__name__)
        self.lcd = lcdManager
        self.running = False
        self.blocked = False
        if self.lcd == None:
            self.lcd = LCDManager()
        #self.l

    def burn(self, url, title, artist):
        self.url = url
        self.title = title
        self.artist = artist
        self.process = subprocess.Popen(["/home/andre/floppy-player/burn2floppy.sh", url, title, artist],  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        line = ""
        while self.process.poll() == None:
            lastElement = self.process.stdout.read(1).decode("utf-8", errors="ignore")
            if lastElement == "\r" or lastElement == "\n":
                print(line)
                try:
                    if "s ETA " in line:
                        self.lcd.setUpper(["1/3: Download"])
                        progress = float(line.split()[1][:-1])
                        progressBar = ""
                        for i in range(0,int(0.16 * progress)):
                            progressBar += chr(255)
                        self.lcd.lowerLine = [progressBar]
                    if ", ETA" in line:
                        self.lcd.setUpper(["2/3: Encode"])
                        progress = float(line.split()[0][1:-2])
                        progressBar = ""
                        for i in range(0,int(0.16 * progress)):
                            progressBar += chr(255)
                        self.lcd.lowerLine = [progressBar]
                    if "Writing Track" in line:
                        self.lcd.setUpper(["3/3: Write"])
                        progress = float(line.split()[2][:-3])
                        progressBar = ""
                        for i in range(0,int((16/81) * progress)):
                            progressBar += chr(255)
                        self.lcd.lowerLine = [progressBar]
                except Exception as e:
                    print("Error in burn()")
                line = ""
            else:
                line += lastElement
        self.lcd.setUpper(["Finished!"])
        self.lcd.lowerLine = (["                "])
        pass

    def run(self):
        self.app.add_url_rule("/", view_func=self.home)
        self.app.add_url_rule("/startDownload", view_func=self.startDownload, methods=['POST'])
        try:
            self.app.run(debug = False, host="0.0.0.0", port=80)
        except RuntimeError as e:
            print(e)

    def stop(self):
            del self.app

    def home(self):
        if self.blocked or self.running:
            return render_template('blocked.html')
        return render_template('page.html')

    def startDownload(self):
        if self.blocked:
            return redirect(request.referrer)
        self.running = True
        print(str(request.form.to_dict()))
        self.lcd.setUpper(["0/3 Prepare"])
        self.lcd.lowerLine = ["                "]
        uploadedFile = request.files["file"]
        print(uploadedFile)
        if uploadedFile.filename != '':
            uploadedFile.save("/tmp/floppySong.mp3")
            self.burn("/tmp/floppySong.mp3", request.form["title"], request.form["artist"])
        else:
            self.burn(request.form["url"], request.form["title"], request.form["artist"])
        self.running = False
        return redirect(request.referrer)


if __name__ == "__main__":
    lcd = LCDManager()
    lcd.setUpper(["    BURNMODE   "])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    myIp = s.getsockname()[0]
    s.close()
    lcd.lowerLine = [myIp]
    BurnHandler(lcd).start()