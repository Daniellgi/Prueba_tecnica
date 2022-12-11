import base64
import numpy as np
import cv2

def crear_lista_predicciones(predicciones):
    lista_predicciones=[]
    for prediccion in predicciones:
        img = cv2.imread(f'./Images/{prediccion[1]}.jpg')
        #cv2.imshow('Imagen_enviar',img)
        #cv2.waitKey(0)
        img_byte = codificar_imagen(img)
        diccionario_prediccion = {'fecha':prediccion[1],
                                'prediccion':prediccion[2],
                                'imagen':img_byte}

        lista_predicciones.append(diccionario_prediccion)
    #cv2.destroyAllWindows()
    return lista_predicciones
def decodificar_imagen(image_codificada):
    image_dec = base64.b64decode(image_codificada)
    data_np = np.fromstring(image_dec, dtype='uint8')
    decimg = cv2.imdecode(data_np, 1)
    return decimg

def codificar_imagen(image):
    _, encimg = cv2.imencode(".jpg ", image)
    img_str = encimg.tostring()
    img_byte = base64.b64encode(img_str).decode("utf-8")
    return img_byte