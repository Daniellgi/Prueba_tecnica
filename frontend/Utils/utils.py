import base64
import numpy as np
import cv2

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