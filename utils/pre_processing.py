import cv2
import numpy as np
from PIL import Image

# https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
# https://nanonets.com/blog/ocr-with-tesseract/
# https://github.com/TCAT-capstone/ocr-preprocessor/blob/main/main.py
# https://towardsdatascience.com/pre-processing-in-ocr-fc231c6035a7
# == Main ======================================================================
def load(path):
    return cv2.imread(path)

def image_filter(image):
    image = grayscale(image)
    # image = thresholding(image, mode="GAUSSIAN")
    # image = opening(image)
    # image = closing(image)
    return image

def roi_filter(image):
    image = resize(image)
    return image

def load_with_filter(path):
    image = load(path)
    return image_filter(image)

def isEven(num):
    return num % 2 == 0

# == Color =====================================================================
def grayscale(image, blur=False):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# https://opencv-python.readthedocs.io/en/latest/doc/09.imageThresholding/imageThresholding.html
def thresholding(image, mode="GENERAL",block_size=9, C=5):
    if isEven(block_size):
        print("block_size to use odd")
        return;

    if mode == "MEAN":
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)
    elif mode == "GAUSSIAN":
        return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
    else:
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def equalization(image):
    return cv2.equalizeHist(image)

# == Noise =====================================================================
def remove_noise(image, kernel_size=3):
    return cv2.medianBlur(image, ksize=kernel_size)

def blur(image, kernel=(3,3)):
    return cv2.GaussianBlur(gray, kernel, 0)

# == Morphology ================================================================
def dilation(image, kernel=np.ones((3,3),np.uint8)):
    return cv2.dilate(image, kernel, iterations = 1)

def erosion(image, kernel=np.ones((3,3),np.uint8)):
    return cv2.erode(image, kernel, iterations = 1)

def opening(image, kernel=np.ones((3,3),np.uint8)):
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def closing(image, kernel=np.ones((3,3),np.uint8)):
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def canny(image):
    return cv2.Canny(image, 100, 200)

# == Others ====================================================================
def resize(image, interpolation=cv2.INTER_CUBIC):
    height, width = image.shape
    factor = max(1, 20.0/ height)
    size = (int(factor * width), int(factor * height))
    return cv2.resize(image, dsize=size, interpolation=interpolation)

# https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)