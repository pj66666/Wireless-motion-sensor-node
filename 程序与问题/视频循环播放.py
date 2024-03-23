import numpy as np
import cv2

#先提取视频的每一帧，存放到一个列表，然后循环展示每一帧，即可实现视频的循环播放
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

if __name__ == '__main__':
    video("F:/比赛/工程训练综合能力竞赛/Hw.mp4")
