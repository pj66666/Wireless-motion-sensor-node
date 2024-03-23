int count=0;
void setup(){
  Serial.begin(9600);
}
 
void loop(){
    
//    接受数据
    String str="";
    while(Serial.available()){
       char ch=Serial.read();
       str+=ch;
       delay(10);
     }
    if(str.length()>0)
    Serial.println(str);
    
//    //发送数据
//    count++;
//    Serial.println(1);
//    
//    delay(1000);
 
}
