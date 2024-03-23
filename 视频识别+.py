#!/usr/bin/python
# -*- coding:  utf-8 -*-

import serial
import cv2
import numpy as np
import time

#树莓派对应的arduino串口
com0="/dev/ttyACM0"
com3="/dev/ttyACM1"
#com0="/dev/ttyUSB0"
com1="/dev/ttyUSB1"
com2="/dev/ttyAMA0"

#初始化串口
ser=serial.Serial(com0,9600,timeout=1)

#HSV阈值
lower_red_1 = np.array([0, 80, 200])    #s180
upper_red_1 = np.array([35, 255, 255])

lower_red_2 = np.array([170, 110, 200])
upper_red_2 = np.array([180, 255, 255])
    
lower_blue = np.array([70, 160, 50])    #s60
upper_blue = np.array([124, 255, 255])


#对一张图片进行形状、颜色分析
def analysis(frame):


      h, w, ch = frame.shape
      result = np.zeros((h, w, ch), dtype=np.uint8)
      
      frame1=cv2.GaussianBlur(frame,(11,11),0)#高斯处理

      #转换BGR为HSV
      hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

      red_mask_1 = cv2.inRange(hsv,lower_red_1,upper_red_1) #将图像二值化，在lower和upper之间的颜色变为白色，其他全为黑色
      red_mask_2 = cv2.inRange(hsv,lower_red_2,upper_red_2)
      red_mask = cv2.bitwise_or(red_mask_1, red_mask_2) #两种红色统一

      blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)  

      red_res = cv2.bitwise_or(frame, frame, mask = red_mask) #或运算，将彩色图像中红色部分选中，忽略其余颜色      
      blue_res = cv2.bitwise_and(frame, frame, mask = blue_mask)

      final_gray = cv2.bitwise_or(red_res, blue_res) #将选出的红色，蓝色都集成起来
      final_gray = cv2.cvtColor(final_gray,cv2.COLOR_BGR2GRAY) #得到最终的灰度图。轮廓提取的输入



      contours, hierarchy = cv2.findContours(final_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      for cnt in range(len(contours)):
                  
            # 计算面积与周长
            p = cv2.arcLength(contours[cnt], True)
            area = cv2.contourArea(contours[cnt])
            # 提取与绘制轮廓
            cv2.drawContours(result, contours, cnt, (0, 255, 0), 2)
                  # 轮廓逼近
            epsilon = 0.04 * cv2.arcLength(contours[cnt], True)  #0.03或0.04
            approx = cv2.approxPolyDP(contours[cnt], epsilon, True)

            corners = len(approx)
            #print(corners)
            mm = cv2.moments(contours[cnt])
                  # 求解中心位置
            if mm['m00'] != 0:
                      
              cx = int(mm['m10'] / mm['m00'])
              cy = int(mm['m01'] / mm['m00'])
              cv2.circle(result, (cx, cy), 3, (0, 0, 255), -1)

                      # 颜色分析
              color = frame[cy][cx]
              
              color_str = "(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ")"
              print("(cx,cy):( %.f,%.f),周长: %.3f, 面积: %.3f 颜色: %s 形状: %s "% (cx,cy,p, area, color_str,corners))
            else:
              continue

            shape_type = ""
            rank = ""
            object = []
            ranks = ""




            if  color[2] >= 200 :
                  if corners == 3 :
                        shape_type = 'red_triangle'
                        rank = '1'
                        print(shape_type)
                  elif corners >= 6 :
                        shape_type = 'red_circle' 
                        rank = '2'                  
                        print(shape_type)
                  elif corners == 4:
                        shape_type = 'red_rectangle'
                        rank = '3'
                        print(shape_type)
            elif color[0] >= 160 :
                  if corners == 3:
                        shape_type = 'blue_triangle'
                        rank = '4'
                        print(shape_type) 
                  elif corners >= 6 :
                        shape_type = 'blue_circle'
                        rank = '5'
                        print(shape_type)
                  elif corners == 4:
                        shape_type = 'blue_rectangle'
                        rank = '6'
                        print(shape_type)
            
            if rank in ranks:
              continue:
            else:
              object.append(rank)


            # display both the mask and the image side-by-side
            cv2.imshow('mask_red',red_res)
            cv2.imshow('mask_blue',blue_res)
            cv2.imshow('Analysis Result',result)
            cv2.imshow('final_gray',final_gray)
            #cv2.imshow('image', img)

#数据传输给arduino
def transmission(thing):
  for i in thing:
    ser.write(i)
    time.sleep(1)   #相当于换行

#通信判断
def tongxin():
   while 1:   
      
      res=ser.read().decode()
      
      print(res)
      if res == '1':
        print('ffff')
        camera()
        #if res == '0'::
          #print('dddd')
         # transmission(object)
          #break


def camera():
  cap = cv2.VideoCapture(0)      #usb camera parameter usually is 0
  cap.set(3,640)  
  cap.set(4,480)
  while(True):
      ret,Frame = cap.read()     #读取函数ret返回true或者false，false即读取图像失败，frame为每一帧的图像。

      analysis(Frame)
      cv2.imshow('Object detector',Frame)

      if ser.read().decode() == '0':
        break
      #elif cv2.waitKey(1) & 0xFF == ord('q'):            #按q退出
         # break
  transmission(ranks)


cap = cv2.VideoCapture(0)

if __name__ == "__main__":

    tongxin()
    
    #if ser.read() == 1:

    #if ser.read() == 0:
      #tongxing(object)
      #break
cap.release()
cv2.destroyAllWindows()
#图片处理
      #img = cv2.imread("C:/Users/hp/Desktop/hongyuan.jpg")    
      #frame = cv2.resize(img, (0,0), fx=0.8, fy=0.8)


      
#cv2.destroyAllWindows()
