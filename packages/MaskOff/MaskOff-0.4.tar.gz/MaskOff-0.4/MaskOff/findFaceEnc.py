from imutils import paths
import face_recognition
import pickle
import cv2
import os
 
# в директории Images хранятся папки со всеми изображениями
def DetermineFace(photo, name):

    rgb = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    knownEncodings=[]
    knownNames=[]
    #используем библиотеку Face_recognition для обнаружения лиц
    boxes = face_recognition.face_locations(rgb,model='hog')
    # вычисляем эмбеддинги для каждого лица
    encodings = face_recognition.face_encodings(rgb, boxes)
    # loop over the encodings
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)
    # сохраним эмбеддинги вместе с их именами в формате словаря
    data = {"encodings": knownEncodings, "names": knownNames}
    # для сохранения данных в файл используем метод pickle
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()