from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import glob
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DEBUG_MODE = False

VIDEOLIST_EXCEL = "Video_List.xlsx"
VIDEO_EXTENTION = ".mp4"

RAW_VIDEO_FOLDER = "raw_videos\\"
COVER_SLIDE_FOLDER = "cover_slides\\"
PROCESSED_VIDEO_FOLDER = "processed_videos\\"

SYMPOSIUM_NAME = "IFCS-EFTF 2019 Symposium, Orlando USA"
SYMPOSIUM_BANNER = "imgdata\\ifcs-eftf2019-logo-banner-01_web.png"
SYMPOSIUM_LOGO = "imgdata\\ifcs-eftf2019.png"

UFFC_BANNER = "imgdata\\IEEE-UFFC.png"
UFFC_LOGO = "imgdata\\uffc-logo-small-transparent.png"

FINEPRINT_LINE_1 = "Video recorded and uploaded with the authors' consent."
FINEPRINT_LINE_2 = "Any opinions expressed by the authors do not necessarily reflect the views of the IEEE UFFC Society."
FINEPRINT_LINE_3 = ""
FINEPRINT_LINE_4 = "IEEE UFFC Society Symposia - https://ieee-uffc.org/symposia/"
FINEPRINT_LINE_5 = "IEEE UFFC Society Transactions - https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=58"

COVER_DURATION = 5

# Grab the list of all of the mp4 videos from the raw_videos folder.
videoList = pd.read_excel(VIDEOLIST_EXCEL)
# Iterate over each video
for dataIndex,dataRow in videoList.iterrows():

    videoID = dataRow.ID
    videoSession = dataRow.Session
    videoAuthor = dataRow.Author
    videoTitle = dataRow.Title + VIDEO_EXTENTION
    print("|"+videoTitle + "|")
    # videoFile = dataRow.Vide)

    # Load the video as a VideoFileClip. If debug mode enabled, keep only
    # the first 30 seconds of each video for further processing.
    if DEBUG_MODE == True:
        mainVideo = VideoFileClip(RAW_VIDEO_FOLDER + videoTitle).subclip(0, 30)
    else:
        mainVideo = VideoFileClip(RAW_VIDEO_FOLDER + videoTitle)
        
    videoWidth,videoHeight = mainVideo.size

    coverImage = Image.new("RGB",(videoWidth,videoHeight),"white")
    drawHandler = ImageDraw.Draw(coverImage)

    #fontsize=2
    #fnt = ImageFont.truetype("arial.ttf", fontsize)
    #while fnt.getsize(videoTitle)[0] < 0.9*videoWidth:
    #    fontsize += 1
    #    fnt = ImageFont.truetype("arial.ttf", fontsize)

    #tw, th = drawHandler.textsize(videoTitle, font=fnt)
    #drawHandler.text(((videoWidth-tw)/2,(videoHeight-th)/2), videoTitle, fill="black", font=fnt)

    dpi = 100
    titleSize = 1
    fig = plt.figure(figsize=(videoWidth/dpi,videoHeight/dpi))
    text = fig.text(0, 0, videoTitle, name="Arial",size=titleSize)    
    fig.savefig('formula.png', dpi=dpi)
    
    while text.get_window_extent().size[0] < 0.9*videoWidth and text.get_window_extent().size[1] < 0.1*videoHeight:
        plt.clf()
        titleSize = titleSize + 1
        text = fig.text(0, 0, videoTitle, name="Arial",size=titleSize)
        fig.savefig('formula.png', dpi=dpi)
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    # Adjust the figure size so it can hold the entire text.
    fig.set_size_inches((width, height))
    
    # Adjust text's vertical position.
    dy = (bbox.ymin/float(dpi))/height
    text.set_position((0, -dy))
    
    # Save the adjusted text.
    fig.savefig('formula2.png', dpi=dpi)

    image1 = Image.open("formula2.png")
    width1, height1 = image1.size
    image1 = image1.convert("RGBA")
    coverImage.paste(image1, (int(videoWidth/2) - int(width1/2), int(videoHeight/2) - int(height1/2)), image1)

    image1 = Image.open(UFFC_BANNER)
    width1, height1 = image1.size
    image1 = image1.convert("RGBA")
    coverImage.paste(image1, (videoWidth - width1, videoHeight - height1), image1)

    image1 = Image.open(SYMPOSIUM_BANNER)
    width1, height1 = image1.size
    image1 = image1.convert("RGBA")
    coverImage.paste(image1, (int(videoWidth/2) - int(width1/2),  height1), image1)

    msg = " 2019 " + videoAuthor + " and IEEE UFFC Society, All Rights Reserved"
    fontsize=2
    fnt = ImageFont.truetype("arial.ttf", fontsize)
    while fnt.getsize(msg)[1] < 0.02*videoHeight:
        fontsize += 1
        fnt = ImageFont.truetype("arial.ttf", fontsize)
    tw, th = drawHandler.textsize(msg, font=fnt)
    drawHandler.text((2,int(videoHeight)-6*(th+1)), msg, fill="black", font=fnt)

    msg = FINEPRINT_LINE_1
    tw, th = drawHandler.textsize(msg, font=fnt)
    drawHandler.text((2,int(videoHeight)-5*(th+1)), msg, fill="black", font=fnt)

    msg = FINEPRINT_LINE_2
    tw, th = drawHandler.textsize(msg, font=fnt)
    drawHandler.text((2,int(videoHeight)-4*(th+1)), msg, fill="black", font=fnt)

    msg = FINEPRINT_LINE_3
    tw, th = drawHandler.textsize(msg, font=fnt)
    drawHandler.text((2,int(videoHeight)-3*(th+1)), msg, fill="black", font=fnt)

    msg = FINEPRINT_LINE_4
    tw, th = drawHandler.textsize(msg, font=fnt)
    drawHandler.text((2,int(videoHeight)-2*(th+1)), msg, fill="black", font=fnt)

    msg = FINEPRINT_LINE_5
    tw, th = drawHandler.textsize(msg, font=fnt)
    drawHandler.text((2,int(videoHeight)-1*(th+1)), msg, fill="black", font=fnt)


    fntbd = ImageFont.truetype("arialbd.ttf", fontsize)
    fontsize=2
    while fntbd.getsize(videoAuthor)[1] < 0.03*videoHeight:
        fontsize += 1
        fntbd = ImageFont.truetype("arialbd.ttf", fontsize)
    
    tw, th = drawHandler.textsize(videoAuthor, font=fntbd)
    drawHandler.text(((videoWidth-tw)/2,int(0.5*videoHeight)+2*(th+2)), videoAuthor, fill="black", font=fntbd)

    tw, th = drawHandler.textsize(videoSession, font=fntbd)
    drawHandler.text(((videoWidth-tw)/2,int(0.5*videoHeight)+3*(th+2)), videoSession, fill="black", font=fntbd)

    tw, th = drawHandler.textsize(SYMPOSIUM_NAME, font=fntbd)
    drawHandler.text(((videoWidth-tw)/2,int(0.5*videoHeight)+4*(th+2)), SYMPOSIUM_NAME, fill="black", font=fntbd)


    coverImage.save(COVER_SLIDE_FOLDER + "coverSlide" + str(videoID) + ".jpg", "JPEG")
    
    logoUFFCBottomRight = (ImageClip(UFFC_LOGO)
              .set_duration(mainVideo.duration)
              .resize(height=int(videoHeight/5))
              .margin(right=8, bottom=8, opacity=0.5)
              .set_pos(("right","bottom")))

    logoSymposiumBottomLeft = (ImageClip(SYMPOSIUM_LOGO)
              .set_duration(mainVideo.duration)
              .resize(height=int(videoHeight/5))
              .margin(left=8, bottom=8, opacity=0.5)
              .set_pos(("left","bottom")))

    compositeVideo = CompositeVideoClip([mainVideo, logoUFFCBottomRight, logoSymposiumBottomLeft])    
    
    coverSlide = ImageClip(COVER_SLIDE_FOLDER + "coverSlide" + str(videoID) + ".jpg")
    coverSlide = coverSlide.set_duration(COVER_DURATION)
    finalVideo = concatenate_videoclips([coverSlide,compositeVideo])

    finalVideo.write_videofile(PROCESSED_VIDEO_FOLDER + str(videoID) + ".mp4")