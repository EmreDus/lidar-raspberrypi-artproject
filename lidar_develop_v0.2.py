#version 0.1 ---> haberlesme yok - music loop düzeltildi - lidar mirror angle yanlis hesaplama duzeltildi.

#simple laser scan reader 

#this project working on conda virtual environment (lidar_project)
#python version = 3.6.3


#lidar library --> pip3 install rplidar-robotica

#github repo : https://github.com/Roboticia/RPLidar
# documents : https://rplidar.readthedocs.io/en/latest/



#most common error : descriptor length mismatch

# details....


from curses import baudrate
from gettext import find

from numpy import angle
from rplidar import RPLidar
from audioplayer import AudioPlayer

import time
import serial

#data=serial.Serial("/dev/ttyUSB0", 9600) #transmit data serially

#moving avarage array filter
INDEX = 0
VALUE = 0
SUM = 0
AVERAGED = 0
WINDOW_SIZE = 10

def findRange(array):
    for x in array:
        if(x>150 and x<500):
            return 1
            break

media = AudioPlayer("Platform1.wav")
media.play(loop=True)
ses = [0,10,20,30,40,50,60,70,80,90,100]
vol=10
media.volume = 0
#baudrate is important 
lidar = RPLidar('/dev/ttyUSB1', baudrate=256000)

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

mirror_list = [0,0,0,0,0,0,0,0,0,0]

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    scan_list = [x[2] for x in scan]
    angle_list = [x[1] for x in scan]
    
    inRange = findRange(scan_list)
    
    print("inRange..........")
    print(inRange)
    
   
    
        
    #check first object in 1m range
    if inRange ==1:
        print("...mirror moving for 1 near angle...")
        #send=data.write(b"1") # motor dönüyor uart bilgisi 
        
       
        #time.sleep(0.05)
        if (vol<0):
            vol=0
        if (vol>100):
            vol=100
        media.volume = vol
        vol = vol+2
        
        near_scan = min(scan_list)
        print(near_scan)
        index = scan_list.index(near_scan)

        near_angle = angle_list[index]
        
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
        print("min angle", min_angle) 
        print("max_angle", max_angle)

        #print("near scan: ")
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

        inRange2 = findRange(scan_list2)
        print("....range for second ...")
        print(inRange2)
        
        #check second object in range of 1m
        if inRange2 == 1:
              
            z = 0
            angle_list2 = [x_1[1] for x_1 in second_list]
            if len(scan_list2) == 0:
                print("no one close")
            else:     
                near2 = min(scan_list2)

                print("near 2 angle: ")
                index2 = scan_list2.index(near2)
                near_angle_2 = angle_list2[index2]

                print(near_angle_2)
                
                
            near_angle = round(near_angle)
            near_angle_2 = round(near_angle_2)
            mirror_angle = round((near_angle + near_angle_2))/2

            if z<2:
                m_angle_before = mirror_angle
                
                       
            SUM = SUM - mirror_list[0]
            mirror_list.append(mirror_angle)
            SUM = SUM + mirror_angle
            INDEX = (INDEX + 1) % WINDOW_SIZE
            
            AVERAGED = SUM / WINDOW_SIZE
            
            '''                   
            if (abs((mirror_list[WINDOW_SIZE])-(mirror_list[WINDOW_SIZE-1])) > 300):
                print("danger zone")
                print("danger zone")
                print("danger zone")
                print("danger zone")
                mirror_list.pop(WINDOW_SIZE)
            '''                       
                
            print("averaged with filter: ",AVERAGED)
            mirror_angle = round(AVERAGED)
            
            
            if (len(mirror_list) > 10):
                mirror_list.pop(0)
                a=0
            
            
            #else:
            #    mirror_angle = sum(mirror_list) / len(mirror_list)
           
            print("mirror angle:")
            print(mirror_angle)
            z+=1
              
    else:
        print("no one")
        #send=data.write(b"0") 
        if (vol<0):
            vol=0
        if (vol>100):
            vol=100
        
        media.volume = vol
        vol = vol-3
    
    
    if i==500:
            media.volume = vol
            break

print(len(mirror_list))
print(mirror_list)

lidar.stop()
lidar.stop_motor()
lidar.disconnect()





          