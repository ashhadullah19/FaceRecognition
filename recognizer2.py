import cv2
import numpy as np
from PIL import Image
import pickle
import os
import sqlite3
import time
import datetime
import requests
import json


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "/home/pi/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

#def getProfile(id):
#    conn=sqlite3.connect("FaceBase.db")
#    cmd="SELECT * FROM Employee WHERE Id = "+str(id)
#    cursor=conn.execute(cmd)
#    profile=None
#    for row in cursor:
#        profile=row
#    print(profile)
#    
#    return profile
    #conn.close()
#.strftime
def post_request(email,Time):
    currentDate = time.strftime("%y-%m-%d")
    currentDate = "20" + str(currentDate) + " " + str(Time)
    data = {"UserEmail":  str(email) , "EntryType":  str(' ') , "EntryTime": str(currentDate)}
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    print(data_json)
    req = requests.post('https://neuhrapi-dev.neusol.com/api/visitlog', data=data_json, headers = headers)
    print(req.status_code)

count = 0
last_id = 0
time1 = time.asctime(time.localtime())
time1 = time1.split(' ')[3]
last_time = time1
print(last_time)
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, 3 ,5)
    time1 = time.asctime(time.localtime())
    time1 = time1.split(' ')[3]
    diff = int(time1.split(':')[2]) - int(last_time.split(':')[2])
    print('diff' +": " + str(diff))
    print(time1)

    for(x,y,w,h) in faces:
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
        print(Id)
        if(last_id == 0):
            last_id = Id
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),4)
        #profile= getProfile(id)
        conn=sqlite3.connect("/home/pi/Desktop/project2/faces.db")
        cmd="SELECT * FROM Employee WHERE Id = "+ str(Id)
        cursor=conn.execute(cmd)
        profile=None
        for row in cursor:
            profile=row
        print(profile)
        if(profile!=None):
            cv2.putText(im, profile[2], (x+5,y-5), font, 1, (255,255,255), 2)
            currentDate = time.strftime("%d_%m_%y")
            cmd = "select InTime,OutTime from DateTime where rowid = (select max(rowid) from DateTime where Id = " + str(last_id) + " and Date = '" + currentDate + "')"
            print(cmd)
            cursor=conn.execute(cmd)
            profile=None
            for row in cursor:
               profile=row
            print(profile)
            if(last_id != Id):
                print('ok')
                if(profile != None):
                    if(profile[0] == ''):
                        cmd = "INSERT INTO DateTime(Id,Date,InTime,OutTime) Values(" + str(last_id)  + ",'"+  currentDate +"',"+"'"+ last_time +"'" +","+ "''" +")"  
                    else:
                        cmd = "INSERT INTO DateTime(Id,Date,InTime,OutTime) Values(" + str(last_id)  + ",'"+  currentDate +"',"+ "''" +",'"+ last_time +"')"
                else:
                    cmd = "INSERT INTO DateTime(Id,Date,InTime,OutTime) Values(" + str(last_id)  + ",'"+  currentDate +"',"+"'"+ last_time +"'" +","+ "''" +")"
                print(profile)
                conn.execute(cmd)
                conn.commit()
                cmd = "select * from Employee where Id = " + str(last_id)
                cursor=conn.execute(cmd)
                profile=None
                for row in cursor:
                   profile=row
                if(profile != None):
                    post_request(profile[2],last_time)
            
            else:
                last_time = time1
    print('ab condition check')
    if(diff == 5 and count == 0):
                 try:
                     count = count +1
                     print('agaya')
                     currentDate = time.strftime("%d_%m_%y")
                     cmd = "select InTime,OutTime from DateTime where rowid = (select max(rowid) from DateTime where Id = " + str(last_id) + " and Date = '" + currentDate + "')"
                     print(cmd)
                     cursor=conn.execute(cmd)
                     profile=None
                     for row in cursor:
                       profile=row
                     print(profile)
                     if(profile != None):
                            if(profile[0] == ''):
                                cmd = "INSERT INTO DateTime(Id,Date,InTime,OutTime) Values(" + str(last_id)  + ",'"+  currentDate +"',"+"'"+ last_time +"'" +","+ "''" +")"  
                            else:
                                cmd = "INSERT INTO DateTime(Id,Date,InTime,OutTime) Values(" + str(last_id)  + ",'"+  currentDate +"',"+ "''" +",'"+ last_time +"')"
                     else:
                        cmd = "INSERT INTO DateTime(Id,Date,InTime,OutTime) Values(" + str(last_id)  + ",'"+  currentDate +"',"+"'"+ last_time +"'" +","+ "''" +")"
                     try:
                         print(cmd)
                         conn.execute(cmd)
                         conn.commit()
                         cmd = "select * from Employee where Id = " + str(last_id) 
                         cursor=conn.execute(cmd)
                         profile=None
                         for row in cursor:
                           profile=row
                         if(profile != None):
                             post_request(profile[2],last_time)
                             
                     except:
                             print('koi query ni')
                 except:
                    print('profile none ha')
    if(diff == 6):
        count = 0
    cv2.imshow('im',im) 
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()