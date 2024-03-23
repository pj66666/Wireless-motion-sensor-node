import os                        #路径
import argparse                  #方便设置变量吧
import cv2                       #opencv
import numpy as np               #数组
import sys                       #配合路径
import time                      #延时
from threading import Thread     #线程
import importlib.util            #tensorflow库，具体不清楚


class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):

        self.stream = cv2.VideoCapture(0)            #读取摄像头视频
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])       #摄像头高度
        ret = self.stream.set(4,resolution[1])       #摄像头宽度
            

        (self.grabbed, self.frame) = self.stream.read()     #按帧读取

	# 控制摄像头停止
        self.stopped = False

    def start(self):
	# Start the thread线程 that reads frames from the video stream
        Thread(target=self.update,args=()).start()         #target是一个方法，args是位置变量的元组，此处update对应下面函数，不断更新
        return self

    def update(self):
        #无限循环，直到线程停止
        while True:
            if self.stopped:
                self.stream.release()
                return

            #按帧读取
            (self.grabbed, self.frame) = self.stream.read()   

    def read(self):
	#返回最近的一帧
        return self.frame

    def stop(self):
	#线程停止
        self.stopped = True
    def video(self,dir):           #视频路径
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
    def set_servo_angle(self,channel,angle):
        angle=4096*((angle*11)+500)/20000
        pwm.set_pwm(channel,0,int(angle))

# 定义和解析输入参数，就是为了在命令行调用程序做准备
parser = argparse.ArgumentParser()   #创建 ArgumentParser() 对象，一般我们只选择用description，这里无
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',      
                    required=True)                           #调用 add_argument() 方法添加参数，基本上按默认参数来，若改变在命令行更改
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')                 #简化识别模型
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')                  #模型标签图
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5)                             #threshold临界点，可信度大于50%显示
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='1280x720')                      #默认分辨率

args = parser.parse_args()       #使用 parse_args() 解析添加的参数，通常 parse_args() 不带参数调用

MODEL_NAME = args.modeldir         #定义路径变量
GRAPH_NAME = args.graph            #模型变量
LABELMAP_NAME = args.labels        #标签变量
min_conf_threshold = float(args.threshold)    #临界值
resW, resH = args.resolution.split('x')       #分辨率    spilt把一个数组从左到右按顺序切分
imW, imH = int(resW), int(resH)               

# 导入tensorflow库
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter

# 当前文件夹路径
CWD_PATH = os.getcwd()

# 模型路径
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

#标签路径
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

#加载Tensorflow Lite model.
interpreter = Interpreter(model_path=PATH_TO_CKPT)
interpreter.allocate_tensors()
#模型参数
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5   #用于模型量化
input_std = 127.5

# 初始化帧率计算
frame_rate_calc = 1
freq = cv2.getTickFrequency()

#初始化视频流
videostream = VideoStream(resolution=(imW,imH),framerate=30).start()  #调用start函数
time.sleep(1)

pwm.set_pwm_freq(50)  #脉冲频率50Hz

img = np.zeros((1000,800,3),np.uint8)+255

font=cv2.FONT_HERSHEY_PLAIN

text="Queue"+"    "+"Class"+"    "+"Num"+"    "+"OK or NO"

cv2.putText(img,text,(10,50),font,1.5,(0,0,0),2)

d=100

while True:

    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    frame1 = videostream.read()       #获取图片帧

    frame = frame1.copy()                                    #复制图片
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)       #设置图片格式
    frame_resized = cv2.resize(frame_rgb, (width, height))   #更改大小
    input_data = np.expand_dims(frame_resized, axis=0)       #表示在0位置添加数据

    #如果使用浮动模型，则对像素值进行归一化（即，如果模型未量化）
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve取回 detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates（座标） of detected objects  物体坐标
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects分类请况
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects信誉值
    #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)监测到的数量

    #遍历所有检测并在置信度高于最小阈值时绘制检测框
    for i in range(len(scores)):           #len可以确定列表长度，range生成数字列表，默认从0开始输出
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):   #0.5>可信度<1

            # Get bounding box coordinates and draw box
            #解释器可以返回超出图像尺寸的坐标，需要使用max（）和min（）强制其位于图像内
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
            
            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)          #画一个包括物体的矩形框

            #显示label
            object_name = labels[int(classes[i])] #通过使用分类索引从labelmap矩阵中寻找检测物体名称
            label = '%s: %d%%' % (object_name, int(scores[i]*100)) # 例子: 'person: 72%'
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) #获取字体大小
            label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
            cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text

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

    # 在左上角处绘制帧率，cv文字
    cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
    #显示画面
    cv2.imshow('Object detector', frame)

    t2 = cv2.getTickCount()framerate
    time1 = (t2-t1)/freq
    frame_rate_calc= 1/time1

    if cv2.waitKey(1) == ord('q'):
        break


video("D:///.mp4")


cv2.destroyAllWindows()
videostream.stop()