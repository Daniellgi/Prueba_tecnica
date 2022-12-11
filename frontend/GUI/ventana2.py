from GUI.ui_vista1 import*
import cv2
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QImage
import numpy as np
from Predicciones.predicciones import Prediccion,Predicciones
from Conexion_API.conexion_api import Conectar_API

class Ventana_dos(QtWidgets.QMainWindow):
    def __init__(self,conn_api, predicciones_app):
        super().__init__()
        self.direccion = ""
        self.conn_api = conn_api
        self.predicciones_app = predicciones_app
        self.ventana = Ui_Vista1() 
        self.ventana.setupUi(self)
        self.ventana.nueva_prediccion.clicked.connect(self.prediccion)

        add_button = QtWidgets.QPushButton("Prueba")
        self.ventana.tabla_predicciones.setCellWidget(0, 0, add_button)
    
    def prediccion(self):
        try:
            file = QFileDialog.getOpenFileName(filter="Images (*.png *.jpg")
            self.direccion = file[0]
            print(self.direccion)
            image = cv2.imread(self.direccion)
            usuario_existe, prediccions, imagen_prediccion = self.conn_api.prediccion(image)
            print(f"Prediccion: {prediccions}")
            if usuario_existe and len(prediccions)>0:
                prediccion_app = Prediccion(prediccions[0][0],prediccions[0][1],imagen_prediccion,self.ventana)
                self.predicciones_app.add_prediccion(prediccion_app)
                h,w,_ = imagen_prediccion.shape
                print(h,w)
                r=h/w
                imagen_prediccion = cv2.resize(imagen_prediccion,(400,int(400*r)))
                frame = cv2.cvtColor(imagen_prediccion, cv2.COLOR_BGR2RGB)
                imagen_prediccion = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
                self.ventana.mostrar_imagen.setPixmap(QtGui.QPixmap.fromImage(imagen_prediccion))
                self.actualizar_tabla()
            else:
                pass
        except Exception as e:
            print(f"Error al hacer la predicción: {e}")

    def actualizar_tabla(self):
        
        predicciones = self.predicciones_app.get_predicciones()
        x=3
        y= len(predicciones)
        columnas = ['Imagen','Fecha','Predicción']
        self.ventana.tabla_predicciones.setRowCount(y)
        self.ventana.tabla_predicciones.setColumnCount(x)

        for j in range(x):
            encabezado = QtWidgets.QTableWidgetItem(columnas[j])
            self.ventana.tabla_predicciones.setHorizontalHeaderItem(j,encabezado)
        for i, prediccion in enumerate(predicciones):
            
            add_button = prediccion.boton_mostrar_imagen
            self.ventana.tabla_predicciones.setCellWidget(i,0, add_button)
            
            fecha = str(prediccion.fecha)
            etiquetas_prediccion = str(prediccion.lista_etiquetas)
            self.ventana.tabla_predicciones.setItem(i,1, QTableWidgetItem(fecha))
            self.ventana.tabla_predicciones.setItem(i,2, QTableWidgetItem(etiquetas_prediccion))