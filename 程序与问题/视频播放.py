import numpy as np
import cv2
import os


def inital(video_dir):
    
def videoread(video_dir):
    cap = cv2.VideoCapture(video_dir) #生成读取视频对象
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    #获取视频的宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))   #获取视频的高度
    fps = cap.get(cv2.CAP_PROP_FPS)    #获取视频的帧率
    fourcc = cv2.VideoWriter_fourcc(*'XVID')     #视频的编码
    
    while (cap.isOpened()):
        ret,frame = cap.read() #按帧读取视频
        cv2.imshow('frame',frame)
        #到视频结尾时终止
        cv2.waitKey(100)
        if ret is False :
            cap = cv2.VideoCapture(video_dir)
    #cap.release()
    #cv2.destroyAllWindows()
    
if __name__ == '__main__':
    i=1
    while(1):
        i=i+1
        print("第"+str(i)+"遍")
        videoread('D:/录屏/学习/新建文件夹/新建文件夹/20210223_160831.mp4')
