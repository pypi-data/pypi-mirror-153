from PIL import Image
import api
import matplotlib.pyplot as plt
import cv2 
import os
import pickle

def CheckFace(path):
    image = api.load_image_file(path)
    face_loc = api.face_locations(image)
    if (len(face_loc) == 0):
        return False
    return True

def DetermineFace(photo):
    rgb = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
    knownEncodings=[]
    knownNames=[]
    boxes = api.face_locations(rgb,model='hog')
    encodings = api.face_encodings(rgb, boxes)
    for encoding in encodings:
        knownEncodings.append(encoding)
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open("face_enc", "wb")
    f.write(pickle.dumps(data))
    f.close()

def Compare(pic):
    data = pickle.loads(open('face_enc', "rb").read())
    image = pic
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodings = api.face_encodings(rgb)
    for encoding in encodings:
        matches = api.compare_faces(data["encodings"],
        encoding)
        if True in matches:
            return True
    return False

def CompareFaces(photo1, photo2): 
    if (not(CheckFace(photo1)) or not(CheckFace(photo2))):
        return False
    DetermineFace(cv2.imread(photo1))
    return Compare(cv2.imread(photo2))