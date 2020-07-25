import tkinter as tk
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
from tkinter import messagebox
import sqlite3
import math
import argparse


window = tk.Tk()

window.title("Attendance System")

window.configure(background='black')


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

x_cord = 75;
y_cord = 20;
checker=0;

message = tk.Label(window, text="GCNEP,Haryana" ,bg="black"  ,fg="white"  ,width=20  ,height=2,font=('Times New Roman', 25, 'bold'))
message.place(x=110, y=760)

message = tk.Label(window, text="ATTENDANCE MANAGEMENT PORTAL" ,bg="black"  ,fg="white"  ,width=40  ,height=1,font=('Times New Roman', 35, 'bold underline'))
message.place(x=300, y=20)

lbl = tk.Label(window, text="Enter Your Office ID",width=20  ,height=2  ,fg="white"  ,bg="black" ,font=('Times New Roman', 25, ' bold ') )
lbl.place(x=200-x_cord+30, y=200-y_cord)


txt = tk.Entry(window,width=30,bg="white" ,fg="black",font=('Times New Roman', 15, ' bold '))
txt.place(x=250-x_cord, y=300-y_cord)

lbl2 = tk.Label(window, text="Enter Your Name",width=20  ,fg="white"  ,bg="black"    ,height=2 ,font=('Times New Roman', 25, ' bold '))
lbl2.place(x=600-x_cord+20, y=200-y_cord)

txt2 = tk.Entry(window,width=30  ,bg="white"  ,fg="black",font=('Times New Roman', 15, ' bold ')  )
txt2.place(x=650-x_cord, y=300-y_cord)

lbl3 = tk.Label(window, text="ATTENDANCE",width=20  ,fg="white"  ,bg="black"  ,height=2 ,font=('Times New Roman', 30, ' bold '))
lbl3.place(x=120, y=570-y_cord)


message2 = tk.Label(window, text="" ,fg="white"   ,bg="black",activeforeground = "green",width=60  ,height=4  ,font=('times', 15, ' bold '))
message2.place(x=700, y=570-y_cord)

lbl4 = tk.Label(window, text="STEP 1",width=20  ,fg="white"  ,bg="black"  ,height=2 ,font=('Times New Roman', 20, ' bold '))
lbl4.place(x=240-x_cord, y=375-y_cord)

lbl5 = tk.Label(window, text="STEP 2",width=20  ,fg="white"  ,bg="black"  ,height=2 ,font=('Times New Roman', 20, ' bold '))
lbl5.place(x=645-x_cord, y=375-y_cord)

lbl6 = tk.Label(window, text="STEP 3",width=20  ,fg="white"  ,bg="black"  ,height=2 ,font=('Times New Roman', 20, ' bold '))
lbl6.place(x=1100-x_cord, y=375-y_cord)

 
def TakeImages():
    Id=(txt.get())
    name=(txt2.get())
    conn = sqlite3.connect('database.db')
    if not os.path.exists('./dataset'):
        os.makedirs('./dataset')
    
    
    c = conn.cursor()

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    
    uname = input("Enter your name: ")

    c.execute('INSERT INTO users (name) VALUES (?)', (uname,))


    uid = c.lastrowid

    sampleNum = 0

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            sampleNum = sampleNum+1
            cv2.imwrite("dataset/User."+str(uid)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            cv2.waitKey(100)
        cv2.imshow('img',img)
        cv2.waitKey(1);
        if sampleNum >20:
            break
    cap.release()

    conn.commit()

    conn.close()
    cv2.destroyAllWindows()
   
    

    
def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    threshold=0.82
    path = 'dataset'
    if not os.path.exists('./recognizer'):
        os.makedirs('./recognizer')

    def getImagesWithID(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow("training",faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces,Ids)
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()
    tk.messagebox.showinfo('Completed','Your model has been trained successfully!!')

def TrackImages():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    fname = "recognizer/trainingData.yml"
    if not os.path.isfile(fname):
        print("Please train the data first")
        exit(0)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(fname)

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            ids,conf = recognizer.predict(gray[y:y+h,x:x+w])
            c.execute("select name from users where id = (?);", (ids,))
            result = c.fetchall()
            name = result[0][0]
            if conf < 50:
                cv2.putText(img, name, (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,255,0),2)
            else:
                cv2.putText(img, 'No Match', (x+2,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        cv2.imshow('Face Recognizer',img)
        if (cv2.waitKey(1)==ord('q')):
            break
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cap.release()
    cv2.destroyAllWindows()
    res=attendance
    message2.configure(text= res)
    res = "Attendance Taken"
    message.configure(text= res)
    tk.messagebox.showinfo('Completed','Congratulations ! Your attendance has been marked successfully for the day!!')
    



    
    
def quit_window():
    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       tk.messagebox.showinfo("Greetings", "Thank You very much for using our software. Have a nice day ahead!!")
       window.destroy()
    
def create_database():
    conn = sqlite3.connect('database.db')

    c = conn.cursor()

    sql = """
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
               id integer unique primary key autoincrement,
               name text,
               img_count integer
    );
    """
    c.executescript(sql)

    conn.commit()

    conn.close()
    
def check_age():
    def highlightFace(net, frame, conf_threshold=0.7):
        frameOpencvDnn=frame.copy()
        frameHeight=frameOpencvDnn.shape[0]
        frameWidth=frameOpencvDnn.shape[1]
        blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections=net.forward()
        faceBoxes=[]
        for i in range(detections.shape[2]):
            confidence=detections[0,0,i,2]
            if confidence>conf_threshold:
                x1=int(detections[0,0,i,3]*frameWidth)
                y1=int(detections[0,0,i,4]*frameHeight)
                x2=int(detections[0,0,i,5]*frameWidth)
                y2=int(detections[0,0,i,6]*frameHeight)
                faceBoxes.append([x1,y1,x2,y2])
                cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
        return frameOpencvDnn,faceBoxes


    parser=argparse.ArgumentParser()
    parser.add_argument('--image')

    args=parser.parse_args()

    faceProto="opencv_face_detector.pbtxt"
    faceModel="opencv_face_detector_uint8.pb"
    ageProto="age_deploy.prototxt"
    ageModel="age_net.caffemodel"
    genderProto="gender_deploy.prototxt"
    genderModel="gender_net.caffemodel"

    MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
    ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList=['Male','Female']

    faceNet=cv2.dnn.readNet(faceModel,faceProto)
    ageNet=cv2.dnn.readNet(ageModel,ageProto)
    genderNet=cv2.dnn.readNet(genderModel,genderProto)

    video=cv2.VideoCapture(args.image if args.image else 0)
    padding=20
    while cv2.waitKey(1)<0 :
        hasFrame,frame=video.read()
        if not hasFrame:
            cv2.waitKey()
            break
    
        resultImg,faceBoxes=highlightFace(faceNet,frame)
        if not faceBoxes:
            print("No face detected")

        for faceBox in faceBoxes:
            face=frame[max(0,faceBox[1]-padding):
                       min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                       :min(faceBox[2]+padding, frame.shape[1]-1)]

            blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds=genderNet.forward()
            gender=genderList[genderPreds[0].argmax()]
            print(f'Gender: {gender}')

            ageNet.setInput(blob)
            agePreds=ageNet.forward()
            age=ageList[agePreds[0].argmax()]
            print(f'Age: {age[1:-1]} years')

            cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
            cv2.imshow("Detecting age and gender", resultImg)


check_age = tk.Button(window, text="Check your age!", command=check_age  ,fg="red"  ,bg="black"  ,width=30  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
check_age.place(x=1075-x_cord, y=200-y_cord)
create_database = tk.Button(window, text="CREATE DATABASE", command=create_database  ,fg="red"  ,bg="black"  ,width=30  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
create_database.place(x=1075-x_cord, y=300-y_cord)
takeImg = tk.Button(window, text="IMAGE CAPTURE BUTTON", command=TakeImages  ,fg="red"  ,bg="black"  ,width=30  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
takeImg.place(x=250-x_cord, y=425-y_cord)
trainImg = tk.Button(window, text="MODEL TRAINING BUTTON", command=TrainImages  ,fg="red"  ,bg="black"  ,width=30  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
trainImg.place(x=650-x_cord, y=425-y_cord)
trackImg = tk.Button(window, text="MARK ATTENDANCE", command=TrackImages  ,fg="red"  ,bg="red"  ,width=30  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
trackImg.place(x=1075-x_cord, y=425-y_cord)
quitWindow = tk.Button(window, text="QUIT", command=quit_window  ,fg="red"  ,bg="red"  ,width=10  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
quitWindow.place(x=700, y=735-y_cord)
 
window.mainloop()
