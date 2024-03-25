from django.db import models
from PIL import Image
import os

# # resize custom ImageFields
# def Resize_image(image_file, max_width=1000, max_hieght=1000):
#     img = Image.open(image_file)
#     width, height = img.size

#     # Calculate image size in megabytes after extracting dimensions
#     image_size = (width * height) / (1024 * 1024)
#     aspect_ratio = width / height  # Calculate aspect ratio
#     if width > max_width or height > max_hieght:

#         if aspect_ratio > 1:  # Landscape orientation
#             new_width = max_width
#             new_height = int(max_width / aspect_ratio)
#         else:  # Portrait or square orientation
#             new_height = max_hieght
#             new_width = int(max_hieght * aspect_ratio)

#         resized_img = img.resize((int(new_width), int(new_height)))
#         resized_img.save(f'{image_file}-resized.{img.format.lower()}')
#         return resized_img
        
#     return img




def Resize_image(image, max_width=1000, max_height=1000):
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


# dirfil = r'C:\Users\zero9\Downloads'
# namefil = 'image.png'
# image = os.path.join(dirfil, namefil)


# print(Resize_image(image))
