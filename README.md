# Full-Stack Rocket Engine Electronics System 🚀

This repository contains the complete embedded system and software stack used to test Baylor Aero's second liquid-fueled rocket engine. With a tight two-semester timeline and a limited budget, the system was designed from scratch to acquire real-time sensor data, control actuators, and replace costly commercial DAQ hardware with a fully custom, robust solution.

## 📸 System Overview

![System Diagram](./v2_diagram.png)

## 🛠 Features

- Real-time data acquisition and actuator control  
- Full-stack embedded system design from power to telemetry  
- Custom firmware and GUI written in C++ and Python (PyQt)  
- Wireless telemetry to ground station via UART → Pi → Wi-Fi  
- Replaces expensive LabVIEW/NI DAQ solutions  

## ⚡️ Core Components

| Electronics                       | Subsystems                |
|----------------------------------|---------------------------|
| 12V–24V Boost Converter          | 4x ADCs                   |
| 7.2V–5V LDO                      | 4x DACs                   |
| Modified Rechargeable Battery    | 3x Relays                 |
| 7.2V–5V Buck Converter           | 2x MOSFETs                |
| Car Battery                      | Raspberry Pi 4B+          |

## 📡 Firmware Details

The firmware runs on an **ATmega328P microcontroller**, written in **C++**, and includes:

- Polling of analog and digital sensors (e.g., pressure transducers)  
- Solenoid valve control (1A–32A range)  
- UART serial communication to ground systems  
- EEPROM-based data retention  
- Signal filtering and overcurrent protection  

## 🖥 GUI + Visualization

A custom GUI built using **Python** and **PyQt** enables:

- Serial communication and test sequencing  
- Real-time visualization of pressure and system state  
- Synchronized sampling and ADC calibration  
- Safety and fault detection logic  

## 🧠 Skills Used

- Embedded Systems Design  
- Power Electronics & Regulation  
- Python GUI Development (PyQt)  
- Microcontroller Firmware (C++)  
- Signal Conditioning  
- Wireless Telemetry (UART → Pi → Wi-Fi)  
- Systems Integration & Debugging  

## 📁 File Structure
