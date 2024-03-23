#include <MsTimer2.h>    //定时中断库

//**************编码器接线******************
#define Encoder_A 2  //外部中断，编码器A相
#define Encoder_B 8  //B相


//***********驱动电路输入******************
#define motor_En 6    //pwm输出 
#define Motor_AIN1 4//正 
#define Motor_AIN2 5//反


//************编码器脉冲转换速度参数************
int count=0;    //脉冲计数 
float V_1;      //电机1速度


//************PID参数************
float V_KP =3.2,V_KI =0.01,Target_V=40;   //Target目标速度
double pwm=0,previous_error=0,last_error=0;
float Average;    //中间变量


//************初始化************
void setup()
{  
  Serial.begin(9600);
//  pinMode(Encoder_A,INPUT);    //编码器输入    %%%%%%%%%%%%%%%%%%%%%%%%%
  pinMode(Encoder_B,INPUT);
  
  pinMode(motor_En,OUTPUT);    //驱动输出
  pinMode(Motor_AIN1,OUTPUT);
  pinMode(Motor_AIN2,OUTPUT);

  analogWrite(motor_En,LOW);  //输出初始化低电平
  digitalWrite(Motor_AIN1, LOW);  
  digitalWrite(Motor_AIN2, LOW);
  
  MsTimer2::set(10, Timer_interrupt);  //内部定时中断
  MsTimer2::start();
  attachInterrupt(0, Read_Encoder_Enable, FALLING);  //2号（编码器A相引脚）上升沿触发外部中断 //%%%%%%%%%%%%%
}



//************主函数************
void loop() {
   
    Average=PID(V_1,Target_V);
    set_U(Average);
//   set_U(30);      
}


//************外部中断函数，判断方向************
void Read_Encoder_Enable()
  {
    if (digitalRead(Encoder_B) == LOW)                
       count++;  //根据另外一相电平判定方向         
    else          
       count--; 
  }

//************内部定时中断************

void Timer_interrupt(){
  
  V_1 = (count*PI*12.7)/(500*51*0.01);  //速度cm/s
  Serial.println(V_1);
  count=0;
  }


//************PID调速，得到控制电压PWM************
int PID(int current_speed,int target_speed) {
//  static float pwm,previous_error,last_error;  
  
  previous_error = target_speed-current_speed;  //当前转速减去设定值  
  pwm+=V_KP*(previous_error-last_error)+V_KI*previous_error;
   
  last_error = previous_error;
  
  //限幅  
  if(pwm>255){
   pwm=255; }
   
  if(pwm<-255){
    pwm=-255; }    

   return pwm;
}

  
//************设置电机1的控制电压************
void set_U(int pwm){
  if(pwm >0)
  {
   analogWrite(motor_En , pwm); 
   digitalWrite(Motor_AIN1, HIGH);
   digitalWrite(Motor_AIN2, LOW);
  }
  if(pwm == 0)
  {
   analogWrite(motor_En,0);  
   digitalWrite(Motor_AIN1,LOW);
   digitalWrite(Motor_AIN2,LOW);
  }
  if(pwm <0)
  {
   analogWrite(motor_En , -pwm);  
   digitalWrite(Motor_AIN1, LOW);
   digitalWrite(Motor_AIN2, HIGH);
  } 
}
