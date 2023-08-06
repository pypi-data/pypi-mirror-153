import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from pdfcropper.utils.error import ErrorHandler


def crop_image(ifile, ofile, error='ignore', precrop=0):
    e = ErrorHandler(error=error)
    if not os.path.exists(ifile):
        msg = f':file:{ifile}: not found'
        e.send(FileNotFoundError, msg)

    #print(f'Cropping {input_filename} to {output_filename}')
    # Read in the image and convert to grayscale
    img = cv2.imread(ifile)
    if precrop > 0:
        img = img[:-precrop, :-precrop]  # Perform pre-cropping
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8)  # To invert the text to white
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, np.ones(
        (2, 2), dtype=np.uint8))  # Perform noise filtering
    coords = cv2.findNonZero(gray)  # Find all non-zero points (text)
    x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
    # Crop the image - note we do this on the original image
    cropped_image = img[y:y+h, x:x+w]
    if 0 in cropped_image.shape:
        msg = f':image:{ifile}: is empty'
        e.send(IndexError, msg)

    cv2.imwrite(ofile, cropped_image)


def add_text(ifile, ofile, text, padding=100):
    image = Image.open(ifile)
    top = padding
    width, height = image.size
    new_width = width
    new_height = height + top
    result = Image.new(image.mode, (new_width, new_height), (255, 255, 255))
    result.paste(image, (0, top))
    I1 = ImageDraw.Draw(result)
 
    # Custom font style and font size
    myFont = ImageFont.truetype('ariblk.ttf', 48)
    
    # Add Text to an image
    I1.text((width/4, 20), text, font=myFont, fill =(0, 0, 0))
    result.save(ofile)