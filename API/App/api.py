from fastapi import FastAPI
from fastapi import Body 
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel
from Modelos.Modelos_Api import login_request, login_response
from Modelos.Modelos_Api import detection_request, detection_response
from Conexion_DB.conexion_db import Conexion_DB 
from Detector_Objetos.detector import Detector
from Utils.utils import crear_lista_predicciones,decodificar_imagen,codificar_imagen
import numpy as np
import cv2
from datetime import datetime


path_obj_names=r"./Pesos/obj.names"
path_obj_weights=r"./Pesos/custom-yolov4-detector_last.weights"
path_obj_cfg=r"./Pesos/custom-yolov4-detector.cfg"

app = FastAPI()
conn = Conexion_DB()
detector_yolo = Detector(path_obj_names,path_obj_weights,path_obj_cfg)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/login',response_model= login_response)
def login(login_req : login_request = Body(...)):
    try:
        usuario_existe = False 
        id_usuario = None
        predicciones = []

        usuario_existe, id_usuario = conn.login(login_req.usuario,login_req.password)
        if usuario_existe == True:
            predicciones = conn.busca_predicciones(id_usuario)
            predicciones = crear_lista_predicciones(predicciones)
            if predicciones != []:
                print("Este Usuario tiene predicciones")
            else:
                print("Este usuario no tiene predicciones")

        else:
            print("El usuario no encontrado, Verifique sus credenciales")  

        return login_response(
            usuario_existe=usuario_existe,
            predictions=predicciones)
    
    except Exception as e:
        print("Excepción en login", e)
        return JSONResponse(content= {"Mensaje":str(e)},status_code=500)

@app.post('/prediccion',response_model= detection_response)
def prediccion(detection_req : detection_request = Body(...)):
    try:
        usuario_existe = False 
        id_usuario = None
        prediccion = []
        fecha_deteccion = ""

        usuario_existe, id_usuario = conn.login(detection_req.usuario,detection_req.password)
        if usuario_existe == True:
            fecha_deteccion = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            decimg = decodificar_imagen(detection_req.image)
            image, lista_etiquetas_prediccion = detector_yolo.detect(decimg)
            cv2.imwrite(f'./Images/{fecha_deteccion}.jpg',image)
            #cv2.imshow("Image",image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            prediccion = conn.insertar_predicciones(id_usuario,fecha_deteccion,lista_etiquetas_prediccion)
            prediccion = crear_lista_predicciones(prediccion)
        else:
            print("El usuario no encontrado, Verifique sus credenciales")  

        return detection_response(
            usuario_existe=usuario_existe,
            prediction=prediccion)
    
    except Exception as e:
        print("Excepción en prediccion", e)
        return JSONResponse(content= {"Mensaje":str(e)},status_code=500)



