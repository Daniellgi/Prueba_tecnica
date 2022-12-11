import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
import numpy as np

class Prediccion:
    def __init__(self, fecha, lista_etiquetas, imagen, ventana_padre_botton):
        self.fecha = fecha
        self.lista_etiquetas = lista_etiquetas
        self.imagen = imagen
        self.ventana_padre_botton = ventana_padre_botton
        self.boton_mostrar_imagen = QtWidgets.QPushButton("Mostrar Imagen")
        self.boton_mostrar_imagen.clicked.connect(self.mostrar_imagen)

    def mostrar_imagen(self):
        h,w,_ = self.imagen.shape
        print(h,w)
        r=h/w
        #cv2.imshow("imagen mostrar",self.imagen)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        imagen_prediccion = cv2.resize(self.imagen,(400,int(400*r)))
        frame = cv2.cvtColor(imagen_prediccion, cv2.COLOR_BGR2RGB)
        imagen_prediccion = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.ventana_padre_botton.mostrar_imagen.setPixmap(QtGui.QPixmap.fromImage(imagen_prediccion))
        
class Predicciones:
    def __init__(self):
        self.predicciones = []
    
    def add_prediccion(self, prediccion):
        self.predicciones.append(prediccion)
    
    def set_predicciones(self, predicciones):
        self.predicciones = predicciones
    def get_predicciones(self):
        return self.predicciones