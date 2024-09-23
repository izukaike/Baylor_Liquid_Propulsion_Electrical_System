from data_viz(dac_test) import  MplCanvas, MainWindow
import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import openpyxl
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

'''
f1 = open("ref_data.txt", 'w+')
f2 = open("in_data.txt", 'w+')
f3 = open("time.txt",'w+')
f4 = open("adc_read.txt",'w+')
f5 = open("pitime.txt",'w+')


f1.write('')
f2.write('')
f3.write('')
f4.write('')
f5.write('')


f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
'''

f1 = open("ref_data.txt", 'r')
f2 = open("in_data.txt", 'r')
f3 = open("time.txt", 'r')
f4 = open("adc_read.txt",'r')
f5 = open("pitime.txt",'r')

a1 = np.array([])
a2 = np.array([])
a3 = np.array([])
a4 = np.array([])
a5 = np.array([])
a6 = np.array([])

s1 = 0

s2 = 0

for i in range(50):
    dat = f1.readline()
    day = f2.readline()

    if dat != '':
        s1 += float(dat)
    if day != '':
        s2 += float(day)


ref = float(s1/50)
dac = float(s2/50)

d1 = 1
d3 = 1
d4 = 1
for i in range(10000):

    daq = f4.readline()
    #print(daq)
    dax = f5.readline()

    if daq != '':
        d1 = float(daq) # adc voltage
        d1 = (1-( (d1+207)/4095))*ref
        
    if dax != '':
        d3 = float(dax) # time
        d3 /= 1000

    d4 = abs(((d1-dac)/ref)*100)
    if d4 <= 0:
        print("neg")

    
    a1 = np.append(a1,[d1])
    a2 = np.append(a2,[dac])
    a3 = np.append(a3,[d3])
    a4 = np.append(a4,[d4])
    


a1 = a1.astype(float)
a2 = a2.astype(float)
a3 = a3.astype(float)
a4 = a4.astype(float)



   

f1.close()
f2.close()
f3.close()
f4.close()
f5.close()

app = QApplication(sys.argv)

        # Create and display the main window
main_window = MainWindow(a3,a1,a3,a2,a3,a4)
main_window.show()

        # Start the PyQt event loop
sys.exit(app.exec_())