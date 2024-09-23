import pyvisa
import time

rm = pyvisa.ResourceManager()

f1 = open("ref_data.txt", 'w+')
f2 = open("in_data.txt", 'w+')

f4 = open("adc_read.txt",'w+')
f5 = open("pitime.txt",'w+')


f1.write('')
f2.write('')

f4.write('')
f5.write('')


f1.close()
f2.close()
f4.close()
f5.close()

f1 = open("ref_data.txt", 'w+')
f2 = open("in_data.txt", 'w+')
f4 = open("adc_read.txt",'r')
f5 = open("pitime.txt",'r')



a1 = []
a2 = []
a3 = []
a4 = []
a5 = []


oscope = rm.open_resource('USB0::0x0957::0x179B::MY53401346::0::INSTR')

#oscope.timeout = 500#
#oscope.write('*CLS')
begin = time.time()
elapse = 0
try:
    while elapse < 15:
        #d1 = oscope.query(':MEASure:VRMS? DISplay,DC,CHANnel1')
        #d2 = oscope.query(':MEASure:VRMS? DISplay,DC,CHANnel2')

        d1 = oscope.query(':MEASure:VAVerage? DISplay,CHANnel1')
        d2 = oscope.query(':MEASure:VAVerage? DISplay,CHANnel2')

        now = time.time()
    
        a1.append(float(d1))
        a2.append(float(d2))
        elapse = (now-begin)
        print(elapse)
        a3.append(elapse)
except KeyboardInterrupt:
    print("oops!")
finally:

    for i in range(len(a1)):
        f1.write(str(a1[i])  + '\n')
        f2.write(str(a2[i])  + '\n')
        #f3.write(str( a3[i]*1000) + "\n")

    f1.close()
    f2.close()
    oscope.close()
    rm.close()







