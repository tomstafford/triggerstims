'''
Timer stimulus generation
- makes videos of shrinking circles of different colours
'''

import socket #to get host machine identity
import os # for joining paths and filenames sensibly
import scipy.misc #for image function
import numpy as np #number functions

#test which machine we are on and set working directory
if 'tom' in socket.gethostname():
    os.chdir('/home/tom/Dropbox/university/students/choice_risk/images')
else:
    print("I don't know where I am! ")


#cribbing from
#https://stackoverflow.com/questions/12062920/how-do-i-create-an-image-in-pil-using-a-list-of-rgb-tuples

def distance(x,y,centre):
    '''calculate straight line distance of two x,y points'''
    return np.sqrt((centre[0]-x)**2 + (centre[1]-y)**2)


def makeimg(width,height,colour,radius,filename):
    '''make an image containing a coloured circle'''
    channels = 3
    centre=[width/2, height/2]
    # Create an empty image
    if colour==[0,0,0]: #white background
        img = 255*np.ones((height, width, channels), dtype=np.uint8)
    else:
        img = np.zeros((height, width, channels), dtype=np.uint8)
    # Draw something (http://stackoverflow.com/a/10032271/562769)
    xx, yy = np.mgrid[:height, :width]
    # Set the RGB values
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            r, g, b = colour
            if distance(x,y,centre)<radius:
                img[y][x][0] = r
                img[y][x][1] = g
                img[y][x][2] = b

    return img

#colours of our stimuli
colours=[[0,0,0],[0,0,255],[0,255,0],[0,255,255],
         [255,0,0],[255,0,255],[255,255,0],[255,255,255]]

# Image size
width = 640
height = 480

#loop over colours
for c,colour in enumerate(colours):
    colourname='c'+str(c)

    #make frames
    for i,radius in enumerate(np.linspace(min([width,height])/2,0,6)):
        filename='img'+str(i)+'.png'
         
        # Make image    
        img=makeimg(width,height,colour,radius,filename)
        # Save the image
        scipy.misc.imsave(filename, img)
    
    #join frames into mp4 - you need ffmpeg installed
    os.system("ffmpeg -r 1 -i img%01d.png -vcodec mpeg4 -y " + colourname + ".mp4")
