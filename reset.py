import minimalmodbus
import serial
from curses import baudrate


def com_modbus():
    
    try:
        instrument = minimalmodbus.Instrument("/dev/ttyUSB2",1,mode="rtu",debug=False)
        instrument.serial.baudrate = 115200         # Baud
        instrument.serial.bytesize = 8
        instrument.serial.parity   = serial.PARITY_NONE
        instrument.serial.stopbits = 1
    except:
        try:
            instrument = minimalmodbus.Instrument("/dev/ttyUSB1",1,mode="rtu",debug=False)
            instrument.serial.baudrate = 115200         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
        except:
            instrument = minimalmodbus.Instrument("/dev/ttyUSB2",1,mode="rtu",debug=False)
            instrument.serial.baudrate = 115200         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
    
    return instrument
        

instrument = com_modbus()

inp = input("For reset the system press 'r' and then enter (if not just press enter): ")

if inp == 'r':
    instrument.write_register(250, 1, 0, 16, False) 
    print("Reset complited")
else:
    instrument.write_register(250, 0, 0, 16, False) 
    print("Reset passed")
print("Config parameters")

servo_rpm1 = int(input("Please enter servo rpm 1: "))
instrument.write_register(200, servo_rpm1, 0, 16, False)

servo_rpm2 = int(input("Please enter servo rpm 2:  "))
instrument.write_register(210, servo_rpm2, 0, 16, False)

ramp_value = int(input("Please enter servo ramp value: "))
instrument.write_register(220, ramp_value, 0, 16, False)

mirror_tol = int(input("Please enter mirror angle tolerance: "))
instrument.write_register(230, mirror_tol, 0, 16, False)

light_time = int(input("Please enter light fadeout / fadein time: "))
instrument.write_register(240, light_time, 0, 16, False)

 