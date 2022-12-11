import cv2
import time
import os

class Detector:
    def __init__(self, path_obj_names,path_obj_weights,path_obj_cfg):

        self.confidence_threshold = 0.4
        self.nms_threshold = 0.4
        self.colors = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
        self.class_names = []
        with open(path_obj_names, "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

        self.net = cv2.dnn.readNet(path_obj_weights,path_obj_cfg)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) #must be enabled for CPU
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) #must be enabled for CPU
        
        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=(416, 416), scale=1/float(255.0), swapRB=True)

    def detect(self, image):
        classes, scores, boxes = self.model.detect(image, self.confidence_threshold, self.nms_threshold)
        lista_etiquetas_prediccion = []
        
        for (classid, score, box) in zip(classes, scores, boxes):
            color = self.colors[int(classid) % len(self.colors)]
            label = self.class_names[classid]#"%s : %f" % (classid, round(score,2))
            cv2.rectangle(image, box, color, 2)
            cv2.putText(image, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            lista_etiquetas_prediccion.append({"id":label,"bbox":[str(box[0]), str(box[1]), str(box[2]), str(box[3])]})
           
        return image, lista_etiquetas_prediccion
