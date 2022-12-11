import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from Predicciones.predicciones import Prediccion,Predicciones
from GUI.ventana_log import VentanaLog
from Conexion_API.conexion_api import Conectar_API

if __name__ == "__main__":
     app = QtWidgets.QApplication(sys.argv)
     predicciones_app = Predicciones()
     conn_api = Conectar_API()
     mi_app = VentanaLog(conn_api,predicciones_app)
     mi_app.show()
     sys.exit(app.exec_())	
