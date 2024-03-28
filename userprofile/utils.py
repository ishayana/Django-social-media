from django.db import models
from PIL import Image
import os


def Resize_image(image, max_width=1920, max_height=1080):
    img = Image.open(image)
    width, height = img.size
    # Calculate aspect ratio
    aspect_ratio = width / height
    # Check if resizing is necessary
    if width > max_width or height > max_height:
        if aspect_ratio > 1:  # Landscape orientation
            new_width = max_width
            new_height = int(max_width / aspect_ratio)

        else:  # Portrait or square orientation
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

        # Resize the image
        img = img.resize((new_width, new_height))
        # Overwrite the original image with the resized image
        img.save(image.path)

    # Return the path of the original image
    return image.path
