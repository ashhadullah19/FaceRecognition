import cv2
import numpy as np
import os
import sqlite3
import requests

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "C:/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);


font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter

def getProfile(id):
    conn=sqlite3.connect("Face.db")
    cmd="SELECT * FROM Employee WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
        
    conn.close()
    return profile
    

# Initialize and start realtime video capture
cam = cv2.VideoCapture(1)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img =cam.read()
    #img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        profile= getProfile(id)
        if(profile!=None):
            #cv2.putText(im, profile [1], (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(profile[1]), (x+5,y-5), font, 1, (255,255,255), 2)
        print('confidence: ' + str(confidence) + " name : " + str(profile[1]))
#        r = requests.get('http://localhost:82/fr/authenticate.php?confidence='+str(confidence)+'&name='+str(profile[1]))
            #cv2.putText(img, str(profile(1)), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 
#    if(len(faces) != 0):
#        break
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()