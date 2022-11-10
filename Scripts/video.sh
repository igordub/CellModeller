#!/bin/bash

# Note: this script requires imagemagick, ffmpeg and ghostscript
# The easiest way to install on OSX is to install homebrew package manager
# and then "brew install imagemagick" etc.

# Run Draw2DPDF to generate pdf files
for file in $( ls *.pickle ); do
    echo Processing: $file
    python3 $HOME/apps/cellmodeller/Scripts/Draw2DPDF.py $file > /dev/null
done

# Convert and resize etc. pdf files into png
for file in $( ls *.pdf ); do
    NAME=`basename $file .pdf`
    convert \
        -colorspace RGB \
        -verbose        \
        -density 150    \
        $NAME.pdf       \
        $NAME.png
done

# Run ffmpeg to generate video file
ffmpeg -framerate 7 -i %*.png -vf scale=1920:1080 -r 24 $1
