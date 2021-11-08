
#define MAXTENSION 9
#define MINERROR 8

//Turn Complet 5400
#define TURNCOMPLETREAR   5400.0
#define DEGRETOSIGNAL     5400.0 / 360

int setTensionMotor1(int positionCurrent, int positionDesired);
int setTensionMotor2(int speedCurrent, double speedDesired);
int setTensionMotor3(int positionCurrent, int positionDesired);
