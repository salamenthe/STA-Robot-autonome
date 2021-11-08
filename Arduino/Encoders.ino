#include "Encoders.h"

volatile int position1 = 0;
volatile long duration1 = 0;
volatile long timeOfLastPulse1 = 0;
volatile char dir1 = 0;

volatile int position2 = 0;
volatile long duration2 = 0;
volatile long timeOfLastPulse2 = 0;
volatile char dir2 = 0;

volatile int position3 = 0;
volatile long duration3 = 0;
volatile long timeOfLastPulse3 = 0;
volatile char dir3 = 0;

int getPosition1()
{
  noInterrupts();
  int temp = position1;
  interrupts();
  return temp;
}

int getPosition2()
{
  noInterrupts();
  int temp = position2;
  interrupts();
  return temp;
}

int getPosition3()
{
  noInterrupts();
  int temp = position3;
  interrupts();
  return temp;
}

// get the actual speed, computed from the time between two pulses.
float getSpeedMotor1(){
  noInterrupts();
  long tempDur = duration1;
  char tempDir = dir1; 
  interrupts();
  if(tempDur == 0)
    return 0;
  else 
    if(tempDir>0)
      return 1000000.0/( (float)tempDur );
    else 
      return -1000000.0/( (float)tempDur );
    
}

float getSpeedMotor2(){
  noInterrupts();
  long tempDur = duration2;
  char tempDir = dir2; 
  interrupts();
  if(tempDur == 0)
    return 0;
  else 
    if(tempDir>0)
      return 1000000.0/( (float)tempDur );
    else 
      return -1000000.0/( (float)tempDur );
    
}

float getSpeedMotor3(){
  noInterrupts();
  long tempDur = duration3;
  char tempDir = dir3; 
  interrupts();
  if(tempDur == 0)
    return 0;
  else 
    if(tempDir>0)
      return 1000000.0/( (float)tempDur );
    else 
      return -1000000.0/( (float)tempDur );
    
}

void InitEncoders()
{ 
  pinMode(PORT1_NE2,INPUT_PULLUP);
  pinMode(PORT1_NE1,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PORT1_NE2),ISR_encoder1,RISING);

  pinMode(PORT2_NE2,INPUT_PULLUP);
  pinMode(PORT2_NE1,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PORT2_NE2),ISR_encoder2,RISING);
  
  pinMode(PORT3_NE2,INPUT_PULLUP);
  pinMode(PORT3_NE1,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PORT3_NE2),ISR_encoder3,RISING);
}


// fonction appelée lors des interruptions 'front montant'
void ISR_encoder1(){
  long newTime = micros();
  if(digitalRead(PORT1_NE1)) // detection du sens de rotation
    {
      position1++;
      dir1 = 1;
    }
    else
    {
      position1--;
      dir1 = -1;
    }
  duration1 = newTime - timeOfLastPulse1;
  timeOfLastPulse1 = newTime;
}

void ISR_encoder2(){
  long newTime = micros();
  if(digitalRead(PORT2_NE1)) // detection du sens de rotation
    {
      position2++;
      dir2 = 1;
    }
    else
    {
      position2--;
      dir2 = -1;
    }
  duration2 = newTime - timeOfLastPulse2;
  timeOfLastPulse2 = newTime;
}

void ISR_encoder3(){
  long newTime = micros();
  if(digitalRead(PORT3_NE1)) // detection du sens de rotation
    {
      position3++;
      dir3 = 1;
    }
    else
    {
      position3--;
      dir3 = -1;
    }
  duration3 = newTime - timeOfLastPulse3;
  timeOfLastPulse3 = newTime;
}
