

from PIL import Image
import numpy as np


img_path = 'C:/Users/Jochen/New folder (2)/daryll.jpg'

image = Image.open(img_path)


ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, new_width=900):
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def grayify(image):
    grayscale_image = image.convert("L")
    return grayscale_image


def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return characters


def image_to_ascii(image, new_width=900):
    image = resize_image(image)
    image = grayify(image)

    pixels = image.getdata()

    ascii_str = ''
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // 25]
    img_width = image.width
    
    ascii_str_len = len(ascii_str)
    ascii_img=""
    
    
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"

   
    with open("C:\\Users\\Jochen\\New folder (2)\\ascii_image.txt", "w") as f:
        f.write(ascii_img)
    return "/mnt/data/ascii_image.txt"


ascii_result = image_to_ascii(image, new_width=900)
ascii_result
