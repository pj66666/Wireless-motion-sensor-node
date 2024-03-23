import numpy as np

import cv2

import time


#播放视频
def video(dir):           #视频路径
    cap = cv2.VideoCapture(dir)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()        
        if frame is None:           #最后一帧结束后跳出循环
            break
        frames.append(frame)
    cap.release()

    end = False
    while True:
        if end:
            break
        for frame in frames:
            cv2.imshow("loop a gif",frame)
            cv2.waitKey(int(1000/fps))      #根据帧率暂停对应时间，
                                            #保证合原视频一样播放效果,
                                            #不知为啥，这里需要整数
            
            k = cv2.waitKey(int(fps)) & 0xFF
            if k == 27:        #(按esc退出)
                end = True
                break
#调用舵机
def set_servo_angle(channel,angle):
    angle=4096*((angle*11)+500)/20000
    pwm.set_pwm(channel,0,int(angle))

pwm.set_pwm_freq(50)  #脉冲频率50Hz


img = np.zeros((1000,800,3),np.uint8)+255

font=cv2.FONT_HERSHEY_PLAIN

text="Queue"+"    "+"Class"+"    "+"Num"+"    "+"OK or NO"

cv2.putText(img,text,(10,50),font,1.5,(0,0,0),2)

d=100

for i in range(12):
    Rubbish = ['vegetable','pepper','cucumber','apple','banana','pear','bottle','can','battery','brick','cigarette']

    if i == 0:
       boxes = Rubbish[0]
    elif i == 1:
       boxes = Rubbish[1]
    elif i == 2:
       boxes = Rubbish[2]
    elif i == 3:
       boxes = Rubbish[3]
    elif i == 4:
       boxes = Rubbish[4]
    elif i == 5:
       boxes = Rubbish[5]
    elif i == 6:
       boxes = Rubbish[6]
    elif i == 7:
       boxes = Rubbish[7]
    elif i == 8:
       boxes = Rubbish[8]
    elif i == 9:
       boxes = Rubbish[9]
    elif i == 10:
       boxes = Rubbish[10]
    elif i == 11:
       video("D:/XXX.mp4")


    if object_name == Rubbish[0]:
        title="   "+ str(i)+"       "+"Kitchen waste"+"     "+"1"+"        "+"OK"
        set_servo_angle(5,90)
        time.sleep(0.5)
        set_servo_angle(6,90)
        time.sleep(1)
        set_servo_angle(6,90)
        time.sleep(0.5)
        set_servo_angle(5,90)
        time.sleep(0.5)
    elif object_name == Rubbish[1]:
        title="   "+ str(i)+"       "+"Kitchen waste"+"     "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[2]:
        title="   "+ str(i)+"       "+"Kitchen waste"+"     "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[3]:
        title="   "+ str(i)+"       "+"Kitchen waste"+"     "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[4]:
        title="   "+ str(i)+"       "+"Kitchen waste"+"     "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[5]:
        title="   "+ str(i)+"       "+"Kitchen waste"+"     "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[6]:
        title="   "+ str(i)+"       "+"recyclable trash"+"   "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[7]:
        title="   "+ str(i)+"       "+"recyclable trash"+"   "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[8]:
        title="   "+ str(i)+"       "+"Hazardous waste"+"   "+"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[9]:
        title="   "+ str(i)+"       "+"Other garbage"+"     " +"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    elif object_name == Rubbish[10]:
        title="   "+ str(i)+"      "+"Other garbage"+"     " +"1"+"        "+"OK"
        set_servo_angle(4,90)
        time.sleep(1)
    
    cv2.putText(img,title,(10,d),font,1.5,(0,0,0),2)
    #time.sleep(1)
    d=d+50

cv2.imshow("Rubbish",img)



cv2.waitKey(0)

cv2.destroyAllWindows()

#加上引号就不是打印变量了，比如title加上引号就变成了打印title，注意i也不能加
#否则不能打印出来数字
