import cv2
import datetime
import os
import sys

from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


'''
Global vars
'''
MODE_FNO = 'fno'
MODE_DUR = 'dur'

'''
Cut a video
'''
def cutVideo(input_file, output_file, start_seconds, end_seconds) :
    ffmpeg_extract_subclip(input_file, start_seconds, end_seconds, targetname=output_file)


'''
Extract frames from a video in MODE = DURATION
todo: check for video length
'''
def extractFrames_DUR(pathIn, pathOut,start_ex, duration, interval)  :
    # Create output folder
    # os.mkdir() creates a new dir. If it already exists, it raises an error
    # os.makedirs() creates a new dir. If it already exists, it OVERWRITES the previous one. Use it wisely.
    os.mkdir(pathOut)
    #os.makedirs(pathOut, exist_ok=True)

    # Open the video and get some properties
    cap = cv2.VideoCapture(pathIn)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames_per_interval = interval * fps

    # Grab the next frame
    success = cap.grab()
    fno = 0
    extracted = 0
    while fno / fps < duration :
        # Extract one frame for every frame_per_interval frames
        if (fno % frames_per_interval == 0) :
            ret, frame = cap.retrieve()
            if (ret == True) :
                #print ("Read frame %d: " % fno, ret)
                extracted += 1
                # Save frame as .jpeg file
                temp = fno/fps
                temp = round (temp, 2)
                cv2.imwrite(os.path.join(pathOut, "frame_{:d}_second_{:2f}.jpeg".format(fno, temp)), frame)
            else :
                print ("ERROR! During frame extraction")
                break
        success = cap.grab()
        fno += 1
    cap.release()

    # Extract Frames Report
    print ("\n####### Extract Frames REPORT")
    print ("Input title: ", pathIn)
    print ("Output folder: ", pathOut)
    print ("Start extraction at: ", start_ex)
    print ("Extracted frames: %d" % (extracted))
    print ("Given Duration: %f" % duration)
    print ("Given Interval: ", interval)
    print ("Frames per second: ", fps)
    print ("Frames per interval: ", frames_per_interval)
    print ("##################\n")

'''
Extract frames from a video in MODE = NUMBER OF FRAMES
todo: check for video length
'''
def extractFrames_FNO(pathIn, pathOut,start_ex, number_of_frames, interval)  :
    # Create output folder
    os.makedirs(pathOut, exist_ok=True)

    # Open the video and get some properties
    cap = cv2.VideoCapture(pathIn)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frames_per_interval = interval * fps

    # Grab the next frame
    success = cap.grab()
    fno = 0
    extracted = 0
    while extracted < number_of_frames :
        # Extract one frame for every frame_per_interval frames
        if (fno % frames_per_interval == 0) :
            ret, frame = cap.retrieve()
            if (ret == True) :
                #print ("Read frame %d: " % fno, ret)
                extracted += 1
                # Save frame as .jpeg file
                temp = fno/fps
                temp = round (temp, 2)
                cv2.imwrite(os.path.join(pathOut, "frame_{:d}_second_{:2f}.jpeg".format(fno, temp)), frame)
            else :
                print ("ERROR! During frame extraction")
                break
        success = cap.grab()
        fno += 1
    cap.release()

    # Extract Frames Report
    print ("\n####### Extract Frames REPORT")
    print ("Input title: ", pathIn)
    print ("Output folder: ", pathOut)
    print ("Start extraction at: ", start_ex)
    print ("Extracted frames: %d / %d" % (extracted, number_of_frames))
    print ("Given Interval: ", interval)
    print ("Frames per second: ", fps)
    print ("Frames per interval: ", frames_per_interval)
    print ("##################\n")


'''
Check wether the input file is a .mp4 or not
'''
def checkFormat(input_file) :
    if ( str(input_file.split(".")[1]).lower() != 'mp4') :
        print ("ERROR! No .mp4 file detected as input.")
        print ("Please use a .mp4 extension for the file.")
        return -1
    return 1


'''
Convert a string of the format mm:hh:ss:dd to a datetime.timedelta object
'''
def timeString_to_timeObj(timestring) :
    temp = tuple([int(x) for x in timestring[0:].split(':')])
    timeobj = datetime.timedelta(hours=temp[0], minutes=temp[1], seconds=temp[2], milliseconds=temp[3])
    return timeobj


'''
Convert a datetime.timedelta object to seconds
'''
def timeObj_to_seconds(timeobj) :
    return timeobj.total_seconds()


'''
Main
'''
def main()  :

    # Read command line input
    # Example 0: python frEx.py -cut -input input_file -output output_file -start hh:mm:ss:dd -end hh:mm:ss:dd
    # Example 1: python frEx.py -frex -input inputfile.mp4 -output output_folder -start hh:mm:ss:dd -duration hh:mm:ss:dd -interval hh:mm:ss:dd
    # Example 2: python frEx.py -frex -input inputfile.mp4 -output output_folder -start hh:mm:ss:dd -nf number_of_frames -interval hh:mm:ss:dd

    argv = sys.argv
    input_file = ''
    output_file = ''
    output_path = ''

    # Cut mode
    if ('-cut' in argv) :

        start_cut = 0.0
        end_cut = 0.0

        # -input command management
        if ('-input' in argv) :
            input_file = argv[argv.index('-input') +1]
            if (not checkFormat(input_file)) : return -1
        else :
            print ("ERROR! Missing -input command. Exiting . . .")
            return -1

        # -output command management
        if ('-output' in argv) :
            output_file = argv[argv.index('-output') +1]
        else :
            print ("WARNING! Missing -output command.")
            print ("Output file name set as ", input_file.split(".")[0] + "_out." +input_file.split(".")[1])
            output_file = input_file.split(".")[0] + "_out." +input_file.split(".")[1]

        # -start command management
        if ('-start' in argv) :
            start_cut_str = argv[argv.index('-start') +1]
            start_cut_obj = timeString_to_timeObj(start_cut_str)
            start_cut = timeObj_to_seconds(start_cut_obj)
        else :
            print ("WARNING! Missing -start command.")
            print ("The cut will start at default time set to 00:00:00.00.")
        
        # -end command management
        if ('-end' in argv) :
            end_cut_str = argv[argv.index('-end') +1]
            end_cut_obj = timeString_to_timeObj(end_cut_str)
            end_cut = timeObj_to_seconds(end_cut_obj)
        else :
            print ("WARNING! Missing -end command.")
            print ("The cut will end ad default time set to video duration time.")
            video = VideoFileClip(input_file)
            end_cut = video.duration

        # Cut Report
        print ("\n####### CUT REPORT")
        print ("Input title: ", input_file)
        print ("Output file: ", output_file)
        print ("Start cut at: ", start_cut)
        print ("End cut at: ", end_cut)
        print ("##################\n")


        # Cut execution
        cutVideo(input_file, output_file, start_cut, end_cut)

    # Frame Extraction mode
    elif ('-frex' in argv) :

        start_ex = 0.0
        end_ex = 0.0
        duration = 0.0
        number_of_frames = 0
        interval = 0
        mode = ''
        
        # -input command management
        if ('-input' in argv) :
            input_file = argv[argv.index('-input') +1]
        else :
            print ("ERROR! Missing -input command. Exiting . . .")
            return -1

        # -output command management
        if ('-output' in argv) :
            output_file = argv[argv.index('-output') +1]
        else :
            print ("WARNING! Missing -output command.")
            print ("Output file name set as ", input_file.split(".")[0] + "_out." +input_file.split(".")[1])
            output_file = input_file.split(".")[0] + "_out." +input_file.split(".")[1]

         # -start command management
        if ('-start' in argv) :
            start_ex_str = argv[argv.index('-start') +1]
            start_ex_obj = timeString_to_timeObj(start_ex_str)
            start_ex = timeObj_to_seconds(start_ex_obj)
        else :
            print ("WARNING! Missing -start command.")
            print ("The cut will start at default time set to 00:00:00.00.")

        # Duration or number of frames management
        if ('-duration' in argv) :
            duration_str = argv[argv.index('-duration') +1]
            duration_obj = timeString_to_timeObj(duration_str)
            duration = timeObj_to_seconds(duration_obj)
            mode = MODE_DUR
        elif ('-nf' in argv) :
            nf_str = argv[argv.index('-nf') +1]
            number_of_frames = int(nf_str)
            mode = MODE_FNO
        else :
            print ("ERROR! Specify frame extraction mode [-duration | -nf].")
            return -1

        # -interval command management
        if ('-interval' in argv) :
            interval_str = argv[argv.index('-interval') +1]
            interval_obj = timeString_to_timeObj(interval_str)
            interval = timeObj_to_seconds(interval_obj)
        else :
            print ("ERROR! Missing sampling interval.")
            return -1

        if (mode == MODE_FNO) :
            extractFrames_FNO(input_file, output_file,start_ex, number_of_frames, interval)
        elif (mode == MODE_DUR) :
            extractFrames_DUR(input_file, output_file,start_ex, duration, interval)
        


    elif ('-help' in argv) :
        print("Example 0: python frEx.py -cut -input input_file -output output_file -start hh:mm:ss:dd -end hh:mm:ss:dd")
        print("Example 1: python frEx.py -frex -input inputfile.mp4 -output output_folder -start hh:mm:ss:dd -duration hh:mm:ss:dd")
        print("Example 2: python frEx.py -frex -input inputfile.mp4 -output output_folder -start hh:mm:ss:dd -nf number_of_frames -interval hh:mm:ss:dd")


    #extractFrames('cut.mp4', 'data')

if __name__=="__main__":
    main()
