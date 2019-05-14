import cv2
import numpy as np
from PIL import Image
import pickle
import os
import sqlite3




cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('/home/pi/haarcascade_frontalface_default.xml')
def insertorupdate(Id,Name,Email):
    conn=sqlite3.connect("faces.db")
    cmd="SELECT * FROM Employee WHERE Id="+str(Id)
    c = conn.execute(cmd)
    isRecordExist=0
    for row in c:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE Employee Set Name="+str(Name)+ ",Email= "+ str(Email)+ " WHERE Id="+str(Id)
    else:
#        cmd = conn.execute("INSERT INTO Employee(Id,Name,Email) Values(" +str(Id)+" , "+str(Name)+ " , "+ str(Email)+")")
     cmd="INSERT INTO Employee(Id,Name,Email) Values(" +str(Id)+" , "+str(Name)+ " , "+ str(Email)+")"
    print(cmd)
    conn.execute(cmd)
    conn.commit()
    conn.close()

id = input('\n enter user id end press <return> ==>  ')
name = input('\n enter user name end press <return> ==>  ')
email = input ('\n enter user email end press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

while(True):

    ret, img = cam.read()
    #img = cv2.flip(img, -1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 3 , 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 3)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("/home/pi/Desktop/project2/New/" + str(id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 5: # Take 100 face sample and stop video
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
#  cv2.imshow('im',im) 
    #if cv2.waitKey(10) & 0xFF==ord('q'):
     #   break
#cam.release()
#cv2.destroyAllWindows()
