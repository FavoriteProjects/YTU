import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import glob
import pandas as pd
import matplotlib
import textwrap
matplotlib.use('Agg')

DEBUG_MODE = True

VIDEOLIST_EXCEL = "Video_List.xlsx"
VIDEO_EXTENTION = ".mp4"

RAW_VIDEO_FOLDER = "raw_videos\\"
COVER_SLIDE_FOLDER = "cover_slides\\"
PROCESSED_VIDEO_FOLDER = "processed_videos\\"

SLIDE_BACKGROUND = "imgdata\\Slide_Background.png"

COVER_DURATION = 5

# Grab the list of all of the mp4 videos from the raw_videos folder.
videoList = pd.read_excel(VIDEOLIST_EXCEL)
# Iterate over each video
for dataIndex, dataRow in videoList.iterrows():

    videoID = dataRow.ID
    videoTitle = dataRow.Title
    videoAuthor = dataRow.Author
    videoAffiliation = dataRow.Affiliation
    print('|' + videoTitle + '|')
    # videoFile = dataRow.Vide)

    # Load the video as a VideoFileClip. If debug mode enabled, keep only
    # the first 30 seconds of each video for further processing.
    if DEBUG_MODE == True:
        mainVideo = VideoFileClip(
            RAW_VIDEO_FOLDER + videoTitle + VIDEO_EXTENTION).subclip(0, 30)
    else:
        mainVideo = VideoFileClip(
            RAW_VIDEO_FOLDER + videoTitle + VIDEO_EXTENTION)

    videoWidth, videoHeight = mainVideo.size

    # coverImage = Image.new("RGB",(videoWidth,videoHeight),"white")
    coverImage = Image.open(SLIDE_BACKGROUND)
    drawHandler = ImageDraw.Draw(coverImage)

    # setting video title to it's place
    fntbd = ImageFont.truetype("calibrib.ttf", 80)
    y = videoHeight*(0.33)
    lines = textwrap.wrap(videoTitle,width=25)
    for line in lines:
        lw, lh = fntbd.getsize(line)
        x = (videoWidth)/25 + (videoWidth - lw)/2 - 7*(videoWidth)/25 + 25
        drawHandler.text( (x ,y) , line, fill="white", font=fntbd,anchor=None,spacing=4, align="center")
        y += (1.05)*lh

    # setting video author to it's place
    fntbd = ImageFont.truetype("calibrib.ttf", 40)
    y = videoHeight*(0.6)
    lines = textwrap.wrap(videoAuthor,width=25)
    authorspace=0
    for line in lines:
        lw, lh = fntbd.getsize(line)
        x = (videoWidth)/25 + (videoWidth - lw)/2 - 7*(videoWidth)/25
        drawHandler.text( (x ,y) , line, fill="white", font=fntbd,anchor=None,spacing=4, align="center")
        y += (1.05)*lh
        authorspace += lh

    # setting video Affiliation to it's place
    fntbd = ImageFont.truetype("calibrib.ttf", 35)        
    y = videoHeight*(0.6) + (1.5)*authorspace
    lines = textwrap.wrap(videoAffiliation,width=35)
    for line in lines:
        lw, lh = fntbd.getsize(line)
        x = (videoWidth)/25 + (videoWidth - lw)/2 - 7*(videoWidth)/25
        drawHandler.text( (x ,y) , line, fill="white", font=fntbd,anchor=None,spacing=4, align="center")
        y += (1.05)*lh


    coverImage.save(COVER_SLIDE_FOLDER + "coverSlide" + str(videoID) + ".png", "PNG")
    # Video Concatenation with formed slide
    compositeVideo = CompositeVideoClip([mainVideo])
    coverSlide = ImageClip(COVER_SLIDE_FOLDER + "coverSlide" + str(videoID) + ".png")
    coverSlide = coverSlide.set_duration(COVER_DURATION)
    finalVideo = concatenate_videoclips([coverSlide, compositeVideo, coverSlide])

    finalVideo.write_videofile(PROCESSED_VIDEO_FOLDER + str(videoID) + ".mp4")
