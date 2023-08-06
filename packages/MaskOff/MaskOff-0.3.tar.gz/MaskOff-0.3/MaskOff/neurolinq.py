import findFaceEnc
import Compare
import cv2
def CompareFace(name, photo1, photo2): 
    findFaceEnc.DetermineFace(photo1, name)
    Compare.ComparePeople(photo2)
