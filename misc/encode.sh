#!/bin/bash
# INRAE\Olivier Vitrac - rev. 21/03/2021
# fork from: 
# inspired from: https://stackoverflow.com/questions/41346234/can-ffmpeg-encode-multiple-files-at-once

in_dir=`pwd`
out_dir="$in_dir/converted"
in_file="*.gif"
resolution="1280"
mkdir -p "$out_dir"
#IFS=$'\n'

i=0;
find "${in_dir}" -type f -name "${in_file}" | sort | while IFS= read -r in_file; do
    ((i=i+1))
    echo "==========================="
    echo "$i> processing ${in_file}"
    fullname="${in_file##*/}"
    dirname="${in_file%/*}"
    basename="${fullname%.*}"
    extension="${fullname##*.}"
    if [ "$dirname" == "$path" ]; then
        dirname="."
    fi
    if [ "$extension" == "$basename" ]; then
        extension=""
    fi
    echo "Dirname:   $dirname"
    echo "Fullname:  $fullname"
    echo "Basename:  $basename"
    echo "Extension: $extension"
    fname="$basename$extension"
    out_file="$out_dir/$basename"
    # Generate cover image
    cd "$dirname"
    ffmpeg -i "$fullname" -vframes 1 -ss 00:00:00.060 -vf scale=${resolution}:-2 -q:v 1 "${out_file}.jpg" </dev/null
    #cd "$dirname"
    ffmpeg -i "$fullname" -c:v libvpx -qmin 0 -qmax 25 -crf 4 -b:v 1M -vf scale=${resolution}:-2 -an -threads 0 "${out_file}.webm" </dev/null
    cd "$dirname"
    # Generate MP4
    ffmpeg -i "$fullname" -c:v libx264 -pix_fmt yuv420p -profile:v baseline -level 3.0 -crf 22 -preset veryslow -vf scale=${resolution}:-2 -an -movflags +faststart -threads 0 "${out_file}.mp4" </dev/null
    echo "> ${out_file}.mp4,.jpg generated"
    echo "==========================="
done
cd "$in_dir"
