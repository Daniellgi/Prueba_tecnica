from GUI.ui_login import *
import cv2
import numpy as np
from GUI.ventana2 import Ventana_dos
from Predicciones.predicciones import Prediccion,Predicciones

class VentanaLog(QtWidgets.QMainWindow):
    def __init__(self,conn_api, predicciones_app):
        self.conn_api = conn_api
        self.predicciones_app = predicciones_app
        super().__init__()
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)
        self.ui.bt_ingresar.clicked.connect(self.iniciar_sesion)
        self.ventana = Ventana_dos(self.conn_api,self.predicciones_app)
        
    def iniciar_sesion(self):
        self.ui.contrasena_incorrecta.setText('')
        self.ui.usuario_incorrecto.setText('')
        users_entry = self.ui.users.text()
        password_entry = self.ui.password.text()

        users_entry = str(users_entry)
        password_entry = str(password_entry)

        usuario_existe, prediccions, imagenes = self.conn_api.login(users_entry,password_entry)
        print(f"Prediccion: {prediccions}")
        if usuario_existe and len(prediccions)>0:
            for prediccion, imagen in zip(prediccions, imagenes):
                #cv2.imshow("Imagen_anterior",imagen)
                #cv2.waitKey(0)
                print(prediccion)
                prediccion_app = Prediccion(prediccion[0],prediccion[1],imagen,self.ventana.ventana)
                self.predicciones_app.add_prediccion(prediccion_app)
            cv2.destroyAllWindows()
        else:
            pass
    
        if (usuario_existe==False):
            self.ui.contrasena_incorrecta.setText('Contraseña incorrecta')
            self.ui.usuario_incorrecto.setText('Usuario incorrecto')

        elif(usuario_existe==True):
            self.hide()
            self.ventana.show()
            self.ventana.actualizar_tabla()
        else:
            self.ui.contrasena_incorrecta.setText('')
            self.ui.usuario_incorrecto.setText('Error conectando con la API')