# Erame Extractor
A simple tool to naively cut and extract frames from a .mp4 video

# Modes
Three different modes are available: _cut_ to cut a video, _duration_ to extract frames for a certain time at a given interval, _frame number_ to extract the wanted number of frame each interval unit

* * *

### CUT MODE

`
python frEx.py -cut -input input_file -output output_file -start hh:mm:ss:dd -end hh:mm:ss:dd
`

Example:
`
python frEx.py -cut -input video.mp4 -output cut.mp4 -start 00:03:27:500 -end 00:05:25:100
`

In this way you will cut the video _video.mp4_ from the **minute 3, second 27.5** to the **minute 5, second 25.1**.

* * *

### EXTRACT FRAMES FOR A GIVEN TIME

`
python frEx.py -frex -input inputfile.mp4 -output output_folder -start hh:mm:ss:dd -duration hh:mm:ss:dd -interval hh:mm:ss:dd
`

Example:

`
python frEx.py -frex -input video.mp4 -output data -start 00:01:21:200 -duration 00:02:30:00 -interval 00:00:00:500
`

In this way you will extract **1 frame every 0.5 seconds** from the video _video.mp4_ starting from **minute 1, second 21.2** for a total time of **minutes 2, seconds 30**.

* * *

### EXTRACT A FIXED NUMBER OF FRAMES

`
python frEx.py -frex -input inputfile.mp4 -output output_folder -start hh:mm:ss:dd -nf number_of_frames -interval hh:mm:ss:dd
`

Example:
`
python frEx.py -frex -input video.mp4 -output data -start 00:02:15:500 -nf 10 -interval 00:00:00:100
`

In this way you will extract **nf = 10 frames** from the video _video.mp4_ starting from **minute 02, second 15.5** with an **interval of 1 frame every 0.1 seconds**.

* * *

### Requirements
Requirements can be found in the file _requirements.txt_

* * *

## Disclaimer
This software has not been tested in edge scenarios, it is just something I need right now to do stuffs, so no input control has been implemented.

Enjoy
