#!/bin/bash

waitForFloppyOut () {
  echo Waiting for floppy to be ejected
  while ./gw pin get 28 | ( ! grep Low > /dev/null )
  do
    :
  done
}

waitForFloppyIn () {
  echo Waiting for floppy to be inserted
  printf "  |  Insert  |\n  V   Disk   V" > disp 
  while ./gw pin get 28 | ( ! grep High > /dev/null )
  do
    :
  done
}

killAudioPipeline () {
   echo Kill audio pipeline
   killall aplay
   killall ffmpeg
}

startAudioPipeline () {
  echo Start audio pipeline
  printf "Loading..." > disp 
  bufferFill=0
  while [[ $bufferFill -le 2048 ]]
  do
    bufferFill=$(wc -c /tmp/buffer.img | awk '{print $1}')
    if [ $? -ne 0 ]; then bufferFill=0; fi;
  done
  echo Playing...
  
  ls -lah /tmp/ | grep buffer.img | awk '{print "Playing...\n", $5}' > disp
  ffmpeg -err_detect ignore_err  -i /tmp/buffer.img -f wav - | aplay -q -t wav
  printf "Eject floppy" > disp
}

while true
do
  echo Prepare next run
  ./gw seek 0
  rm -f /tmp/buffer.img
  touch /tmp/buffer.img

  waitForFloppyIn
  startAudioPipeline  &

  ./gw read --revs 1 --retries 0 /tmp/buffer.img > /dev/zero
  if [ $? -ne 0 ]
  then
    killAudioPipeline > /dev/null
  fi

  waitForFloppyOut
  killall aplay && killall ffmpeg
done
}
