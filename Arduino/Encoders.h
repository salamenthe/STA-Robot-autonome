// PIN utilisées pour l'encodeur incrémental
#define PORT1_NE1 31
#define PORT1_NE2 18

#define PORT2_NE1 38
#define PORT2_NE2 19

#define PORT3_NE1 49
#define PORT3_NE2 3

void InitEncoders(); // setup encoder position detection

int getPosition1(); // get the actual position of the incremental encoder in pulse.
int getPosition2();
int getPosition3();

float getSpeedMotor1(); // get the actual speed in pulses/s, computed from the time between two pulses.
float getSpeedMotor2();
float getSpeedMotor3();
