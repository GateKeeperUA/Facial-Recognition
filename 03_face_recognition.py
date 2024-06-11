


import cv2
import numpy as np
import os 
import paho.mqtt.client as mqtt

# MQTT SETTINGS 
broker_address = "127.0.0.1"
port = 1883
topic = "DETI/Authenticate/Recognition"


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#id counter para rec
id = 0
message = ""
names = ['None', '1', '2', '3', '4', '5'] 

# Start Real time vid com settings
cam = cv2.VideoCapture(0)
cam.set(3, 640) # widht
cam.set(4, 480) # height

# Min quadrado para reconhecimento
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# Callback function                        AQUIIIII
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
#def on_publish(client, userdata, mid):
#    print("Message published")




# MQTT client
client = mqtt.Client()

# Assign callback     Anterior
client.on_connect = on_connect
#client.on_publish = on_publish
# Connect ao broker de mqtt


while True:
    client.connect(broker_address, port)
    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip image to fit webcam

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

        # confidence for match on model
        if (confidence < 60):
            id = id
            confidence = "  {0}%".format(round(100 - confidence))
            if(id!=message):
                message = "317"+str(id) #message format       !! To be tested !!
                client.publish(topic, message)
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
                     
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    

    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff #  'ESC'
    if k == 27:
        break


print("\n [INFO] Exiting Program and cleanup stuff")
# Disconnect mqtt broker and release cam
cam.release()
cv2.destroyAllWindows()
client.disconnect()
