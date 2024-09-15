#include <MCP48xx.h>
#include <math.h>  // Needed for sin() and exp() functions
const int BIT = 12;
// Define the MCP4822 instance, giving it the SS (Slave Select) pin
MCP48xx<12> d1(10);
MCP48xx<12> d2(9);
MCP48xx<12> d3(8);
MCP48xx<12> d4(7);

void init_dac(MCP48xx<BIT> *d)
{
  d->turnOnChannelA();
  d->turnOnChannelB();

  d->setGainA(MCP4822::High);
  d->setGainB(MCP4822::High);

  d->init();
  
}


void setup() {
    Serial.begin(115200);
    pinMode(A0,INPUT);
    pinMode(A5,INPUT);
    
    init_dac(&d1);
    init_dac(&d2);
    init_dac(&d3);
    init_dac(&d4);
}

void sweep(MCP48xx<BIT>* d, char c, int top,int bottom)
{
  int voltage = bottom;
  int del = 2;
  int jump = 50;
  if( c == 'A')
  {
    while(voltage < top)
      {
        voltage  += jump;
        d->setVoltageA(voltage);
        d->updateDAC();// Update the DAC with the new voltage value
        delay(del);
        
      }
      d->setVoltageA(bottom);
      d->updateDAC();
  }
  else
  {
    while(voltage < top)
      {
        voltage  += jump;
        d->setVoltageB(voltage);
        d->updateDAC();// Update the DAC with the new voltage value
        delay(del);
        
      }
      d->setVoltageB(bottom);
      d->updateDAC();
  }
}

// Loop to generate exponentially growing amplitude sine wave
void loop() {
    sweep(&d1,'A',2700,1700);
    sweep(&d1,'B',2700,1700);
    sweep(&d2,'A',2500,1500);
    sweep(&d2,'B',2500,1500);
    sweep(&d3,'A',2700,1700);
    sweep(&d3,'B',2700,1700);
    sweep(&d4,'A',2700,1700);
    sweep(&d4,'B',2700,1700);
}
