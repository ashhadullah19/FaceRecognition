from tkinter import *
import os
from datetime import datetime
root=Tk()
root.configure(background="white")

def function1():
     #insertorupdate(55,"assbith","ass@b")
    ## m = __import__(facerecognition.py)
     os.system("python3 facerecognition.py")
   
    
def function2():
    
    os.system("python3 /home/pi/Desktop/project2/facetraining.py")

def function3():

    os.system("python3 /home/pi/Desktop/project2/recognizer2.py")
    
   
def function4():

    root.destroy()
    
root.title("Employee Attendance System")

Label(root, text="EMPLOYEE ATTENDANCE SYSTEM",font=("times new roman",20),fg="white",bg="grey",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=7,pady=7)

#creating first button
Button(root,text="Create Dataset",font=("times new roman",20),bg="#0D47A1",fg='white',command=function1).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
#Button.pack()
#creating second button
Button(root,text="Train Dataset",font=("times new roman",20),bg="#0D47A1",fg='white',command=function2).grid(row=4,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

#creating third button
Button(root,text="Recognize + Attendance",font=('times new roman',20),bg="#0D47A1",fg="white",command=function3).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

Button(root,text="Exit",font=('times new roman',20),bg="maroon",fg="white",command=function4).grid(row=9,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
