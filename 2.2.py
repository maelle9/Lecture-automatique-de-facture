import numpy as np
import cv2
import matplotlib.pyplot as plt

def display_image (path):
    image = Image.open(path)
    plt.imshow(image)
    plt.show()

def display_image_2 (path):
    image = cv2.imread(path)
    plt.imshow(image)
    plt.show()

def image (path):
    return cv2.imread(path)

def opencv_resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def plot_gray(image):
    plt.figure(figsize=(16, 10))
    return plt.imshow(image, cmap='Greys_r')

path = "data\sample.jpg"

src = cv2.imread(path)
Color = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
Resize = opencv_resize(Color, 450 / Color.shape[0])
Blur = cv2.GaussianBlur(Resize,(3,3),0)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
Struct = cv2.dilate(Blur,kernel,iterations = 2)
image = cv2.Canny(Struct,100,100,apertureSize=3)
plot_gray(image)
plt.show()
