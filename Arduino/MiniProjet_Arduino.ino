#include "Motors.h"
#include "Encoders.h"
#include "ControlSystem.h"

#define PINLEDTEST 13
#define DT 5 //sampling period in milliseconds

#define MAXSPEED 15
#define MAXDEGRECART 30
#define MAXDEGRECAMERA 25

char message[10];
int indexMessage = 0;
bool messageAcept = false;

char action[4];
int valAction;

int valMotor1 = 0;
int valMotor2 = 0;
int valMotor3 = 0;

void setup() {
  // put your setup code here, to run once:
  InitMotors();
  InitEncoders();
  
  // initialization of the serial communication.
  Serial2.begin(115200);
  Serial.begin(9600);
}

void loop() {

  if (Serial2.available() > 0) {
    addMessage(Serial2.read());
  }

  if (messageAcept) {
    messageAcept = false;
    
    setMessage();
    setVariables();
    
  }

  waitNextPeriod();
  
  UpdateActuator();
  
}

void setVariables() {
  if (action[1] == 'm' && action[2] == '1') {
    valMotor1 = valAction * MAXDEGRECART / 100;
    
    if (abs(MAXDEGRECART) > 30) {
      valMotor1 = MAXDEGRECART * valMotor1 / abs(valMotor1);
    }
  }
  else if (action[1] == 'm' && action[2] == '2') {
    valMotor2 = valAction * MAXSPEED / 100;
    
    if (abs(valMotor2) > MAXSPEED) {
      valMotor2 = MAXSPEED * valMotor2 / abs(valMotor2);
    }
  }
  else if (action[1] == 'm' && action[2] == '3') {
    valMotor3 = valAction * MAXDEGRECAMERA / 100;
    
    if (abs(valMotor3) > MAXDEGRECAMERA) {
      valMotor3 = MAXDEGRECAMERA * valMotor3 / abs(valMotor3);
    }
  }
}

void UpdateInputSignals(){
  //use getSpeed() declared in Encoder.h
}
  
void UpdateActuator(){
  setMotorAVoltage1(setTensionMotor1(getPosition1(), valMotor1));       //DEGRE
  setMotorAVoltage2(setTensionMotor2(getSpeedMotor2(), valMotor2));     //RPM
  setMotorAVoltage3(setTensionMotor3(getPosition3(), valMotor3));       //DEGRE
}

void setMessage() {
    
  action[0] = message[0];
  action[1] = message[1];
  action[2] = message[2];
  action[3] = '\0';

  char auxVal[7];
  int i;
  for (i = 4; message[i] != '\0'; i++) {
    auxVal[i - 4] = message[i];
    //Serial.println(auxVal[i - 3]);
  }
  
  auxVal[i - 4] = '\0';

  valAction = atoi(auxVal);
  
  Serial.print("Action: ");
  Serial.print(action);
  Serial.print(", Val: ");
  Serial.println(auxVal);
}

void addMessage(int codMessage) {
  if (codMessage == 64 || indexMessage == 10) {
    message[indexMessage] = '\0';
    indexMessage = 0;
    //Serial.println(message);
    messageAcept = true;
  }
  else {
    messageAcept = false;
    message[indexMessage] = codMessage;
    indexMessage++;
  }
}

void waitNextPeriod() 
{
  static long LastMillis=0; 
  long timeToWait = DT - ( millis() - LastMillis) ;
  if(timeToWait>0)
    delay(timeToWait);
  LastMillis=millis();
}
