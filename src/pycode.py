'''
Author: Izuka Ikedionwu

Description: python side to interface with pi and front this is the middle man

features:
- streamlined wifi

Created: 6/28/24
'''

#dependencies

#wifi
import socket
import numpy
import json
import struct

#global variables
PT1 = 0
PT2 = 1
PT3 = 2
PT4 = 3
PT5 = 4
FS  = 5
TS  = 6
RR  = 7
#ToDo: add anymore numbers for front end
class System_Health:
    '''
    Shared Data
    '''
    py_stats  = {}
    pi_stats  = {}
    sys_stats = {}

    #        measurement             default status
    py_stats['init wifi connection']    = 'null'
    py_stats['wifi message tx']         = 'null'
    py_stats['wifi message rx']         = 'null'
    py_stats['v1 open command']         = 'null'
    py_stats['v2 open command']         = 'null'
    py_stats['v3 open command']         = 'null'
    py_stats['v4 open command']         = 'null'
    py_stats['v5 open command']         = 'null'
    py_stats['coil on command']         = 'null'
    py_stats['cal command']             = 'null'
    py_stats['test command']            = 'null'
    py_stats['BM command']              = 'null'

    pi_stats["valve 1 fb"]              = 'null'
    pi_stats["valve 2 fb"]              = 'null'
    pi_stats["valve 3 fb"]              = 'null'
    pi_stats["valve 4 fb"]              = 'null'
    pi_stats["valve 5 fb"]              = 'null'
    pi_stats["coil fb"]                 = 'null'
    pi_stats["pt 1 fb"]                 = 'null'
    pi_stats["pt 2 fb"]                 = 'null'
    pi_stats["pt 3 fb"]                 = 'null'
    pi_stats["pt 4 fb"]                 = 'null'
    pi_stats["pt 5 fb"]                 = 'null'
    pi_stats["lc fb"]                   = 'null'
    pi_stats["thermo 1 fb"]             = 'null'
    pi_stats["thermo 2 fb"]             = 'null'
    pi_stats["abort pt 1 "]             = 'null'
    pi_stats["abort pt 2 "]             = 'null'
    pi_stats["abort pt 3 "]             = 'null'
    pi_stats["abort pt 4 "]             = 'null'
    pi_stats["abort pt 5 "]             = 'null'
    pi_stats["abort pt 6 "]             = 'null'
    py_stats['cal command fb']          = 'null'
    py_stats['test command fb']         = 'null'
    py_stats['BM command fb']           = 'null'
    # still to be updated


    #ToDo Fill in the feedback list

    sys_stats.update(py_stats,**pi_stats) 

     
    def get_pi_status(self):
        return self.pi_stats
    
    
    def get_py_status(self):
        return self.py_stats
    
    @classmethod
    def get_sys_status(self):
        id = 0
        keys = list(self.sys_stats.keys())
        values = list(self.sys_stats.values())

        max_key_length = max(len(key) for key in keys)

        for i in range(len(keys)):
            print(f'{keys[i].ljust(max_key_length)} : {values[i]}')
        return self.sys_stats


class Wifi_Client:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.addy = ''

        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the server
            self.connection.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            System_Health.py_stats["wifi connection"] = 'good'
        except Exception as e:
            print(f"Error: {e} at connect")
            System_Health.py_stats["wifi connection"] = 'bad'
    def send_command(self,d):
        '''
        telemetry packet:
        [heartbeat][data layer][aborts][status data]
        '''
        #form packet
        sent = self.connection.sendall(d)
        System_Health.py_stats["wifi message tx"] = 'good'
    
        if(sent == 0):
            System_Health.py_stats["wifi message tx"] = 'bad'
            raise RuntimeError("socket connection broken at sent")
        return 0
    def recieve_data(self):
        '''
        telemetry packet:
        [heartbeat][data layer][status data]
        '''
        packet_size = 1024
        self.data = self.connection.recv(packet_size)
        print(type(self.data))

        if(self.data == ''):
            System_Health.py_stats["wifi message rx"] = 'bad'
            raise RuntimeError("did not recieve packet")
        else:
            System_Health.py_stats["wifi message rx"] = 'good'

        return self.data

class Wifi_Host:
    def __init__(self,host,port):
    
        #pi ip address 
        self.host   = host
        self.port   = port
        self.connection   = ''
        self.addy   = ''

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                # Bind the socket to the host and port
                server_socket.bind((self.host,self.port))
    
                # Start listening for incoming connections
                server_socket.listen()
                print(f"Server is listening on {self.host}:{self.port}")
                # Accept incoming connections
                self.connection, self.addy = server_socket.accept()
                System_Health.py_stats["init wifi connection"] = 'good'
    

        except Exception as e:
            print(f"Error: {e} at connect")
            System_Health.py_stats["init wifi connection"] = 'bad'
    
    def send_command(self,d):
        '''
        telemetry packet:
        [heartbeat][data layer][aborts][status data]
        '''
        #form packet
        sent = self.connection.sendall(d)
        System_Health.py_stats["wifi message tx"] = 'good'
    
        if(sent == 0):
            System_Health.py_stats["wifi message tx"] = 'bad'
            raise RuntimeError("socket connection broken at sent")
        return 0
    def recieve_data(self):
        '''
        telemetry packet:
        [heartbeat][data layer][status data]
        '''
        packet_size = 1024
        self.data = self.connection.recv(packet_size)
        print(type(self.data))

        if(self.data == ''):
            System_Health.py_stats["wifi message rx"] = 'bad'
            raise RuntimeError("did not recieve packet")
        else:
            System_Health.py_stats["wifi message rx"] = 'good'

        return self.data

#processes incoming data and forms outgoing data packets
class Telemetry:
    def __init__(self,wifi,sys):
        # default 
        #32 bits for 32 commands -> bitwise operations for processing 
        self.heartbeat  = -49 #checksum for verification
        self.coil_speed =  80 #default coil speed
        self.data       =  0
        self.status     =  6
        self.tail       = -48
        self.data_out   = struct.pack('iiiii',0,0,0,0,0)
        self.wifi       = wifi
        self.sys        = sys
        #idk how to set up incoming data packets yet

        #all this class does is set and clear bits for the fized data packets coming in and out
        
        ''' 
        Data out
        byte                         bits
        [heartbeat]||[valve1][valve2][valve3][valve4][coil]|[coil speed]
        '''
                


    #add heartbeat -> header for data
    def set_coil(self,ms):
        self.coil_speed = ms
        return 0

    def send_data(self):
        self.wifi.send_command(self.send_data_out())
        return 0
    
    #function that starts processing the incoming data
    def get_data(self):
        rx = self.wifi.recieve_data()

        #check start byte
        start = 0
        if (rx[start] << (32-8)) == -49:
            print("*process message")
        else: 
            print("no start byte detected")
            return -1
        #ToDo: finish this function 
        #what what is my data packet look like and what am I expecting

        return rx

    def open_valve(self, num):
        #set msb
        #this should be handled at the get data section of the code
        self.data = self.data | (1 << (num-1))
        System_Health.py_stats["v f'{num} open command"] = 'good'
        return 0 
    
    
    def close_valve(self, num):
        #clear msb
        self.data = self.data & ~(1 << (num-1)) 
        System_Health.py_stats["v{num} open command"] = 'bad'
        return 0
    def spark_coil(self):
        self.data = self.data & ~(1 << 6) 
        System_Health.py_stats["v{num} open command"] = 'bad' #status gets cleared from pi side
        return 0

    #not used by front-end
    def send_data_out(self):
        self.data_out = struct.pack('iiiii',self.heartbeat,self.data,self.status,self.coil_speed,self.tail)
        return self.data_out

#collects data and visualizes it for System_Health analysis

#todo finish this class
class Metrics:
    def __init__(self):
        print("metrics")







            
