"# ChallengeMM_RGB" 
# ChallengeMM_RGB

Este challenge analiza las proporciones de R,G,B en una imagen capturada y retorna una tupla r,g,b
es independiente de las condiciones de iluminacion pues los valores se normalizan al brillo total
para probar se incluyen varias imagenes (3 de lena a distinto brillo y otras dos)
el challenge implementa el mecanismo de lock para que solo un challenge multimedia pida interaccion a la vez

# requisitos:
la variable de entorno SECUREMIRROR_CAPTURES debe existir y apuntar al path donde el server bluetooth deposita las capturas

para instalar la libreria openCV simplemente:

pip3 install opencv-python

para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial

para instalar el modulo easygui simplemente:

pip3 install easygui
