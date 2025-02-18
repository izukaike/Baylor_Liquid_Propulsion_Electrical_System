from pycode import System_Health,Telemetry, Metrics
from pycode import V1, V2, V3, V4,C,T,CS,A # this needs coil
import socket
import time

data_arr = []
file_path = "Hotfire_Basic_Sample.xlsx"
#this doesnt do anything 
sys  = System_Health()
#this really connects
tel  = Telemetry(sys)

#send data
'''
tel.open_valve(V1)
tel.spark_coil()
tel.start_test()
tel.set_coil(75)
tel.send_data()
tel.close_valve(V1)
tel.abort()
tel.send_data()
'''
#tel.upload_test_sequence(file_path)


#get data
while True:
    data_arr = tel.get_data()
    print(data_arr)










