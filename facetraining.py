import cv2
import numpy as np
from PIL import Image
import os


# Path for face image database
path1 = 'new/'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("C:/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml");
faceSamples=[]
ids = []
# function to get the images and label data
def getImagesAndLabels(path,Id):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    print(len(imagePaths))
    
    i = 1
    for imagePath in imagePaths:
        print("loop: " + str(i))
        i = i +1
#        if(os.path.split(imagePath)[-1].split(".")[-1]!='jpg'):
#            continue

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[0])
        
       # id = 1
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
           
            ids.append(id)
    return faceSamples,ids

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path1,1)
#faces,ids = getImagesAndLabels(path2,2)
#faces,ids = getImagesAndLabels(path3,3)
#faces,ids = getImagesAndLabels(path4,4)
print(ids)
recognizer.train(faces, np.array(ids))


# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len((ids))))