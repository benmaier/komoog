#!/bin/bash

for i in $(ls . | grep wav)
do
    echo $i
    ffmpeg -loop 1 -i ../pixel.png -i $i -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest $i.mp4
done
