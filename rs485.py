import time
import os
import serial
import modbus
import platform
import sys
import glob
import serial.tools.list_ports

class Com:

    def __init__(self) -> None:
        print("INIT SERIAL PORT ...")
        self.data = Data()
        self.timeout = 1
        self.baudrate = 9600
        self.status = False
        self.firmwareVersion = self.get_fimrwareVersion()
        self.com = "None"
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
        self.com = self.serial_ports()
        if self.com is not None:
            self.serial = serial.Serial(self.com, self.baudrate, timeout=self.timeout)
            self.serial.close()
            self.serial.open()
            self.check_presence()

    def serial_ports(self):
        ports:list = []
        if sys.platform.startswith('win'):
            port = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            port = glob.glob('/dev/tty[A-Za-z]*')
            for p in port:
                if "USB" in p:
                    ports.append(p)
        elif sys.platform.startswith('darwin'):
            port = glob.glob('/dev/tty.*')
            for p in port:
                if "usbserial" in p:
                    ports.append(p)
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        if result:
            return result[0]
        return None
            
    def check_presence(self):
        if sys.platform.startswith('win'):
            myports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            myports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            myports = glob.glob('/dev/tty.*')
        else:
            self.status = False
            return 
        if self.com in myports:
            self.status = True
        else:
            self.status = False


    def updateData(self):
        self.check_presence()

        if self.status == False:
            self.data.serialStatus = False
            self.data.serial = "Disconnected"
            try:
                self.init_serial()
            except Exception as e:
                pass
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
            self.data.hdo = 0
            return

        self.data.serial = "Connected"
        self.data.serialStatus = True
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

        time.sleep(0.5)
        reg = 4000
        length = 10
        try:
            readRegs = self.modbusClient.read_regs(reg, length)
            self.serial.write(readRegs)
            receiveData = self.serial.read(5+(2*length))
            receiveData = self.modbusClient.mbrtu_data_processing(receiveData)
            
            self.data.hdo = receiveData[9]
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
            print(e)

    

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
        self.hdo = 0