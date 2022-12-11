#Python

from typing import Dict, List, Optional
#Pydantic 
from pydantic import BaseModel

class login_request(BaseModel):
    usuario : str
    password : str

class detection_request(BaseModel):
    usuario : str
    password : str
    image :str 

class login_response(BaseModel):
    usuario_existe : bool
    predictions: Optional [List[Dict]] = []
    
class detection_response(BaseModel):
    usuario_existe : bool
    prediction: Optional [List[Dict]] = []
    

