#include <MCP48xx.h>
#include <math.h>  // Needed for sin() and exp() functions

// Define the MCP4822 instance, giving it the SS (Slave Select) pin
MCP48xx<12> dac(10);

// Variables to store voltage and time step
int voltage = -100;
float t = 0;  // Time variable for the sine wave
const float frequency = 10000; // Frequency in Hz
const float b = 1.001;        // Exponential growth rate
const float pi = 3.14159265359;
const int sampleRate = 50;  // Samples per second (adjust as needed)

void setup() {
    Serial.begin(115200);
    pinMode(A5, INPUT);

    // Initialize the DAC
    dac.init();
    
    // Turn on channels A and B
    dac.turnOnChannelA();
    dac.turnOnChannelB();

    // Configure the DAC channels in High gain mode
    dac.setGainA(MCP4822::High);
    dac.setGainB(MCP4822::High);
}

// Loop to generate exponentially growing amplitude sine wave
void loop() {

    voltage  += 1;
    dac.setVoltageA(voltage);
    dac.setVoltageB(voltage);
    dac.updateDAC();  // Update the DAC with the new voltage value
    delay(10);
    // Read analog input A5 and convert it to a voltage (for debugging)
    int val = analogRead(A5);
    double r = (val / 1023.0) * 5;
    double w = voltage / 1000.0;
    Serial.println(r);
    Serial.println(w);

    if(voltage > 5100)
    {
       voltage = -100;
    }
}

// Helper function to map a float value to a range
int mapFloat(float x, float in_min, float in_max, int out_min, int out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}