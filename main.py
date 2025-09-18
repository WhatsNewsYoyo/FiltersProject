import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract


#Functions to add
def checkColor(image):
    i = 0;
    return i
    
    
    
def checkVertex(image):
    img = cv2.imread(image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(img_gray, (3,3), 1)

    _, thresh = cv2.threshold(img_gray, 240, 255, cv2.CHAIN_APPROX_NONE)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = max(contours, key=cv2.contourArea)
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    num_vertices = len(approx)
    print(f"Vertex numbers : {num_vertices}")


    #Screenshots for presentation
    plt.figure(figsize=(1,10))
    plt.subplot(1,3,1)
    plt.imshow(cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB))
    plt.title("Gray scale")
    plt.axis('off')

    plt.subplot(1,3,2)
    plt.imshow(cv2.cvtColor(gaussian, cv2.COLOR_BGR2RGB))
    plt.title("Gaussian and gray scale")
    plt.axis('off')
    plt.show()



images = ["dangerSign.jpg", "stopSign.jpg", "WheelchairSign.png"]
n = len(images)
for i in images:
    checkVertex(i)