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
    
    # nombre del fichero
    #filename="lena.bmp"
    #filename="lena_mas.bmp"
    #filename="lena_menos.bmp"
    
    #filename="cantinflas.jpg"
    #filename="cantinflas_mas.jpg"
    #filename="cantinflas_menos.jpg"
    #filename="paisaje.jpg"
    filename="paisaje_mas.jpg"
    

    # lectura de la imagen  en color
    #------------------------------
    img = cv2.imread(folder+"/"+filename,cv2.IMREAD_COLOR)
    B, G, R = cv2.split(img)
    cv2.imshow("challenge MM RGB", img)
    

    #cierra la imagen    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #mecanismo de lock END
    #-----------------------
    os.remove(folder+"/"+"lock") 
    
    #procesamiento
    #calcula la proporcion de pixeles de cada componente que predominan
    #sobre los demas. la proporcion es casi independiente del brillo.
    
    height,width,channels=img.shape
    print ("shape:", height,width,channels)
    r_total=0
    g_total=0
    b_total=0
    brillo_total=0
    for y in range(height):
        for x in range(width):
            b,g,r=img[y][x]
            if (r>=g and r>=b):
                r_total+=1 # sumamos un pixel, no su brillo
            if (g>=r and g>=b):
                g_total+=1 # sumamos un pixel, no su brillo
            if (b>=g and b>=r):
                b_total+=1 # sumamos un pixel, no su brillo
            #img[y][x]=b,g,r
    print ("totales",r_total,g_total,b_total)
    tamano=height*width
    print ("brillo medio=",(brillo_total/(3*height*width)))
    r_ratio=round(10*(r_total/tamano))
    g_ratio=round(10*(g_total/tamano))
    b_ratio=round(10*(b_total/tamano))
    print ("ratios",r_ratio,g_ratio,b_ratio)

    #topamos en 9 para obtener desde 000 hasta 999 ( podria llegar a 10)
    r_ratio=min(9,r_ratio)
    g_ratio=min(9,g_ratio)
    b_ratio=min(9,b_ratio)

    #cierre 
    #cv2.waitKey(0)        
    #cv2.destroyAllWindows()

    #construccion de la respuesta
    cad="%d%d%d"%(r_ratio,g_ratio,b_ratio)
    key = bytes(cad,'utf-8')
    key_size = len(key)
    result =(key, key_size)
    print ("result:",result)
    return result


if __name__ == "__main__":
    midict={"param1": "Por favor haz una captura de la imagen que visualizas en la pantalla de la pared", "param2":3}
    init(midict)
    #executeChallenge()

