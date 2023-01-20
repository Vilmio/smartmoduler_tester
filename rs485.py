import time
import os
import serial
import modbus
import platform

class Com:

    def __init__(self) -> None:
        print("INIT SERIAL PORT ...")
        self.data = Data()
        self.timeout = 1
        self.baudrate = 9600
        self.status = "Inactive"
        self.firmwareVersion = self.get_fimrwareVersion()
        self.com = "None"
        self.init_serial()
        self.modbusClient = modbus.Modbus()


    def get_fimrwareVersion(self):
        arr = os.listdir()
        for i in arr:
            if i[-3:] == "bin":
                version = i[:-4]
                version = version.split("_")
                return version[1]
        return "0.0"
    
    def init_serial(self):
        if (platform.system() == "Darwin"):
            self.com = "/dev/tty.usbserial-2120"
        elif (platform.system() == "Windows"):
            self.com = "/dev/tty.usbserial-2120"
        else:
            self.com = "/dev/tty.usbserial-2120"
        self.serial = serial.Serial(self.com, self.baudrate, timeout=self.timeout)
        self.serial.close()
        self.serial.open()
            
    def updateData(self):
        reg:int = 5000
        length:int = 12
        try:
            readRegs = self.modbusClient.read_regs(reg, length)
            self.serial.write(readRegs)
            receiveData = self.serial.read(5+(2*length))
            receiveData = self.modbusClient.mbrtu_data_processing(receiveData)
            
            if receiveData[0] == 0:
                self.data.evState = "COM ERROR"
            elif receiveData[0] == 1:
                self.data.evState = "EV UNPLUG"
            elif receiveData[0] == 1:
                self.data.evState = "EV PLUG"
            elif receiveData[0] == 1:
                self.data.evState = "EV CHARGING"   
            elif receiveData[0] == 1:
                self.data.evState = "ERROR"                                
            self.data.rfidCounter = receiveData[4]
            self.data.rfidLength = receiveData[5]

            if self.data.rfidLength == 4:
                self.data.rfidID = hex((receiveData[6]<<16) | (receiveData[7]))

            self.data.evseMaxCurrent = receiveData[11]
        except Exception as e:
            pass

        time.sleep(0.3)
        reg = 4000
        length = 6
        try:
            readRegs = self.modbusClient.read_regs(reg, length)
            self.serial.write(readRegs)
            receiveData = self.serial.read(5+(2*length))
            receiveData = self.modbusClient.mbrtu_data_processing(receiveData)
            
            self.data.U1 = receiveData[3]
            self.data.U2 = receiveData[4]
            self.data.U3 = receiveData[5]
            if(receiveData[0] > 32767):
                self.data.I1 = receiveData[0]-65535
            else:
                self.data.I1 = receiveData[0]
            
            if(receiveData[1] > 32767):
                self.data.I2 = receiveData[1]-65535
            else:
                self.data.I2 = receiveData[1]

            if(receiveData[2] > 32767):
                self.data.I3 = receiveData[2]-65535
            else:
                self.data.I3 = receiveData[2]
                
        except Exception as e:
            self.data.U1 = 0
            self.data.U2 = 0
            self.data.U3 = 0
            self.data.I1 = 0
            self.data.I2 = 0
            self.data.I3 = 0
            self.data.evState = "COMM ERROR"
            self.data.rfidCounter = 0
            self.data.rfidLength = 0
            self.data.rfidID = 0
            self.data.evseMaxCurrent = 0
            print(e)
        
        self.data.serial = self.com
        self.data.serialStatus = self.serial.isOpen()
        time.sleep(0.3)
    

class Data:
    def __init__(self) -> None:
        self.U1 = 0
        self.U2 = 0
        self.U3 = 0
        self.I1 = 0
        self.I2 = 0
        self.I3 = 0
        self.evState = 0
        self.rfidCounter = 0
        self.rfidLength = 0
        self.rfidID = 0
        self.evseMaxCurrent = 0
        self.serial = "None"
        self.serialStatus = False