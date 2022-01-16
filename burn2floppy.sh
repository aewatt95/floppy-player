#!/bin/bash

rm -f /tmp/floppySong.img

if  echo $1 | ( grep https > /dev/null )
then
    echo Download youtube video
    youtube-dl -f bestaudio --audio-quality 0 --audio-format wav -i -k -x -o /tmp/floppySong.img --extract-audio $1 
else
    ffmpeg -y -i "$1" /tmp/floppySong.wav
fi

duration=$(soxi -D /tmp/floppySong.wav)
bitrate=$(awk 'BEGIN { printf "%3.0f\n", int( 1440 * 8 / ( '$duration' ) ) }')

echo Calculated bitrate: $bitrate from $duration

fdkaac --profile 29 -b $bitrate -f 2 /tmp/floppySong.wav -o /tmp/floppySong.img
id3v2 --artist "$3" --song "$2" /tmp/floppySong.img

dd if=/dev/zero bs=1M count=1 >> /tmp/floppySong.img
stat /tmp/floppySong.img

/home/andre/git/Greaseweazle/gw write --no-verify /tmp/floppySong.img
