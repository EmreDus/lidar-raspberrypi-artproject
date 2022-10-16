#version 0.3 ---> haberlesme eklendi - music loop düzeltildi - lidar mirror angle yanlis hesaplama duzeltildi.
#motor rpm = 400 - inrange fonksiyonu silinip kodun icine yazildi (index bilgisi icin) -
# try, except eklendi - 

# minimamodbus kapalı

#simple laser scan reader 

#this project working on conda virtual environment (lidar_project)
#python version = 3.6.3


#lidar library --> pip3 install rplidar-roboticia

#github repo : https://github.com/Roboticia/RPLidar
# documents : https://rplidar.readthedocs.io/en/latest/

#most common error : descriptor length mismatch

# details....





from curses import baudrate
from gettext import find

from numpy import angle
from rplidar import RPLidar
from audioplayer import AudioPlayer

#related with modbus communication
import minimalmodbus
import serial
import time

'''
def com_modbus():
    
    #modbus features
    try:
        instrument = minimalmodbus.Instrument("/dev/ttyUSB0",1,mode="rtu",debug=False) # port name, slave address (in decimal)
    except:
        try:
            instrument = minimalmodbus.Instrument("/dev/ttyUSB1",1,mode="rtu",debug=False) 
        except:
            instrument = minimalmodbus.Instrument("/dev/ttyUSB2",1,mode="rtu",debug=False)
            
            
    #instrument.serial.port                     # this is the serial port name
    instrument.serial.baudrate = 115200         # Baud
    instrument.serial.bytesize = 8
    instrument.serial.parity   = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    #instrument.serial.timeout  = 1 # seconds
    #instrument.address                         # this is the slave address number
'''
print("Config parameters")
servo_rpm = input("Please enter servo rpm: ")
#instrument.write_register(1, servo_rpm, 1, 16, False)
mirror_tol = input("Please enter mirror angle tolerance: ")
#instrument.write_register(1, mirror_tol, 1, 16, False)


#moving avarage array filter
INDEX = 0
VALUE = 0
SUM = 0
AVERAGED = 0
WINDOW_SIZE = 10

nearRange = 150
farRange =  600


media = AudioPlayer("Platform1.wav")
media.play(loop=True)
ses = [0,10,20,30,40,50,60,70,80,90,100]
vol=10
media.volume = 0

#baudrate is important
def com_lidar():
    try:
        lidar = RPLidar('/dev/ttyUSB2', baudrate=256000)
        lidar.stop_motor()
        lidar.stop()

    except:
        try:
            lidar = RPLidar('/dev/ttyUSB1', baudrate=256000)
            lidar.stop_motor()
            lidar.stop()

        except:
            lidar = RPLidar('/dev/ttyUSB0', baudrate=256000)
            lidar.stop_motor()
            lidar.stop()

    return lidar
    
lidar = com_lidar()
#com_modbus()
lidar._motor_speed = 400

mirror_list = [0,0,0,0,0,0,0,0,0,0]

x_list = []
index_list = []

#instrument.write_register(1, 0, 1, 16, False) 
#instrument.write_register(0, 0, 1, 16, False)


inRange = 0
inRange2 = 0
inRange3 = 0
for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    scan_list = [x[2] for x in scan]
    angle_list = [x[1] for x in scan]
    x_list = []
    index_list = []
    
    y_list = []
    index2_list = []


    #idx,inRange = findRange(scan_list)
    for idx,x in enumerate(scan_list):
        if(x>nearRange and x<farRange):
            inRange = 1
            idx_1 = idx
            x_list.append(x)
            index_list.append(idx_1)
        
            
    
    
    print("inRange..........")
    #print(inRange)
    
    
    
    
    
    #check first object in 1m range
    if inRange ==1:
        print("...mirror moving for 1 near angle...")

        if (vol<0):
            vol=0
        if (vol>100):
            vol=100
        media.volume = vol
        vol = vol+2
        
        #near_scan = min(scan_list)
        #print(near_scan)
        #index = scan_list.index(near_scan)
        nearest = min(x_list)
    
        if nearest == True:
            inRange = 1
        else:
            inRange = 0
            
        index_new = x_list.index(nearest)

        near_angle = angle_list[index_new]
        
        #bu parametre ayarlanacak
        config_parameter = 135

        min_angle = near_angle - config_parameter
        max_angle = near_angle + config_parameter
        
        if(min_angle < 0):
            temp = max_angle
            max_angle = 360+min_angle
            min_angle = temp
            
        if(max_angle > 360):
            temp2 = max_angle
            max_angle = min_angle
            min_angle = temp2-360
        #print("min angle", min_angle) 
        #print("max_angle", max_angle)

        #print("near scan cm: ",near_scan)
        #print(near_scan)
        print("near angle: ")
        print(near_angle)
        #print("min angle: ")
        #print(min_angle)
        #print("max angle: ")
        #print(max_angle)
        
        second_list = []
        
        for j,angle in enumerate(angle_list):
            #print("angle value of enumerate: ")
            #print(angle)
            if 135 < near_angle < 225:
                if ((0 < angle < min_angle) or (max_angle < angle < 360)):
                    second_list.append(scan[j])
            else:
                if(min_angle < angle < max_angle):
                    second_list.append(scan[j])
                    
                

        
        scan_list2 = [x_2[2] for x_2 in second_list]

        #inRange2 = findRange(scan_list2)
        for idx_22,y in enumerate(scan_list2):
            if(y>nearRange and y<farRange):
                inRange2 = 1
                idx_2 = idx_22
                y_list.append(y)
                index2_list.append(idx_2)
                
            else:
                inRange2 = 0
        print("....range for second ...")
        print(inRange2)
        
        
        #check second object in range of 1m
        if inRange2 == 1:
            third_list = []            
            angle_list2 = [x_1[1] for x_1 in second_list]
            if len(scan_list2) == 0:
                print("no one close")
            else:     
                #idx2, near2 = min(scan_list2)

                print("near 2 angle: ")
                #index2 = scan_list2.index(near2)
                
                nearest2 = min(y_list)
    
                if nearest == True:
                    inRange = 1
                else:
                    inRange = 0
                
                index_new2 = x_list.index(nearest2)

                near_angle_2 = angle_list2[index_new]
                
                #near_angle_2 = angle_list2[idx_2]

                print(near_angle_2)
                
                thirdMaxRange = near_angle_2 + 135
                thirdMinRange = near_angle_2 + 45
                
                
                for j_2,angle_2 in enumerate(angle_list):
                    #print("angle value of enumerate: ")
                    #print(angle)
                    if 350<angle_2<360 or 0<angle_2<near_angle:
                        if thirdMinRange < angle_2 < thirdMaxRange:
                            third_list.append(scan[j_2])
                    
                
                scan_list3 = [x_3[2] for x_3 in third_list]
                
                
                
                for idx_33,z in enumerate(scan_list3):
                
                    if(z>nearRange and z<farRange):
                        inRange3 = 1
                        idx_3 = idx_33
                        break
                    else:
                        inRange3 = 0
                print("3.kisi :", inRange3)       
                
                
            near_angle = round(near_angle)
            near_angle_2 = round(near_angle_2)
            mirror_angle = round((near_angle + near_angle_2))/2
                
                       
            SUM = SUM - mirror_list[0]
            mirror_list.append(mirror_angle)
            SUM = SUM + mirror_angle
            INDEX = (INDEX + 1) % WINDOW_SIZE
            AVERAGED = SUM / WINDOW_SIZE
                
            #print("averaged with filter: ",AVERAGED)
            mirror_angle = round(AVERAGED)
            
            
            if (len(mirror_list) > 10):
                mirror_list.pop(0)
                            
            #else:
            #    mirror_angle = sum(mirror_list) / len(mirror_list)
           
            print("mirror angle:")
            print(mirror_angle)
            
            #instrument.read_register(0, 0, 3, False) # registeraddress, no of decimal, func code: 3-4, singed=False)  
            if (vol<0):
                vol=0
            if (vol>100):
                vol=100
            media.volume = vol
            vol = vol-8
            
            #instrument.write_register(0, 2, 1, 16, False)
            #instrument.write_register(1, mirror_angle, 1, 16, False) 
        else:
            print(" ")
            #instrument.write_register(0, 1, 1, 16, False)
    else:
        print("no one")
        #send=data.write(b"0") 
        if (vol<0):
            vol=0
        if (vol>100):
            vol=100
        
        media.volume = vol
        vol = vol-8
        #instrument.write_register(0, 0, 1, 16, False)
    
    '''
    if i==1000:
            media.volume = vol
            break
    '''
     
    
print(len(mirror_list))
print(mirror_list)


lidar.stop()
lidar.stop_motor()
lidar.disconnect()





          