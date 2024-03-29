# ChallengeMM_RGB y RGBplus

# DESCRIPCION y FIABILIDAD
RGB y RGBplus son dos challenges que piden al usuario hacer una foto para comprobar que se encuentra en un lugar concreto
el challenge RGBplus combina la foto con otra que se obtiene de la intranet, de modo que la imagen final es una combinacion de ambas
el RGB tiene una fiabilidad media porque el usuario puede tener una foto almacenada. El **RGB plus tiene alta fiabilidad** porque es imposible conocer las dos imagenes

# FUNCIONAMIENTO:
Este challenge analiza las proporciones de R,G,B en una imagen capturada y retorna una tupla r,g,b
es independiente de las condiciones de iluminacion pues calcula CUANTOS pixeles tienen la R mas grande, cuantos la G y cuantos la R
Con esas 3 medidas hace una proporción respecto al tamaño y como no se usa el brillo, es casi independiente del brillo de la imagen.

hay dos formas en la que un pixel deja de sumarse o empieza a sumarse:
- Para un pixel dado, si R>=G>=B , entonces se suma 1.  En la versión con mas o menos brillo, dicha condición se sigue cumpliendo a menos que se llegue a la saturación (255) pero incluso en ese caso el primero que llega es R y se seguirá cumpliendo, lo que ocurre es que en ese momento también se cumplirá G>=R>=B. 

- Al bajar el brillo puede ocurrir que dos componentes que valen respectivamente 201 y 200 se igualen , por ejemplo valiendo ambos 100.

Si el numero de pixeles donde se llega a la saturación o se igualan de repente dos componentes no es muy grande, el porcentaje total se sigue manteniendo. Es decir, es muy robusto

La clave resultante va desde 000 hasta 999.
Es un porcentaje en tramos de 10%, hay mucho margen de variación sin cambio en el resultado pero a pesar de todo podría existir alguna imagen muy sensible que tenga una proporción muy cercana al final de un intervalo en una de las componentes pero serían casos muy especiales y habría que oscurecer o abrillantar mucho para conseguir cambiar el porcentaje significativamente


# requisitos:
la variable de entorno **SECUREMIRROR_CAPTURES** debe existir y apuntar al path donde el server bluetooth deposita las capturas
el fichero de captura se debe llamar "capture.jpg".

Hay una variable en el challenge (en ambos challenges) llamada **"DEBUG_MODE"** que la puedes cambiar a True o False. En caso True en lugar del fichero capture.jpg se usa paisaje.jpg y ademas no se borra el fichero capture.jpg despues de procesar. Otra caracteristica de DEBUG_MODE=True es que muestra las imagenes en pantalla (molestando un poco, claro)
En caso DEBUG_MODE=fase, se usa "capture.jpg" y ademas la imagen se borra tras el procesamiento

para instalar la libreria openCV simplemente:

pip3 install opencv-python

IMPORTANTE: tras instalar opencv, la dll python3.dll de instalacion de python cambia, debes darle acceso al programa que haga uso de este challenge ubicandola en un directorio al que pueda acceder

para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial

para instalar el modulo easygui simplemente:

pip3 install easygui

para aprender easygui https://www.geeksforgeeks.org/python-easygui-module-introduction/

configuracion de ejemplo json para RGBplus:

```
{
  "FileName": "challenge_loader_python.dll",
  "Description": "challenge RGBplus para asegurar localizacion",
  "Props": {
    "module_python": "RGB_plus",
    "validity_time": 3600,
    "refresh_time": 10,
    "interactionText": "Por favor haz una captura de la imagen que visualizas en la pantalla de la pared",
    "NetworkImage": "https://pics.filmaffinity.com/the_pink_panther-805664537-large.jpg"
},
"Requirements": "camera" 
}

```
configuracion de ejemplo json para RGB
```
{
  "FileName": "challenge_loader_python.dll",
  "Description": "challenge RGB para asegurar localizacion",
  "Props": {
    "module_python": "RGB",
    "validity_time": 3600,
    "refresh_time": 10,
    "interactionText": "Por favor haz una captura de la imagen que visualizas en la pantalla de la pared",
   },
"Requirements": "camera" 
}
```




