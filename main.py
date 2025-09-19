import cv2
import numpy as np
import matplotlib.pyplot as plt


#Functions to add
def checkColor(image):
    """
    Calcula máscaras HSV para amarillo, rojo y azul a partir de una imagen BGR.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    yellow = cv2.inRange(hsv, np.array([20,50,50]), np.array([35,255,255]))
    blue = cv2.inRange(hsv, np.array([100,150,50]), np.array([140,255,255]))
    red1 = cv2.inRange(hsv, np.array([0,50,50]), np.array([10,255,255]))
    red2 = cv2.inRange(hsv, np.array([160,50,50]), np.array([179,255,255]))
    red = cv2.bitwise_or(red1, red2)
    return {"yellow": yellow, "red": red, "blue": blue}

def mask_has_color(mask, area_frac=0.005):
    """
    Comprueba si una máscara contiene suficiente cantidad de píxeles, usando solo un umbral proporcional al tamaño de la imagen.
    """
    nz = cv2.countNonZero(mask)
    total = mask.shape[0] * mask.shape[1]
    threshold = max(1, int(area_frac * total))  # umbral proporcional, al menos 1 píxel
    return nz >= threshold

def masks_exist(masks, area_frac=0.005):
    """
    Aplica mask_has_color_proportional a cada máscara del dict y devuelve un dict {nombre: True/False}.
    """
    return {name: mask_has_color(mask, area_frac) for name, mask in masks.items()}
    
"""
Esta función cuenta los vértices de la figura más grande presente en una imagen. 
Para ello, primero convierte la imagen a escala de grises y aplica un umbral (threshold) que aísla el contorno de la figura. 
Posteriormente identifica el contorno de mayor tamaño, calcula su perímetro y, con estos datos, determina de manera aproximada el número de vértices de la figura.
"""    
def checkVertex(image):
    #Leer imagen cargada
    img = cv2.imread(image)
    
    #Conversión a gray scale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Compara los pixeles para volverlos blancos o negros dependiendo de su valor.
    _, thresh = cv2.threshold(img_gray, 240, 255, cv2.CHAIN_APPROX_NONE)
    
    #Regresa todos los contornos en la imagen
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    #La figura con mayor contorno es la que tomaremos como la principal de la imagen para regresar sus vertices
    contour = max(contours, key=cv2.contourArea)
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)       
    num_vertices = len(approx)
    print(f"Vertex numbers : {num_vertices}")
    
    return num_vertices


images = ["dangerSign.jpg", "stopSign.jpg", "WheelchairSign.png", "PruebaIcono.jpg", "group.png", "groupYSign.png"]
n = len(images)
#Ciclo principal para que analice cada imagen
for i in images:
    num_vertices = checkVertex(i)    
    img = cv2.imread(i)
    masks = checkColor(img)
    exists = masks_exist(masks)
    detected_sign = None
    
    #Comparativa entre colores y vertices para verificar que simbolo es.
    if exists["red"] and num_vertices == 8:
        detected_sign = "Stop sign"
    elif exists["yellow"] and num_vertices == 3:
        detected_sign = "Danger sign"
    elif exists["blue"] and num_vertices == 4:
        detected_sign = "Wheelchair sign"
    
    if all(exists[c] for c in ["blue", "yellow", "red"]) and num_vertices in [3, 4, 8]:
        detected_sign = "Multiple signs!"
        
    for k, v in exists.items():
        print(f"  {k}: {v}")
    if detected_sign:
        print(f"Detected sign: {detected_sign}\n")
    else:
        print("Detected sign: Unknown\n")
        
    plt.figure(figsize=(1,4))
    plt.subplot(1,4,1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    
    for i, name in enumerate(("yellow","red","blue"), 1):
        plt.subplot(1,4,i+1)
        plt.title(name)
        plt.imshow(masks[name], cmap="gray")
        plt.axis("off")
 
        
    plt.tight_layout()
    plt.show()
