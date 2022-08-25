#WEB library
import streamlit.components.v1 as components
from secrets import choice
import streamlit as st
#from OpenSSL import SSL

#opencv library
import face_recognition
from datetime import datetime
from PIL import Image
import pandas as pd
import numpy as np
import cv2 
import os
import time
from datetime import date 
from tempfile import NamedTemporaryFile
import shutil
from csv import DictReader, DictWriter

#kemungkinan bug disini
FRAME_WINDOW = st.image([]) #frame window

#components.html("<html><body><h1>Absensi</h1></body></html>", width=200, height=200)

hhide_st_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hhide_st_style, unsafe_allow_html=True) #hide streamlit menu


menu = ["HOME","LOGIN", "REGISTER", "DATA", "ABOUT"] #menu
choice = st.sidebar.selectbox("Menu", menu) #sidebar menu

#absensi kehadiran
path = 'absensi' #path to save image
images = [] #list of image
classNames = [] #list of class
myList = os.listdir(path) #list of image

#buat file
# with open('./absensi.csv','w') as file:
#     csv_writer=writer(file,lineterminator='\n')
#     header =('name','date','time','latest time')
#     csv_writer.writerow(header)

col1,col4, col2, col3 = st.columns(4) #columns
cap = cv2.VideoCapture(0) #capture video
if choice == 'LOGIN': 
    st.markdown("<h2 style='text-align: center; color: black;'>ATTEDANCE</h2>", unsafe_allow_html=True) #title
    with col1: #column 1
        st.subheader("CHECKIN")
        run = st.checkbox("Checkin camera") #checkbox
        #run2 = st.checkbox("Run camera2") #checkbox
    if run == True:
        for cl in myList: #loop
            curlImg = cv2.imread(f'{path}/{cl}') #read image
            images.append(curlImg)
            classNames.append(os.path.splitext(cl)[0]) #split image name
        print(classNames)

        def findEncodings(images): #find encoding
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def faceList(name):
            with open('absensi.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    today = date.today()
                    dtString2 = now.strftime('%d/%m/%Y')
                    print("Today's date:", today)
                    f.writelines(f'\n{name},{dtString2},{dtString},')
                pass
        encodeListUnkown = findEncodings(images)
        print('encoding complate!')

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            #imgs = cv2.cvtColor(imgS,cv2.COLOR_RGB2BGR)
            imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

            for encodeFace,faceLoc in zip(encodeCurFrame,faceCurFrame):
                matches = face_recognition.compare_faces(encodeListUnkown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListUnkown,encodeFace)
                #print(faceDis)
                matchesIndex = np.argmin(faceDis)
                
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                if matches[matchesIndex]:
                    name = classNames[matchesIndex].upper()
                    print(name)
                    cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,225),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,225),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    faceList(name)

                    time.sleep(3)
                
                else:
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,225),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,225),cv2.FILLED)
                    cv2.putText(img,"Unknown",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            FRAME_WINDOW.image(img,channels="BGR")
            #cv2.imshow('webcam',img)
            cv2.waitKey(1)
    else:
        pass

    with col4: #column 1
        st.subheader("CHECKOUT")
        run2 = st.checkbox("Checkout camera") #checkbox
        #run2 = st.checkbox("Run camera2") #checkbox
    if run2 == True:
        for cl in myList: #loop
            curlImg = cv2.imread(f'{path}/{cl}') #read image
            images.append(curlImg)
            classNames.append(os.path.splitext(cl)[0]) #split image name
        print(classNames)

        def findEncodings(images): #find encoding
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def faceList(name):
            
            with open('absensi.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name in nameList:
                    temp_file=NamedTemporaryFile(mode='w',delete=False,dir='./tmpfile')
                    with open('./absensi.csv') as file:
                        csv_reader=DictReader(file)
                        data=list(csv_reader)
                        header=('name','date','time','latest time')
                        csv_writer=DictWriter(
                            temp_file,
                            fieldnames=header,
                            lineterminator='\n'
                        )
                        csv_writer.writeheader()
                        now = datetime.now()
                        dtString = now.strftime('%H:%M:%S')
                        dtString2 = now.strftime('%d/%m/%Y')
                        for row in data:
                            if row['name']==name:
                                #row['date']==dtString2
                                row['latest time']=dtString
                            csv_writer.writerow(row)
                    print(temp_file.name)
                    temp_file.close()
                    shutil.move(temp_file.name,'./absensi.csv')      
                pass
        encodeListUnkown = findEncodings(images)
        print('encoding complate!')

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

            for encodeFace,faceLoc in zip(encodeCurFrame,faceCurFrame):
                matches = face_recognition.compare_faces(encodeListUnkown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListUnkown,encodeFace)
                #print(faceDis)
                matchesIndex = np.argmin(faceDis)
                
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

                if matches[matchesIndex]:
                    name = classNames[matchesIndex].upper()
                    print(name)
                    cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,225),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,225),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    faceList(name)

                    time.sleep(3)
                
                else:
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,225),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,0,225),cv2.FILLED)
                    cv2.putText(img,"Unknown",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            #kemungkinan bug disini
            FRAME_WINDOW.image(img,channels="BGR")
            #cv2.imshow('webcam',img)
            cv2.waitKey(1)
    else:
        pass
#register menu
elif choice == 'REGISTER':
    with col2:
        st.subheader("REGISTER")
    def load_image(image_file):
        img = Image.open(image_file)
        return img

    image_file = st.file_uploader("Upload An Image",type=['png','jpeg','jpg'])
    if image_file is not None:
        file_details = {"FileName":image_file.name,"FileType":image_file.type}
        st.write(file_details)
        img = load_image(image_file)
        with open(os.path.join("absensi",image_file.name),"wb") as f: 
            f.write(image_file.getbuffer())         
        st.success("Saved File")

#read data menu

elif choice == 'DATA':
    with col2:
        df = pd.read_csv('absensi.csv')
        st.subheader("READ DATA")
        df = pd.read_csv('absensi.csv')
        st.write(df)
elif choice == 'HOME':
    with col1:
        components.html("<html><body><h1>Absensi</h1></body></html>")
        st.image("MOEKA.jpg",width=800, caption="Moeka") 

elif choice == "ABOUT":
    st.markdown("<h1 style='text-align: center; color: black;'>ABOUT</h1>", unsafe_allow_html=True) #title
    st.subheader("Moeka Store!")
    st.video("https://youtube.com/shorts/mhnrD6Pf8Co")
        