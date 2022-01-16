import threading
import timeout_decorator
import sys

sys.path.append("./Greaseweazle/scripts")

import greaseweazle.tools.util as util
import greaseweazle.codec.ibm.mfm as mod
import greaseweazle.image.img as img

GREASEWEAZLE_DEVICE = "/dev/ttyACM0"

class DriveManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.reset()
        
    def run(self):
        print("DriveManager instance started")


    def reset(self):
        self.cylinder = 0
        self.head = 0
        self.decoder = mod.decode_track
        self.usb = util.usb_open(GREASEWEAZLE_DEVICE)
        self.usb.set_bus_type(1)
        self.usb.drive_select(0)
        self.usb.drive_motor(0, False)

    # Use the write protect switch as an indicator for inserted disk 
    def getDiskAvailable(self):
        return self.usb.get_pin(28)

    @timeout_decorator.timeout(3)
    def getNextData(self):
        self.usb.drive_motor(0, True)
        self.usb.seek(self.cylinder, self.head)
        rawData = self.usb.read_track(revs=1, ticks=0)
        decodedData = self.decoder(self.cylinder, self.head, rawData)
        if self.head == 0:
            self.head += 1
        
        elif self.cylinder < 81:
            self.cylinder += 1
            self.head = 0
        else:
            self.cylinder = 0
            self.head = 0
            self.usb.drive_motor(0, False)
            return None
        return decodedData.get_img_track()
