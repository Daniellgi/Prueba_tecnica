
import requests
import json
import cv2
import numpy as np
from Utils.utils import decodificar_imagen,codificar_imagen

class Conectar_API:
    def __init__(self):
        self.password = ""
        self.usuario = ""
        self.usuario_existe = None

    def login(self,users,password):
        prediccions = []
        lista_imagenes = []
        try:
            dictionary_detection = {
                "usuario" : users,
                "password" : password}

            text_json = json.dumps(dictionary_detection).encode('utf-8')
            response = requests.post("http://127.0.0.1:8000/login/", data=text_json)
            data_rec = response.json()
            self.usuario_existe = data_rec['usuario_existe']

            if self.usuario_existe==True:
                for prediccion in data_rec['predictions']:
                    prediccions.append((prediccion['fecha'], prediccion['prediccion']))
                    decimg = decodificar_imagen(prediccion['imagen'])
                    lista_imagenes.append(decimg)

                print(f"Predicciones anteriores: {prediccions}")
                self.usuario = users
                self.password =password
            else:
               prediccions = [] 
               lista_imagenes = []

        except:
            self.usuario_existe = None

        return self.usuario_existe, prediccions, lista_imagenes

    def prediccion(self,image):
        decimg = None
        prediccions = []
        try:
            img_byte = codificar_imagen(image)
            
            dictionary_detection = {
                "usuario" : self.usuario,
                "password" : self.password,
                "image":img_byte}

            text_json = json.dumps(dictionary_detection).encode('utf-8')
            response = requests.post("http://127.0.0.1:8000/prediccion/", data=text_json)
            data_rec = response.json()
            
            self.usuario_existe = data_rec['usuario_existe']
            if self.usuario_existe==True:
                prediccions.append((data_rec['prediction'][0]['fecha'],data_rec['prediction'][0]['prediccion']))
                decimg = decodificar_imagen(data_rec['prediction'][0]['imagen'])
                #cv2.imshow("Image_decodificada",decimg)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()

            else:
               print("Contraseña y/ó Usuario erroneo")
        except Exception as e:
            print(f"Error: {e}")
            self.usuario_existe = None
        return self.usuario_existe, prediccions, decimg