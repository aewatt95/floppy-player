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
Of couse, this is just my personal impression.

## Greaseweazle
At this point, i have to give a hughe thanks to Keirf and his incredible work on the [Greaseweazle](https://github.com/keirf/Greaseweazle) project. 
With Greaseweazle, it is possible to rescue floppy disks in all formats flux level data manipulation. 
The floppy player uses this project to read and write floppy disks without the the burden of a dedicated floppy controller.
