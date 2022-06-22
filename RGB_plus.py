from math import log10, sqrt
import cv2
# para instalar la libreria openCV simplemente:
# pip3 install opencv-python
# para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial
import numpy as np
import os
from pathlib import Path
import time
#para instalar el modulo easygui simplemente:
#pip3 install easygui
import easygui

# variables globales
# ------------------
props_dict={}
DEBUG_MODE=False

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

    # mecanismo de lock BEGIN
    # -----------------------
    while os.path.exists(folder+"/"+"lock"):
        time.sleep(1)
    Path(folder+"/"+"lock").touch()

    # pregunta si el usuario tiene movil con capacidad foto
    # -----------------------------------------------------
    #textos en español, aunque podrian ser parametros adicionales del challenge
    capable=easygui.ynbox(msg='¿Tienes un movil con bluetooth activo y \
emparejado con tu PC con capacidad para hacer una foto?', choices=("Yes","Not"))
    print (capable)
    #capable=easygui.buttonbox('¿Tienes un movil con bluetooth activo y \
    #emparejado con tu PC con capacidad para hacer una foto?', 'RGB plus', ('SI', 'NO'))
    if (capable==False):
        os.remove(folder+"/"+"lock")
        return 0,0 # clave cero, longitud cero
    
    #popup msgbox pidiendo interaccion
    #---------------------------------
    output = easygui.msgbox(props_dict["param1"], "challenge MM: RGB")

    
    # nombre del fichero para pruebas (a modo de foto tomada por el usuario)
    # ----------------------------------------------------------------------
    # una vez consumida la foto, debe de borrarse
    #filename="lena.bmp"
    #filename="lena_mas.bmp"
    #filename="lena_menos.bmp"

    #filename="kodim07.bmp"
    #filename="kodim07_mas.bmp"
    filename="kodim07_menos.bmp"
    
    #filename="cantinflas.jpg"
    #filename="cantinflas_mas.jpg"
    #filename="cantinflas_menos.jpg"
    
    #filename="paisaje.jpg"
    #filename="paisaje_mas.jpg"
    #filename="paisaje_menos.jpg"

    # imagen de intranet complementaria a la foto de usuario
    # ------------------------------------------------------
    #cargamos una imagen de un servidor fijo, la url podria ser un parametro
    filename_url=props_dict["param3"] 
    cap = cv2.VideoCapture(filename_url)
    
    if( cap.isOpened() ) :
        ret,remoteImg = cap.read()
        #cv2.imshow("image",remoteImg)
    #cv2.waitKey()
    rheight,rwidth,rchannels=remoteImg.shape
    
    # lectura de la imagen  en color
    #-------------------------------
    # se supone que el usuario ha depositado un .jpg usando bluetooth
    # el nombre de la foto puede ser siempre el mismo, fijado por el proxy bluetooth.
    # aqui vamos a "forzar" el nombre del fichero para pruebas
    filename="captura.jpg"
    if (DEBUG_MODE==True):
        #filename="lena.bmp"
        #filename="lena_mas.bmp"
        #filename="lena_menos.bmp"

        #filename="kodim07.bmp"
        #filename="kodim07_mas.bmp"
        filename="kodim07_menos.bmp"
    
        #filename="cantinflas.jpg"
        #filename="cantinflas_mas.jpg"
        #filename="cantinflas_menos.jpg"
    
        #filename="paisaje.jpg"
        #filename="paisaje_mas.jpg"
        #filename="paisaje_menos.jpg"
        
    img = cv2.imread(folder+"/"+filename,cv2.IMREAD_COLOR)
    # una vez consumida, podemos borrar la captura
    os.remove(folder+"/"+filename) 

    
    B, G, R = cv2.split(img)
    #cv2.imshow("challenge MM RGB", img)
    

    #cierra la imagen    
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
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
    proporcion=height/width

    # hacemos un analisis con mitad de una imagen y mitad de la otra
    # lo he hecho en diagonal pero podria hacerse en vertical, horizontal, etc
    for y in range(height):
        for x in range(width):
            if (x*proporcion>y):
                b,g,r=img[y][x]
                
            else:
                ry=int(y*(rheight/height))
                rx=int(x*(rwidth/width))
                #b2,g2,r2=remoteImg[ry][rx]
                b,g,r=remoteImg[ry][rx]
                
            # la media funciona (comprobado)
            #b=(int(b)+int(b2))/2
            #g=(int(g)+int(g2))/2
            #r=(int(r)+int(r2))/2

            # max tambien funciona
            #b=max (b,b2)
            #r=max(r,r2)
            #g=max(g,g2)
            
            if (r>=g and r>=b):
                r_total+=1 # sumamos un pixel, no su brillo
            if (g>=r and g>=b):
                g_total+=1 # sumamos un pixel, no su brillo
            if (b>=g and b>=r):
                b_total+=1 # sumamos un pixel, no su brillo
            img[y][x]=b,g,r
    cv2.imshow("RGBplus", img)
    print ("totales",r_total,g_total,b_total)
    tamano=height*width
    print ("brillo medio=",(brillo_total/(3*height*width)))
    r_ratio=round(10*(r_total/tamano))
    g_ratio=round(10*(g_total/tamano))
    b_ratio=round(10*(b_total/tamano))
    print ("ratios foto",r_ratio,g_ratio,b_ratio)

    

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
    midict={"param1": "Por favor haz una captura de la imagen que visualizas en la pantalla de la pared", "param2":3 , "param3": "https://pics.filmaffinity.com/the_pink_panther-805664537-large.jpg"}
    init(midict)
    #executeChallenge()

