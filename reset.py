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
inp = input("For reset the system press 'r' and then enter: ")

if inp == 'r':
    #instrument.write_register(1, 0, 1, 16, False) 
    print("Reset complited")
 