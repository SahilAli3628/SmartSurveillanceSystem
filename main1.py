import cv2
import time
import os
from simple_facerec import SimpleFacerec
from alerts import email_alert
from alerts import text_alert

def faceBox(faceNet,frame):
    frameHeight=frame.shape[0]
    frameWidth=frame.shape[1]
    blob=cv2.dnn.blobFromImage(frame, 1.0, (300,300), [104,117,123], swapRB=False)
    faceNet.setInput(blob)
    detection=faceNet.forward()
    bboxs=[]
    for i in range(detection.shape[2]):
        confidence=detection[0,0,i,2]
        if confidence>0.7:
            x1=int(detection[0,0,i,3]*frameWidth)
            y1=int(detection[0,0,i,4]*frameHeight)
            x2=int(detection[0,0,i,5]*frameWidth)
            y2=int(detection[0,0,i,6]*frameHeight)
            bboxs.append([x1,y1,x2,y2])
            cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0), 1)
    return frame, bboxs

sfr = SimpleFacerec()
sfr.load_encoding_images("/home/s4hi1/MajorProject/FINAL CODE/SSS/images/")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faceProto = "/home/s4hi1/MajorProject/FINAL CODE/SSS/AgeRange_Gender_Recongnition/opencv_face_detector.pbtxt"
faceModel = "/home/s4hi1/MajorProject/FINAL CODE/SSS/AgeRange_Gender_Recongnition/opencv_face_detector_uint8.pb"
ageProto = "/home/s4hi1/MajorProject/FINAL CODE/SSS/AgeRange_Gender_Recongnition/age_deploy.prototxt"
ageModel = "/home/s4hi1/MajorProject/FINAL CODE/SSS/AgeRange_Gender_Recongnition/age_net.caffemodel"
genderProto = "/home/s4hi1/MajorProject/FINAL CODE/SSS/AgeRange_Gender_Recongnition/gender_deploy.prototxt"
genderModel = "/home/s4hi1/MajorProject/FINAL CODE/SSS/AgeRange_Gender_Recongnition/gender_net.caffemodel"

faceNet=cv2.dnn.readNet(faceModel, faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

cap = cv2.VideoCapture(0)
padding = 20

while True:
    ret, frame1 = cap.read()
    face_locations, face_names = sfr.detect_known_faces(frame1)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
    facerec_label = name

    ret,frame=cap.read()
    frame,bboxs=faceBox(faceNet,frame)
    for bbox in bboxs:
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
    blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
    genderNet.setInput(blob)
    genderPred=genderNet.forward()
    gender=genderList[genderPred[0].argmax()]
    ageNet.setInput(blob)
    agePred=ageNet.forward()
    age=ageList[agePred[0].argmax()]

    label="{},{}".format(gender,age)
    ageGender_label = label
    if facerec_label == 'Unknown':
        frame_text = 'Unknown' + " " + ageGender_label
        count = 0
        while count < 1:
            # email_alert.email_alert("INTRUDER ALERT!!!", "We have detected strangers", "sahilali3628@gmail.com")
            # text_alert.text_alert("INTRUDER ALERT!")
            print("Unknown")
            count += 1
    else:
        frame_text = facerec_label + " "+ ageGender_label

    ret, frames = cap.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x,y,w,h) in faces:
        cv2.rectangle(frames, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.putText(frames, frame_text, (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)

    cv2.imshow("frames", frames)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
