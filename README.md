# Introduction
Combine an old storage medium and the newest audio codec technologies and you get... Something. This thing here. 

The goal of this project is to mimic the feeling of having your favorite songs in your hands again. 
I choosed floppy disks for the availability and price.

# Hardware
For my version of the floppy player i used:
- NEC FD1231H floppy drive (next best one i had)
- A [Greaseweazle](https://github.com/keirf/Greaseweazle)
- Orange Pi Zero (Cheapes SBC with Armbian)
- Charakter LCD

# Technologies
## Encoding 
The audio codec behind this is  the MPEG-4 High Efficiency Advanced Audio Coding HE-AAC developed by the Frauenhofer IIS. It reaches good sound quality at low bitrates. 
ADTS is used as the transport format, as it includes syncronisation, which is important on unreliable mediums such as floppys

## Storage
High density 3.5" 1.44MB floppy disks are used. With this low storage capacity, an audio stream in sufficient audio quality reaches around 5 minutes of play time.
Of course, this is highly subjective and varies from person to person.

## Greaseweazle
At this point, i have to give a hughe thanks to Keirf and his incredible work on the [Greaseweazle](https://github.com/keirf/Greaseweazle) project. 
With Greaseweazle, it is possible to rescue floppy disks in all formats flux level data manipulation. 
The floppy player uses this project to read and write floppy disks without the the burden of a dedicated floppy controller.

# Setup
## Greaseweazle
Follow the setup instruction on the [Greaseweazle](https://github.com/keirf/Greaseweazle) project page

## Configuration
In the next revision, a config file will be used for the setup.
As long as this does not exist, the following options have to be set.
### LCD Manger
The LCD Manager provides functions and a backgroung thread for handling a user interface.
Open the LcdManager.py and change the settings according to your setup:

variable | default | usage
-|-|-
PIN_RESET | 5 | LCD reset pin
PIN_RW |3 | LCD read/write select pin
PIN_ENABLE | 7 | LCD enable ping
PIN_DATA | [12, 11, 8, 10] |  data pins as array (D4, D5, D6, D7)
START_STOP_DELAY | 3 | time in seconds at the end and beginning of text scrolling
REFRESH_DELAY | 0.5 | time in seconds to shift one character of text

As the interface is fixed to 2 rows, the LCD settings (LCD_COLUMNS, LCD_ROWS, LCD_DOTSIZE) should not be changed, unless you wish to design your own UI.

### Audio Manager
This class handles all audio related tasks, such as starting/stopping of audio server, decoder and player. 
The AudioManager.py file does not provide much flexibilty as for now.
Only the audio server can be changed. 
In the future, audio normalization, bitrates, and more audio device settings will be added

variable | default | usage
-|-|-
AUDIO_DEVICE | pulse | audio device used for aplay

### Device Manager
This part handles all drive related tasks such as disk insert detection, motor control and data readout. All functions in here rely heavilly on the Greaseweazle project.

variable | default | usage
-|-|-
GREASEWEAZLE_DEVICE | /dev/ttyACM0 | The serial device representing the Greaseweazle

# Todo
- Configuration file
- Logging
- Requirements setup
- Audio Manager settings
- Burn script