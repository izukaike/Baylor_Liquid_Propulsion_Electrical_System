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

wd = np.array([])
rd = np.array([])
diff = np.array([])
x1 = []
x2 = []
# Custom matplotlib canvas to embed in the PyQt app
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=200):
        self.fig, self.ax = plt.subplots(1,2,figsize=(10,6),dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

    def plot_data(self,x1, y1,x2,y2,x3,diff):
        # Clear previous plot
        self.ax[0].clear()
        self.ax[1].clear()

        # Plot the data     rd  
        self.ax[0].plot(x1, y1, label="DAC Out",color='blue')
        #                    wd
        self.ax[0].plot(x2, y2, label="DAC In",color='green')
        self.ax[1].plot(x3,diff,label="Difference")


        self.ax[0].set_ylim(-0.5,5)
        self.ax[1].set_ylim(-100,100)

        print(self.ax[0].get_ylim())
        # Label every 10th point
        #for i in range(0, len(x1), 10):
        #    self.ax[0].text(x1[i], y1[i], f'({x1[i]:.1f}, {y1[i]:.2f})', fontsize=8)

        # Set title and labels
        self.ax[0].set_title('DAC: Write vs Read Voltage')
        self.ax[0].set_xlabel('Sample Index')
        self.ax[0].set_ylabel('Volts')
        self.ax[0].grid(True)

        self.ax[1].set_title('DAC: Write vs Read')
        self.ax[1].set_xlabel('Sample Index')
        self.ax[1].set_ylabel('Difference')
        self.ax[1].grid(True)
        self.ax[1].legend()
        self.ax[0].legend()

        # Add labels for every 20th data point
        for i in range(0, len(x1), 250):  # Labels every 20th entry
            self.ax[0].annotate(f'{rd[i]:.2f}', (x1[i], rd[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=7, color='blue')
            # Text below for wd (blue line)
            self.ax[0].annotate(f'{wd[i]:.2f}', (x2[i], wd[i]), textcoords="offset points", xytext=(0, -10), ha='center', fontsize=7, color='green')

        for i in range(0, len(x1), 250):  # Labels every 20th entry
            self.ax[1].annotate(f'{diff[i]:.2f}', (x1[i], diff[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=7, color='black')
            # Text below for wd (blue line)

        index = 0
        s = 0
        avg = 0
        diff = np.abs(diff)
        for i in range(len(x2)):
            if(diff[i] == max(diff)):
                index = i
                l = diff[i]


        avg = s/len(x2)
        plt.scatter(index, l , color='r', s=5, label="Highlighted Point")
        self.ax[1].annotate("Max Error: " + f'{diff[index]:.2f}'+"V", (x1[index], diff[index]), textcoords="offset points", xytext=(0, 30), ha='center', fontsize=7, color='black')
        self.ax[1].annotate("Avg. Error: " + f'{avg:.2f}'+"V", (x1[index], diff[index]), textcoords="offset points", xytext=(0, 20), ha='center', fontsize=7, color='black')

        

            

        # Draw plot
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("PyQt5 Plot with Selective Labels")

        # Create a widget and layout for embedding the matplotlib plot
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Create the matplotlib canvas (plotting area)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=200)

        # Add the canvas to the layout
        layout.addWidget(self.canvas)

        # Call the function to plot data with selective labels
        self.canvas.plot_data(x1,rd,x2,wd,x2,diff)

#xfile = openpyxl.load_workbook("dac_data.xlsx")
#sheet = xfile.active

# Configure the serial port (adjust COM port and baud rate as needed)
serial_port = 'COM6'  # Replace with your Arduino's COM port
baud_rate = 115200      # Set the baud rate that matches your Arduino
timeout = 1        # Timeout for the serial read


# Initialize the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

# List to store the data
data = []
if __name__ == "__main__":
    
    try:
        print("Collecting data... Press Ctrl+C to stop and plot.")
        while True:
            #print(ser.in_waiting)
            # Read the serial data line
            serial_line = ser.read(ser.in_waiting).decode('utf-8')
            #print(serial_line)
            #print("\n\n\n")
            if serial_line != '':
                try:
                    data.append(serial_line)
                    #print(data)
                except ValueError:
                    print("Received invalid data. Skipping...")
            time.sleep(0.01)  # Adjust the sleep to control the read frequency

    except KeyboardInterrupt:
        print("Exiting and plotting the data...")

    finally:
        # Close the serial connection
        for i in range(len(data)):
            t = data[i]
            arr = t.split("\r\n")
            for j in range(len(arr)):
                #this skips end data
                if(arr[j] == 's' and len(arr[j:]) > 3 ):
                    rd = np.append(rd,arr[j+1])
                    wd = np.append(wd,arr[j+2])
        
            # Create the application
        x1 = np.linspace(0, len(rd), len(rd),dtype=int)
        x2 = np.linspace(0, len(wd), len(wd),dtype=int)
        new_x1 = []
        new_x2 = []
        new_rd = []
        new_wd = []
        x1 = x1.astype(float)
        x2 = x2.astype(float)
        rd = rd.astype(float)
        wd = wd.astype(float)
        for i in range(len(x2)):
            #print(((rd[i]-wd[i])/(wd))*100)
            val = ((rd[i]-wd[i]))
            diff = np.append(diff,val)
                            
       

        print("size: diff: " +str(len(diff)))
        print("size: x2 " +str(len(x2)))



        #print(wd)
        app = QApplication(sys.argv)

        # Create and display the main window
        main_window = MainWindow()
        main_window.show()

        # Start the PyQt event loop
        sys.exit(app.exec_())
        '''
        print(max(rd))
        print(min(rd))
        print(max(wd))
        print(min(wd))

        row_num = 1
        #for value in rd:
            #sheet.append([value])
        #xfile.save("dac_data.xlsx")
        ser.close()

        # Plot the data after exiting
        fig, ax = plt.subplots(figsize=(10, 6))

            # Create x-axis values
        x1 = np.linspace(0, len(rd), len(rd))
        x2 = np.linspace(0, len(wd), len(wd))

        print("size of rd: " + str(len(rd)))
        print("size of wd: " + str(len(wd)))

        # Plot data
        ax.plot(x1, rd, label="Serial Data", color='g')
        ax.plot(x2, wd, label="Voltage", color='b')

        # Set y-axis limits
        ax.set_ylim(bottom=-0.1,top=(5))

        # Set the plot title and labels
        ax.set_title("Collected Serial Data")
        ax.set_ylabel("Values")

            # Add a legend and grid
        ax.legend()
        ax.grid(True)

        # Show the plot
        plt.show()
        '''
        