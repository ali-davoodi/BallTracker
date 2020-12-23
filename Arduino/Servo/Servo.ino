// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servo1Pin = 3; 
int servo2Pin=4;
// Create a servo object 
Servo Servo1,Servo2; 
unsigned char RXbuff[10];
int RXcnt=0;
int servo1RX,servo2RX;
void setup() { 
  pinMode(13, OUTPUT);      // set LED pin as output
  digitalWrite(13, LOW);    // switch off LED pin

  Serial.begin(115200,SERIAL_8N1);       // initialize UART with baud rate of 9600 bps

   Servo1.attach(servo1Pin); 
   Servo2.attach(servo2Pin);
    Servo1.write(90); 
    Servo2.write(90); 
}
void loop(){ 


if(Serial.available()) {
    unsigned char data_rcvd = Serial.read();   // read one byte from serial buffer and save to data_rcvd
    RXbuff[RXcnt]=data_rcvd;
    if(data_rcvd==0xE7 && RXcnt>=2)
    {
      servo1RX=RXbuff[RXcnt-1];
      servo2RX=RXbuff[RXcnt-2];
      RXcnt=0;
    }
    RXcnt++;

    if (servo1RX >180) servo1RX=180;
    if (servo1RX<0) servo1RX=0;
    Servo1.write(servo1RX);

    if (servo2RX >180) servo2RX=180;
    if (servo2RX<0) servo2RX=0;
    Servo2.write(servo2RX);

  }
}
