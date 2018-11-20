import RPi.GPIO as GPIO
import cv2
import time
from pyzbar import pyzbar
import json
cap = cv2.VideoCapture('http://192.168.43.1:8080/video')

#this is roller coaster 1
#it is now time t1
time_slots = json.load('times.json')
time_currently = time_slots['r1']['t1']


greenpin = 18
redpin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(greenpin,GPIO.OUT)
GPIO.setup(redpin,GPIO.OUT)


while(True):
    # Capture frame-by-frame
#    ret, frame = cap.read()
    ret, frame = cap.read()
    barcodes = pyzbar.decode(frame)
    see_it = False
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        print(barcodeData)
        if barcodeData in time_currently:
            GPIO.output(greenpin,1)
            see_it = True
        else:
            GPIO.output(redpin,1)
            see_it = True

    #destroy
    if see_it == False:
        GPIO.output(redpin,0)
        GPIO.output(greenpin,0)

    # Display the resulting frame
    #cv2.imshow('frame',frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
