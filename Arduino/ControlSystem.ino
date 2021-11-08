#include "ControlSystem.h"

int sumErrorMotor1;
int lastTensionMotor1;
int lasDirectionMotor1;
double KpMotor1 = 0.05;
double KiMotor1 = 0.0001;
int lastValMotor1;

int sumErrorMotor2;
int lastTensionMotor2;
int lasDirectionMotor2;
double KpMotor2 = 0.05;
double KiMotor2 = 0.0001;
int lastValMotor2;

int sumErrorMotor3;
int lastTensionMotor3;
int lasDirectionMotor3;
int lastValMotor3;

int setTensionMotor1(int positionCurrent, int positionDesired) {

  if (lastValMotor1 != positionDesired) {
    sumErrorMotor1 = 0;
  }
  
  sumErrorMotor1 = positionDesired;

  positionDesired = DEGRETOSIGNAL * positionDesired;
  int error = positionDesired - positionCurrent;

  if (abs(error) < MINERROR)
    return 0;
  
  int tensionMotor1;

  if (abs(lastTensionMotor1) < MAXTENSION || error / abs(error) != lasDirectionMotor1 / abs(lasDirectionMotor1)) {
    sumErrorMotor1 += error * DT;
  }

  tensionMotor1 = error * KpMotor1 + 1.0 * sumErrorMotor1 * KiMotor1;
  lasDirectionMotor1 = tensionMotor1 / abs(tensionMotor1);
  lastTensionMotor1 = tensionMotor1;

  return tensionMotor1;
}

int setTensionMotor2(int speedCurrent, double speedDesired) {

  if (lastValMotor2 != speedDesired) {
    sumErrorMotor2 = 0;
  }
  
  lastValMotor2 = speedDesired;

  if (speedDesired == 0) {
    return 0;
  }

  speedDesired = speedDesired * TURNCOMPLETREAR / 60.0;
  int error = speedDesired - speedCurrent;

  if (abs(error) < MINERROR)
    return 0;
  
  int tensionMotor2;

  sumErrorMotor2 += error * DT;

  tensionMotor2 = error * KpMotor2 + 1.0 * sumErrorMotor2 * KiMotor2;
  lasDirectionMotor2 = tensionMotor2 / abs(tensionMotor2);
  lastTensionMotor2 = tensionMotor2;

  return tensionMotor2;
}

int setTensionMotor3(int positionCurrent, int positionDesired) {

  positionDesired = DEGRETOSIGNAL * positionDesired;
  int error = positionDesired - positionCurrent;

  if (abs(error) < MINERROR)
    return 0;
  
  int tensionMotor3;

  if (abs(lastTensionMotor3) < MAXTENSION || error / abs(error) != lasDirectionMotor3 / abs(lasDirectionMotor3)) {
    sumErrorMotor3 += error * DT;
  }

  tensionMotor3 = error * KpMotor1 + 1.0 * sumErrorMotor3 * KiMotor1;
  lasDirectionMotor3 = tensionMotor3 / abs(tensionMotor3);
  lastTensionMotor3 = tensionMotor3;

  return tensionMotor3;
}
