from math import log10, sqrt
import cv2
# para instalar la libreria openCV simplemente:
# pip3 install opencv-python
# para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial
import numpy as np
import os
from pathlib import Path

#para instalar el modulo easygui simplemente:
#pip3 install easygui
from easygui import *

import time

props_dict={} 

def init(props):
    global props_dict
    print("Python: Enter in init")
    
    #props es un diccionario
    props_dict= props
    executeChallenge()
    return 0



def executeChallenge():
    print("Starting execute")
    #for key in os.environ: print(key,':',os.environ[key])
    folder=os.environ['SECUREMIRROR_CAPTURES']
    print ("storage folder is :",folder)

    
    #popup pidiendo interaccion

    #img = cv2.imread(folder+"/"+"ask_interaction.png",cv2.IMREAD_COLOR)
    #cv2.imshow("challenge MM RGB", img)
    #cv2.waitKey(0)

    #mecanismo de lock BEGIN
    #-----------------------
    while os.path.exists(folder+"/"+"lock"):
        time.sleep(1)
    Path(folder+"/"+"lock").touch()
    
    #popup msgbox pidiendo interaccion
    #---------------------------------
    output = msgbox(props_dict["param1"], "challenge MM: RGB")
    
    # lectura de una imagen  en color
    #img = cv2.imread("lena.bmp",cv2.IMREAD_COLOR)
    #img = cv2.imread("lena_mas.bmp",cv2.IMREAD_COLOR)
    #img = cv2.imread("lena_menos.bmp",cv2.IMREAD_COLOR)
    #img = cv2.imread("paisaje.jpg",cv2.IMREAD_COLOR)
    img = cv2.imread(folder+"/"+"cantinflas.jpg",cv2.IMREAD_COLOR)
    B, G, R = cv2.split(img)
    cv2.imshow("challenge MM RGB", img)
    cv2.waitKey(0)
    """
    cv2.imshow("blue", B)
    cv2.waitKey(0)
 
    cv2.imshow("Green", G)
    cv2.waitKey(0)
 
    cv2.imshow("red", R)
    cv2.waitKey(0)
    """    
    cv2.destroyAllWindows()
    
    #mecanismo de lock END
    #-----------------------
    os.remove(folder+"/"+"lock") 
    
    #procesamos
    height,width,channels=img.shape
    print ("shape:", height,width,channels)
    r_total=0
    g_total=0
    b_total=0
    for y in range(height):
        for x in range(width):
            b,g,r=img[y][x]
            r_total+=r
            g_total+=g
            b_total+=b
            #img[y][x]=b,g,r
    print ("totales",r_total,g_total,b_total)
    brillo_total=r_total+g_total+b_total
    r_ratio=int(10*(r_total/brillo_total))
    g_ratio=int(10*(g_total/brillo_total))
    b_ratio=int(10*(g_total/brillo_total))
    print ("ratios",r_ratio,g_ratio,b_ratio)
    #cv2.imshow("challenge MM RGB", img)
    #cv2.imwrite(filename, img)
    cv2.waitKey(0)        
    cv2.destroyAllWindows()
    cad="%d%d%d"%(r_ratio,g_ratio,b_ratio)
    #construccion de la respuesta
    key = bytes(cad,'utf-8')
    key_size = len(key)
    result =(key, key_size)
    print ("result:",result)
    return result


if __name__ == "__main__":
    midict={"param1": "Por favor haz una captura de la imagen que visualizas en la pantalla de la pared", "param2":3}
    init(midict)
    #executeChallenge()

