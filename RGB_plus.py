from math import log10, sqrt
import cv2
# para instalar la libreria openCV simplemente:
# pip3 install opencv-python
# o bien py -m pip install opencv-python
# para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial
import numpy as np
import os
from pathlib import Path
import time
#para instalar el modulo easygui simplemente:
#pip3 install easygui
# o bien py -m pip install easygui
#import easygui
from tkinter import messagebox
import lock

# variables globales
# ------------------
props_dict={}
DEBUG_MODE=True

def init(props):
    global props_dict
    print("Python: Enter in init")
    
    #props es un diccionario
    props_dict= props
    
    # retornamos un cero como si fuese ok, porque
    # no vamos a ejecutar ahora el challenge
    return 0 # si init va mal retorna -1 else retorna 0
    

def executeChallenge():
    print("Starting execute")
    #for key in os.environ: print(key,':',os.environ[key]) # es para ver variables entorno
    folder=os.environ['SECUREMIRROR_CAPTURES']
    print ("storage folder is :",folder)
    
    # mecanismo de lock BEGIN
    # -----------------------
    lock.lockIN("RGBplus")

    # pregunta si el usuario tiene movil con capacidad foto
    # -----------------------------------------------------
    #textos en español, aunque podrian ser parametros adicionales del challenge
    #conexion=easygui.ynbox('¿Tienes un movil con bluetooth activo y cámara emparejado con tu PC?',"challenge MM: RGB", choices=("Yes","Not"))
    conexion=messagebox.askyesno('challenge MM: RGB','¿Tienes un movil con bluetooth activo y cámara emparejado con tu PC?')
    print(conexion)
    #Si el usuario responde que no ha emparejado móvil y PC, devolvemos clave y longitud 0
    if (conexion==False):
        lock.lockOUT("RGBplus")
        print ("return key zero and long zero")
        key=0
        key_size=0
        result =(key,key_size)
        print ("result:",result)
        return result # clave cero, longitud cero
    
    #popup msgbox pidiendo interaccion
    #---------------------------------
    #sent=easygui.ynbox(props_dict["interactionText"], "challenge MM: RGB", choices=("Yes","Not"))
    sent=conexion=messagebox.askyesno('challenge MM: RGB',props_dict['interactionText'])
    print(sent)

    #Si el usuario responde que no ha enviado la imagen, devolvemos clave y longitud 0
    if (sent== False):
        lock.lockOUT("RGBplus")
        print ("return key zero and long zero")
        key=0
        key_size=0
        result =(key,key_size)
        print ("result:",result)
        return result # clave cero, longitud cero
    
    # imagen de intranet complementaria a la foto de usuario
    # ------------------------------------------------------
    #cargamos una imagen de un servidor fijo, la url podria ser un parametro
    filename_url=props_dict["NetworkImage"] 
    cap = cv2.VideoCapture(filename_url)
    
    if( cap.isOpened() ) :
        ret,remoteImg = cap.read()
        if (DEBUG_MODE==True): #mostramos imagenes en modo debug
            cv2.imshow("image",remoteImg)
    #cv2.waitKey()
    rheight,rwidth,rchannels=remoteImg.shape
    
    # lectura de la imagen  en color
    #-------------------------------
    # se supone que el usuario ha depositado un .jpg usando bluetooth
    # el nombre de la foto puede ser siempre el mismo, fijado por el proxy bluetooth.
    # aqui vamos a "forzar" el nombre del fichero para pruebas
    filename="capture.jpg"
    if (DEBUG_MODE==True):
        #filename="lena.bmp"
        #filename="lena_mas.bmp"
        #filename="lena_menos.bmp"

        #filename="kodim07.bmp"
        #filename="kodim07_mas.bmp"
        #filename="kodim07_menos.bmp"
    
        #filename="cantinflas.jpg"
        #filename="cantinflas_mas.jpg"
        #filename="cantinflas_menos.jpg"
    
        filename="paisaje.jpg"
        #filename="paisaje_mas.jpg"
        #filename="paisaje_menos.jpg"

    if os.path.exists(folder+"/"+filename):    
        img = cv2.imread(folder+"/"+filename,cv2.IMREAD_COLOR)
    else:
        print ("ERROR: el fichero de captura",filename," no existe")
        key=0
        key_size=0
        result =(key,key_size)
        print ("result:",result)
        lock.lockOUT("RGBplus")
        return result # clave cero, longitud cero
    
    # una vez consumida, podemos borrar la captura (fichero "capture.jpg")
    if (DEBUG_MODE==False):
        if os.path.exists(folder+"/"+filename):    
            os.remove(folder+"/"+filename)
        
    if (DEBUG_MODE==True): #mostramos imagenes en modo debug
        cv2.imshow("challenge MM RGBplus", img)
    
    
    #mecanismo de lock END
    #-----------------------
    lock.lockOUT("RGBplus")
    
    #procesamiento
    #calcula la proporcion de pixeles de cada componente que predominan
    #sobre los demas. la proporcion es casi independiente del brillo.
    
    height,width,channels=img.shape
    print ("shape:", height,width,channels)
    r_total=0
    g_total=0
    b_total=0
    proporcion=height/width

    # hacemos un analisis con mitad de una imagen y mitad de la otra
    # lo he hecho en diagonal pero podria hacerse en vertical, horizontal, etc
    for y in range(height):
        for x in range(width):
            if (x*proporcion>y): #porcion triangular
                b,g,r=img[y][x] 
                
            else: # la otra porcion la cogemos de la otra imagen
                ry=int(y*(rheight/height))
                rx=int(x*(rwidth/width))
                b,g,r=remoteImg[ry][rx]
                
            if (r>=g and r>=b):
                r_total+=1 # sumamos un pixel, no su brillo
            if (g>=r and g>=b):
                g_total+=1 # sumamos un pixel, no su brillo
            if (b>=g and b>=r):
                b_total+=1 # sumamos un pixel, no su brillo
            img[y][x]=b,g,r

    if (DEBUG_MODE==True):        
        cv2.imshow("RGBplus", img)

    print ("totales",r_total,g_total,b_total)
    tamano=height*width
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
    midict={"interactionText": "¿Has enviado la imagen desde el móvil a tu PC?", "param2":3 , "NetworkImage": "https://pics.filmaffinity.com/the_pink_panther-805664537-large.jpg"}
    init(midict)
    executeChallenge()

