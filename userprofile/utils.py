from django.db import models
from PIL import Image
import os


def Resize_image(image, max_width=1000, max_height=1000):
    img = Image.open(image)
    width, height = img.size
    
    # Calculate aspect ratio
    aspect_ratio = width / height
    
    # Check if resizing is necessary
    if width > max_width or height > max_height:
        if aspect_ratio > 1:  # Landscape orientation
            print('image is landscape')
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:  # Portrait or square orientation
            print('image is portrait')
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

        # Resize the image
        resized_img = img.resize((new_width, new_height))
        print(f'**{image.path}**')
        # Overwrite the original image with the resized image
        resized_img.save(image.path)

    # Return the path of the original image
    return image.path


# dirfil = r'C:\Users\zero9\Downloads'
# namefil = 'image.png'
# image = os.path.join(dirfil, namefil)


# print(Resize_image(image))
