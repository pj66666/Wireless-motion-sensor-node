#!/usr/bin/python
# -*- coding:  utf-8 -*-

import serial
import numpy as np
import time
import cv2
com0="/dev/ttyACM0"
com3="/dev/ttyACM1"
#com0="/dev/ttyUSB0"
com1="/dev/ttyUSB1"
com2="/dev/ttyAMA0"
ser=serial.Serial(com0,9600,timeout=1)
 

#print("Serial name:",ser.name)
#print("Serial baudrate:",ser.baudrate)
#print("Serial state:",ser.is_open)

object = ['red_circle','red_rectangle','green_circle']
def tongxing(o):
  for i in o:
    ser.write(i)
    time.sleep(1)

def camera():
  cap = cv2.VideoCapture(0)      #usb camera parameter usually is 0
  cap.set(3,640)  
  cap.set(4,480)
  while(True):
      ret,Frame = cap.read()     #读取函数ret返回true或者false，false即读取图像失败，frame为每一帧的图像。
      Frame = cv2.flip(Frame,1)  #获取翻转的图像
      
      
      cv2.imshow('gu',Frame)     #原图像显示    
      
      if cv2.waitKey(1) & 0xFF == ord('q'):            #按q退出
          break

if __name__ == "__main__":
  
   while 1:   
      
      res=ser.read().decode()
      
      print(res)
      if res == '1':
        print('ffff')
        camera()
      else:
        print('gsvrd')
        #break


       #time.sleep(1)
       #ser.write("Hello! I am Raspberry!".encode("utf-8"))
  
  
  

  
      
        

#cap.release()
#cap.destroyAllWindows()
    






