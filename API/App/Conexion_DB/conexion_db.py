import sqlite3

class Conexion_DB:
    def __init__(self):
        self.conexion = sqlite3.connect(r'./Base_Datos/db1.db',check_same_thread=False)
    
    def busca_users(self, usuario):
        cur = self.conexion.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE Usuario=:c",{"c":usuario})
        usuariox = cur.fetchall()
        cur.close()
        print(usuariox)
        return usuariox

    def busca_password(self, password):
        cur = self.conexion.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE Password=:c",{"c":password})
        passwordx = cur.fetchall()
        cur.close()
        print(passwordx)
        return passwordx

    def busca_predicciones(self, id_usuario):
        cur = self.conexion.cursor()
        cur.execute("SELECT * FROM Predicciones WHERE IDUsuario=:c",{"c":id_usuario})
        prediccionesx = cur.fetchall()
        cur.close()
        print(prediccionesx)
        return prediccionesx
        
    def login(self, usuario, password):
        usuario_existe= False
        id_usuario = None
        dato1 = self.busca_users(usuario)
        dato2 = self.busca_password(password)
        if dato1 == [] or dato2 ==[]:
            usuario_existe = False
            id_usuario = None
        
        elif dato1 != [] and dato2 != []:
            usuario_existe = True
            id_usuario = dato1[0][0]

        return usuario_existe, id_usuario
    
    def insertar_predicciones(self, id_usuario,fecha_deteccion,lista_etiquetas_prediccion):
        cur = self.conexion.cursor()
        sql_query = """INSERT INTO Predicciones(FechaDeteccion, Prediccion, IDUsuario)
            VALUES (?, ?, ?);"""
        
        cur.execute(sql_query, (fecha_deteccion, str(lista_etiquetas_prediccion),id_usuario))
        self.conexion.commit()
        prediccionesx = [(id_usuario,fecha_deteccion, str(lista_etiquetas_prediccion),id_usuario)]
        print(prediccionesx)
        return prediccionesx

    