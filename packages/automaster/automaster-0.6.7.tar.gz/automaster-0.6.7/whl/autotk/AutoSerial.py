import serial
import serial.tools.list_ports
import time
from autotk.AutoCoreLite import logger


def get_com_device(filter_id=[]):
    '''
    :param <IR模块>"VID_1A86&PID_7523"<电压模块>"VID_067B&PID_2303"<SCAN扫描枪>"VID_E851&PID_1002"
    :return:
    '''
    com_ports = serial.tools.list_ports.comports()
    com_dict = {}
    port_dict = {}
    name_list = []
    for port in com_ports:
        if (port.vid):
            vid = "%04X" % port.vid
            pid = "%04X" % port.pid
            vid_pid = "VID_%s&PID_%s" % (vid, pid)
            name = port.name
            if (filter_id):
                if (vid_pid in filter_id):
                    name_list.append(name)
                    com_dict[vid_pid] = name
                    port_dict[vid_pid] = port
            else:
                com_dict[vid_pid] = name
                port_dict[vid_pid] = port
    return com_dict, port_dict, name_list


class scan_com():
    def __init__(self, Port, BaudRate: str = "9600", TimeOut=10):
        self.defaultport = Port
        self.ports = []
        self.baudrate = BaudRate
        self.timeout = TimeOut
        self.scan_dute = 0.2
        self.scan_count = int(self.timeout / self.scan_dute)
        self.ser = None
        self.err = False
        self.history = ''

    def open(self, Port=None):
        try:
            if Port == None:
                Port = self.defaultport
            self.ser = serial.Serial()
            self.ser.port = Port
            self.ser.baudrate = self.baudrate
            self.ser.timeout = self.scan_dute
            # self.ser.terminator ='\r'
            self.ser.open()
            # logger.info('打开端口%s' % Port)
        except Exception as e:
            logger.critical(e)
            self.err = True
            self.ser = None
        return self.ser

    def cls(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except:
            pass

    def scan_port(self):
        port_names = []
        port_list = list(serial.tools.list_ports.comports())
        for i in port_list:
            port_list_list = list(i)
            port_names.append(port_list_list[0])
        self.ports = sorted(port_names)
        return self.ports

    def scan_loop(self, timeout=None):
        if (timeout):
            self.scan_count = int(timeout / self.scan_dute)
        for i in range(self.scan_count):
            ret_ls = self.ser.readlines()
            # print(ret_ls)
            if (ret_ls):
                self.history = ret_ls[-1]
                return True, self.history
        return False, ""

    def scan(self, timeout=None):
        if (timeout == -1):
            ret = False
            while not ret:
                ret, value = self.scan(10)
                if (ret):
                    logger.info(value)
                    break
            return value
        else:
            if (self.ser):
                try:
                    return self.scan_loop(timeout)
                except Exception as e:
                    try:
                        self.open()
                        return False, ""
                    except:
                        self.err = True
            else:
                try:
                    self.open()
                    return False, ""
                except:
                    self.err = True

    def send(self, msg):
        self.ser.write(msg)

    def trig_recv(self):
        trig = b"\x57\x00\x18\x00\x55\x00"
        trig_end = b"\x57\x00\x19\x00\x55\x00"
        self.ser.write(trig)
        time.sleep(0.2)
        ret = self.ser.readlines()
        result = b""
        if (ret):
            allret = b"".join(ret)
            respond = b"\x31\x00\x00\x00\x55\x00"
            if (respond in allret):
                result = allret[len(respond):]
        self.ser.write(trig_end)
        self.ser.readlines()
        return result.decode().strip()

    def close(self):
        try:
            self.ser.close()
        except:
            pass


class control_com():
    def __init__(self, Port, BaudRate: str = "9600", TimeOut=5):
        self.defaultport = Port
        self.ports = []
        self.baudrate = BaudRate
        self.timeout = TimeOut
        self.scan_dute = 0.2
        self.scan_count = int(self.timeout / self.scan_dute)
        self.ser = None
        self.err = False
        self.history = ''

    def open(self, Port=None):
        try:
            if Port == None:
                Port = self.defaultport
            self.ser = serial.Serial()
            self.ser.port = Port
            self.ser.baudrate = self.baudrate
            self.ser.timeout = self.scan_dute
            # self.ser.terminator ='\r'
            self.ser.open()
            # logger.info('打开端口%s' % Port)
        except Exception as e:
            logger.critical(e)
            self.err = True
            self.ser = None
        return self.ser

    def sendrecv(self, msg):
        self.ser.write(msg)
        time.sleep(0.05)
        return self.ser.readline()

    def click(self, dute=1):
        out1 = self.sendrecv(b"BUTTON_ON\r\n")
        # logger.debug("[Button]ON %s"%out1)
        time.sleep(dute)
        out2 = self.sendrecv(b"BUTTON_OFF\r\n")
        # logger.debug("[Button]OFF %s" % out2)
        result = b'OK' in out1 and b'OK' in out2
        # print("[Button]ON %s OFF %s Click %s"%(out1,out2,result))
        logger.debug("[Button]ON %s OFF %s Click %s" % (out1, out2, result))
        return result

    def cls(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except:
            pass

    def close(self):
        try:
            self.ser.close()
        except:
            pass


class ir_com():
    def __init__(self, Port, BaudRate: str = "9600", TimeOut=5):
        self.defaultport = Port
        self.ports = []
        self.baudrate = BaudRate
        self.timeout = TimeOut
        self.scan_dute = 0.2
        self.scan_count = int(self.timeout / self.scan_dute)
        self.ser = None
        self.err = False
        self.history = ''
        self.keycode = {"7": b"\x01\xFE\x1E\xE1", "8": b"\x01\xFE\x13\xEC", "9": b"\x01\xFE\x12\xED",
                        "10": b"\x01\xFE\x10\xEF",
                        "11": b"\x01\xFE\x17\xE8", "12": b"\x01\xFE\x16\xE9", "13": b"\x01\xFE\x14\xEB",
                        "14": b"\x01\xFE\x1B\xE4",
                        "15": b"\x01\xFE\x1A\xE5", "16": b"\x01\xFE\x18\xE7"}
        self.keyname = {"0": b"\x01\xFE\x1E\xE1", "1": b"\x01\xFE\x13EC", "2": b"\x01\xFE\x12\xED",
                        "3": b"\x01\xFE\x10\xEF",
                        "4": b"\x01\xFE\x17\xE8", "5": b"\x01\xFE\x16\xE9", "6": b"\x01\xFE\x14\xEB",
                        "7": b"\x01\xFE\x1B\xE4",
                        "8": b"\x01\xFE\x1A\xE5", "9": b"\x01\xFE\x18\xE7", "ok": b"\x01\xFE\x55\xAA",
                        "left": b"\x01\xFE\x54\xAB",
                        "rigth": b"\x01\xFE\x15\xEA", "return": b"\x01\xFE\x19\xE6", "up": b"\x01\xFE\x59\xA6",
                        "down": b"\x01\xFE\x51\xAE"}

    def check(self, cmd=b'\xFF\x10\xF0\x00\x00\x06\x0C\x00\x01\x00\x03\x00\x00\x00\x01\x00\x01\x00\x00\x2B\x14'):
        # FF 10 F0 00 00 06 0C 00 01 00 03 00 00 00 01 00 01 00 00 2B 14
        self.ser.write(cmd)
        time.sleep(0.5)
        ret = self.ser.readline()
        judge = ret in [b'\x01\x10\xF0\x00\x00\x06\x73\x0B']
        return judge

    def open(self, Port=None):
        try:
            if Port == None:
                Port = self.defaultport
            self.ser = serial.Serial()
            self.ser.port = Port
            self.ser.baudrate = self.baudrate
            self.ser.timeout = self.scan_dute
            # self.ser.terminator ='\r'
            self.ser.open()
            # logger.info('打开端口%s' % Port)
        except Exception as e:
            logger.critical(e)
            self.err = True
            self.ser = None
        return self.ser

    def recv(self):
        return self.ser.readline()

    def send(self, cmdbyte):
        self.ser.write(cmdbyte)

    def sendkey(self, code: str = None, name: str = None):
        if (code == None):
            cmd = self.keyname[name]
        else:
            cmd = self.keycode[code]
        self.ser.write(cmd)

    def cls(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except:
            pass

    def close(self):
        try:
            self.ser.close()
        except:
            pass


class volt_com():
    def __init__(self, Port, BaudRate: str = "57600", TimeOut=5):
        self.defaultport = Port
        self.ports = []
        self.baudrate = BaudRate
        self.timeout = TimeOut
        self.scan_dute = 0.2
        self.scan_count = int(self.timeout / self.scan_dute)
        self.ser = None
        self.err = False
        self.history = ''

    def open(self, Port=None):
        try:
            if Port == None:
                Port = self.defaultport
            self.ser = serial.Serial()
            self.ser.port = Port
            self.ser.baudrate = self.baudrate
            self.ser.timeout = self.scan_dute
            # self.ser.terminator ='\r'
            self.ser.open()
            # logger.info('打开端口%s' % Port)
        except Exception as e:
            logger.critical(e)
            self.err = True
            self.ser = None
        return self.ser

    def cls(self):
        try:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except:
            pass

    def scan_port(self):
        port_names = []
        port_list = list(serial.tools.list_ports.comports())
        for i in port_list:
            port_list_list = list(i)
            port_names.append(port_list_list[0])
        self.ports = sorted(port_names)
        return self.ports

    def sendrecv(self, msg):
        self.ser.write(msg)
        time.sleep(0.05)
        return self.ser.readline()

    def getVolt_H(self):
        return self.getVolt("H")

    def getVolt_D(self):
        return self.getVolt("D")

    def getVolt(self, cmd="H"):
        try:
            for i in range(3):
                ret = self.sendrecv(cmd.encode())
                out = ret.decode()
                pattern = re.compile(r"\S*V_(\S*)")  # 长度10以上
                list = pattern.findall(out)
                # print(out,list)
                if (list):
                    return float(list[0])
            return None
        except Exception as e:
            logger.critical(e)
            return None

    def getK(self, cmd="K"):
        try:
            for i in range(3):
                ret = self.sendrecv(cmd.encode())
                out = ret.decode()
                # print(out)
                if (cmd in out):
                    return "_P" in out
            return None
        except Exception as e:
            logger.critical(e)
            return None

    def getC(self, cmd="C"):
        try:
            for i in range(3):
                ret = self.sendrecv(cmd.encode())
                out = ret.decode()
                print(out)
                if (cmd in out):
                    return "_P" in out
            return None
        except Exception as e:
            logger.critical(e)
            return None

    def getNo(self, cmd="G"):
        try:
            for i in range(3):
                ret = self.sendrecv(cmd.encode())
                out = ret.decode()
                pattern = re.compile(r"\S*S_(\S*)")  # 长度10以上
                list = pattern.findall(out)
                if (list):
                    return list[0]
            return None
        except Exception as e:
            logger.critical(e)
            return None

    def setNo(self, sn):
        cmd = "S%s" % sn
        try:
            for i in range(3):
                ret = self.sendrecv(cmd.encode())
                out = ret.decode()
                # print(out)
                return "S_P" in out
            return None
        except Exception as e:
            logger.critical(e)
            return None

    def close(self):
        try:
            self.ser.close()
        except:
            pass
