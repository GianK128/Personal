import math

WIDTH = 56

gray_scale = ['⠄','⠆','⠖','⠶','⡶','⣩','⣪','⣫','⣾','⣿']
# gray_scale = ['⠀','⠄','⠆','⠖','⠶','⡶','⣩','⣪','⣫','⣾','⣿']
threshhold = math.floor(255 / (len(gray_scale) - 1))

def resize_image(image, new_w):
    w, h = image.size
    aspect_ratio = float(h) / float(w)
    new_h = int((new_w * aspect_ratio) / 2)
    return image.resize((new_w, new_h))

def grayify_image(image):
    return image.convert("L")

def crop_image(image, new_w):
    pixels = len(image)
    final_ascii = "\n".join(image[i:(i + int(new_w))] for i in range(0, pixels, int(new_w)))

    return final_ascii

def ascii_image(image, new_w = WIDTH):
    new_image = grayify_image(resize_image(image, new_w))
    pixels = list(new_image.getdata())

    image_string = "".join([gray_scale[pixel//threshhold] for pixel in pixels])

    return crop_image(image_string, new_w)