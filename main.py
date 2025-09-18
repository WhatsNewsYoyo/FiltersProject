import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract


#Functions to add
def checkColor(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    yellow = cv2.inRange(hsv, np.array([20,50,50]), np.array([35,255,255]))
    blue = cv2.inRange(hsv, np.array([100,150,50]), np.array([140,255,255]))
    red1 = cv2.inRange(hsv, np.array([0,50,50]), np.array([10,255,255]))
    red2 = cv2.inRange(hsv, np.array([160,50,50]), np.array([179,255,255]))
    red = cv2.bitwise_or(red1, red2)
    return {"yellow": yellow, "red": red, "blue": blue}

def mask_has_color(mask, area_frac=0.005):
    """
    Comprueba si una máscara contiene suficiente cantidad de píxeles,
    usando solo un umbral proporcional al tamaño de la imagen.
    - area_frac: fracción del área total que debe cubrir el color (ej. 0.005 = 0.5%).
    """
    nz = cv2.countNonZero(mask)
    total = mask.shape[0] * mask.shape[1]
    threshold = max(1, int(area_frac * total))  # umbral proporcional, al menos 1 píxel
    return nz >= threshold

def masks_exist(masks, area_frac=0.005):
    """
    Aplica mask_has_color_proportional a cada máscara del dict y devuelve
    un dict {nombre: True/False}.
    """
    return {name: mask_has_color(mask, area_frac) for name, mask in masks.items()}
    
def checkVertex(image):
    i = 0
    



images = ["dangerSign.jpg", "stopSign.jpg", "WheelchairSign.png", "PruebaIcono.jpg", "ImagenJunta.png"]
n = len(images)
for i in range (0,n) :
    img = cv2.imread(images[i])
    
    masks = checkColor(img)
    exists = masks_exist(masks)
    for k, v in exists.items():
        print(f"  {k}: {v}")

    plt.figure(figsize=(9,3))
    for i, name in enumerate(("yellow","red","blue"), 1):
        plt.subplot(1,3,i)
        plt.title(name)
        plt.imshow(masks[name], cmap="gray")
        plt.axis("off")
    plt.tight_layout()
    plt.show()
