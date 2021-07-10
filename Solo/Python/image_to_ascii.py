import os
import PIL.Image

os.path.join(os.getcwd())

gray_scale1 = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`". '
gray_scale2 = "@%#*+=-:. "

def get_image():
    while True:
        path = input("Mueva la imagen al mismo directorio que este archivo e ingrese su nombre y su formato:\n")

        try:
            imagen = PIL.Image.open(path)
            return imagen
        except Exception as e:
            print("No se puede encontrar ese nombre de archivo. Intente de nuevo." + str(e))

def resize_image(image, new_w = 256):
    w, h = image.size
    aspect_ratio = h / w / 1.65
    new_h = int(new_w * aspect_ratio)
    return image.resize((new_w, new_h))

def grayify_image(image):
    return image.convert("L")

def ascii_image(image, new_w):
    new_image = grayify_image(resize_image(image, new_w))
    pixels = new_image.getdata()

    if new_w > 100:
        image_string = "".join(gray_scale1[int(pixel//3.8)] for pixel in pixels)
    else:
        image_string = "".join(gray_scale2[int(pixel//28.3)] for pixel in pixels)
    
    return image_string

def main():
    imagen = get_image()
    
    try:
        new_w = int(input("Ingrese el ancho en pixeles deseado de la imagen. Default es 256.\n"))
    except:
        new_w = 256

    new_image = ascii_image(imagen, new_w)

    pixels = len(new_image)
    final_ascii = "\n".join(new_image[i:(i + new_w)] for i in range(0, pixels, new_w))

    with open("ascii_images.txt", "a") as outfile:
        outfile.write(final_ascii)
        outfile.close()
    
    print("La imagen se convirtió exitosamente.")
    input()

if __name__ == "__main__":
    main()