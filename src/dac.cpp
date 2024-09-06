/*

Author: Izuka Ikedionwu

Description: uMicro controller that interfaces with DAC's and pi for sensor testing

Date Created 9/6/24

*/

#include <MCP48xx.h>

//12 bit resolution
MCP48xx<12> dac(10);
 
//Max is 4.096 using internal reference but that is fine because maximum is not needed
int voltage = 5000;
bool down = false;
void setup() {
    Serial.begin(115200);
    pinMode(A1,INPUT);
    // We call the init() method to initialize the instance
    dac.init();

    // The channels are turned off at startup so we need to turn the channel we need on
    dac.turnOnChannelA();
    dac.turnOnChannelB();

    // We configure the channels in High gain
    // It is also the default value so it is not really needed
    dac.setGainA(MCP4822::High);
    dac.setGainB(MCP4822::High);

    dac.setVoltageA(voltage);
    dac.setVoltageB(voltage);
}

void loop() {


    //used t 
    dac.updateDAC();

}