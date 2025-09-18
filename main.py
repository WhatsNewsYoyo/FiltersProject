import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract


#Functions to add
def checkColor(image):
    i = 0;
    return i
    
    
    
def checkVertex(image):
    img = cv2.imread(images[i])
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(img_gray, (5,5), 1)
    
    
    plt.imshow(cv2.cvtColor(gaussian, cv2.COLOR_BGR2RGB))
    plt.title("Gaussian and gray scale")
    plt.axis('off')
    plt.show()
    return 0    



images = ["dangerSign.jpg", "stopSign.jpg", "WheelchairSign.png"]
n = len(images)
for i in range (0,n) :
    checkVertex(i)