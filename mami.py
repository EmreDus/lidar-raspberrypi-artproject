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

mirror_list = []

true_list = []

#instrument.write_register(1, 0, 1, 16, False) 
#instrument.write_register(0, 0, 1, 16, False)


inRange = 0
inRange2 = 0
inRange3 = 0

list_0_45 = []
flag_1 = False
flag_2 = False
flag_3 = False
flag_4 = False
flag_5 = False
flag_6 = False
flag_7 = False
flag_8 = False

flag_1_5 = False

angle1 = -1
angle2 = -1
angle3 = -1
angle4 = -1
angle5 = -1
angle6 = -1
angle7 = -1
angle8 = -1



for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    scan_list = [x[2] for x in scan]
    angle_list = [x[1] for x in scan]
    list_0_45 = []
    list_45_90 = []
    list_90_135 = []
    list_135_180 = []
    list_180_225 = []
    list_225_270 = []
    list_270_315 = []
    list_315_360 = []
    #idx,inRange = findRange(scan_list)
    for angle in angle_list:
        if (0 < angle < 45):
            index_1 = angle_list.index(angle)
            list_0_45.append(index_1)
        if (45 < angle < 90):
            index_2 = angle_list.index(angle)
            list_45_90.append(index_2)
            
        if (90 < angle < 135):
            index_3 = angle_list.index(angle)
            list_90_135.append(index_3)
            
            
        if (135 < angle < 180):
            index_4 = angle_list.index(angle)
            list_135_180.append(index_4)
         
        
        if (180 < angle < 225):
            index_5 = angle_list.index(angle)
            list_180_225.append(index_5)
        
        
        if (225 < angle < 270):
            index_6 = angle_list.index(angle)
            list_225_270.append(index_6)
            
            
        if (270 < angle <315):
            index_7 = angle_list.index(angle)
            list_270_315.append(index_7)
            
        if (315 < angle < 360):
            index_8 = angle_list.index(angle)
            list_315_360.append(index_8)      
       
            
            
        
    
    for j in range(len(list_0_45)):
        if  scan_list[list_0_45[j]] > nearRange and scan_list[list_0_45[j]] < farRange:
            angle1 = angle_list[list_0_45[j]]
            flag_1 = True
            break
        else:
            flag_1 = False
            angle1 = -1
            
    for j in range(len(list_45_90)):
        if  scan_list[list_45_90[j]] > nearRange and scan_list[list_45_90[j]] < farRange:
            angle2 = angle_list[list_45_90[j]]
            flag_2 = True
            break
        else:
            flag_2 = False
            angle2 = -1
        
            
    for j in range(len(list_90_135)):
        if  scan_list[list_90_135[j]] > nearRange and scan_list[list_90_135[j]] < farRange:
            angle3 = angle_list[list_90_135[j]]
            flag_3 = True
            break
        else:
            flag_3 = False
            angle3 = -1
            
    for j in range(len(list_135_180)):
        if  scan_list[list_135_180[j]] > nearRange and scan_list[list_135_180[j]] < farRange:
            angle4 = angle_list[list_135_180[j]]
            flag_4 = True
            break
        else:
            flag_4 = False
            angle4 = -1
            
    for j in range(len(list_180_225)):
        if  scan_list[list_180_225[j]] > nearRange and scan_list[list_180_225[j]] < farRange:
            angle5 = angle_list[list_180_225[j]]
            flag_5 = True
            break
        else:
            flag_5 = False
            angle5 = -1
            
    for j in range(len(list_225_270)):
        if  scan_list[list_225_270[j]] > nearRange and scan_list[list_225_270[j]] < farRange:
            angle6 = angle_list[list_225_270[j]]
            flag_6 = True
            break
        else:
            flag_6 = False
            angle6 = -1
            
    for j in range(len(list_270_315)):
        if  scan_list[list_270_315[j]] > nearRange and scan_list[list_270_315[j]] < farRange:
            angle7 = angle_list[list_270_315[j]]
            flag_7 = True
            break
        else:
            flag_7 = False
            angle7 = -1
            
    for j in range(len(list_315_360)):
        if  scan_list[list_315_360[j]] > nearRange and scan_list[list_315_360[j]] < farRange:
            angle8 = angle_list[list_315_360[j]]
            flag_8 = True
            break
        else:
            flag_8 = False
            angle8 = -1
            
    true_list = (flag_1, flag_2, flag_3, flag_4, flag_5, flag_6, flag_7, flag_8)
    print("true list: " ,true_list)
    
    true_count = true_list.count(True)
    print("true count", true_count)
    """
    print("1",flag_1)
    print("2",flag_2)
    print("3",flag_3)
    print("4",flag_4)
    print("5",flag_5)
    print("6",flag_6)
    print("7",flag_7)
    print("8",flag_8)
    """
    print("1",angle1)
    print("2",angle2)
    print("3",angle3)
    print("4",angle4)
    print("5",angle5)
    print("6",angle6)
    print("7",angle7)
    print("8",angle8)
   
    if flag_1 == True:
        if flag_5 == True:
            flag_1_5 = True
            mirror_angle = (angle1+angle5)/2
            print("mirror_angle",mirror_angle)
            mirror_list.append(mirror_angle)
            if true_count == 4:
                print("4 var")
        else:
            flag_1_5 = False
            
    if flag_2 == True:
        if flag_6 == True:
            if flag_1_5 == False:
                mirror_angle = (angle2+angle6)/2
                print("mirror_angle",mirror_angle)
                mirror_list.append(mirror_angle)
                if true_count == 4:
                    print("4 var")
    if flag_3 == True:
        if flag_7 == True:
            if flag_1_5 == False:
                mirror_angle = (angle3+angle7)/2
                print("mirror_angle",mirror_angle)
                mirror_list.append(mirror_angle)
                if true_count == 4:
                    print("4 var")
            
    if flag_4 == True:
        if flag_8 == True:
            if flag_1_5 == False:
                mirror_angle = (angle4+angle8)/2
                print("mirror_angle",mirror_angle)
                mirror_list.append(mirror_angle)
                if true_count == 4:
                    print("4 var")
    
    if len(mirror_list) > 10:
        mirror_list.pop(0)
    
    if true_count > 3:
        mirror_angle = mirror_list[len(mirror_list)-2]
        mirror_list.pop(len(mirror_list)-1)
        if len(mirror_list) > 3:
            print("new angle: ", mirror_list[len(mirror_list)-1]) 
    if i==200:
        break
    
"""            
    if flag_5 == True:
        if flag_1 == True:
            mirror_angle = (angle1+angle5)/2
            print("mirror_angle",mirror_angle)
            
    if flag_6 == True:
        if flag_2 == True:
            mirror_angle = (angle6+angle2)/2
            print("mirror_angle",mirror_angle)
            
    if flag_7 == True:
        if flag_3 == True:
            mirror_angle = (angle7+angle3)/2
            print("mirror_angle",mirror_angle)
            
    if flag_8 == True:
        if flag_4 == True:
            mirror_angle = (angle8+angle4)/2
            print("mirror_angle",mirror_angle)        
"""
print(mirror_list)
    
lidar.stop()
lidar.stop_motor()
lidar.disconnect()





          
