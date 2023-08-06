import numpy as np
import win32event
import win32api
import win32com.client
from scipy import signal
from scipy.io import wavfile
import sounddevice
import pyloudnorm as pyln
import pywintypes
from win32com.directsound import directsound
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from autotk.AutoCoreLite import *

# def _sound_rec(devname, rec_len, wavepath="./record.wav", RATE=44100):
#     # rec_id = self.get_rec_id(devname)
#     try:
#         rec_id = self.dev_class.get_rec_id(devname)
#         if (rec_id):
#             sounddevice.default.device[0] = rec_id
#             time.sleep(0.5)
#             rec_narray = sounddevice.rec(int(rec_len * RATE), samplerate=RATE, channels=1)
#             sounddevice.wait()  # Wait until recording is finished
#             return RATE, rec_narray, rec_narray
#         else:
#             logger.critical("Not Found Record Device[%s]" % devname)
#             return False, None, None
#     except:
#         return False, None, None
# def sound_device_query(self):
#         # 使用sounddevice 获取电脑连接的声卡以及系统自带的所有音频驱动信息(驱动, 声道名, id)
#         audio_drivers_and_channels_msg_dict = {}
#         audio_input_channels_msg_dict = {}
#         audio_output_channels_msg_dict = {}
#         this_tmp_dict = {}
#         host_api_tuple = sounddevice.query_hostapis()
#
#         for temp_dict in host_api_tuple:
#             this_tmp_dict[temp_dict["name"]] = temp_dict["devices"]
#
#         channels_list = sounddevice.query_devices()
#         for driver_name in this_tmp_dict:
#             audio_drivers_and_channels_msg_dict[driver_name] = []
#             audio_input_channels_msg_dict[driver_name] = []
#             audio_output_channels_msg_dict[driver_name] = []
#
#             for id in this_tmp_dict[driver_name]:
#                 audio_drivers_and_channels_msg_dict[driver_name].append((id, channels_list[id]["name"]))
#
#                 if channels_list[id]["max_input_channels"] > 0:
#                     audio_input_channels_msg_dict[driver_name].append((id, channels_list[id]['name']))
#
#                 if channels_list[id]["max_output_channels"] > 0:
#                     audio_output_channels_msg_dict[driver_name].append((id, channels_list[id]['name']))
#         self.rec_list = audio_input_channels_msg_dict
#         return audio_drivers_and_channels_msg_dict, audio_input_channels_msg_dict, audio_output_channels_msg_dict
class Sound_Man():
    def __init__(self,IID,Rec_Len,RATE=44100):
        self.iid=IID
        self.reclen=Rec_Len
        self.bps=16
        self.channel=1
        self.rate=RATE

    def sound_rec(self):
        try:
            dsc = directsound.DirectSoundCaptureCreate(self.iid, None)  # 创建设备对象
            cdesc = directsound.DSCBUFFERDESC()  # 创建DSCBUFFERDESC结构对象
            bSize = int(self.rate * self.channel * self.bps / 8 * self.reclen)
            cdesc.dwBufferBytes = bSize  # 缓存大小
            cdesc.lpwfxFormat = pywintypes.WAVEFORMATEX()  # DirectSound数据块格式
            cdesc.lpwfxFormat.wFormatTag = pywintypes.WAVE_FORMAT_PCM
            cdesc.lpwfxFormat.nChannels = self.channel
            cdesc.lpwfxFormat.nSamplesPerSec = self.rate
            cdesc.lpwfxFormat.nAvgBytesPerSec = int(self.rate * self.channel * self.bps / 8)
            cdesc.lpwfxFormat.nBlockAlign = int(self.channel * self.bps / 8)
            cdesc.lpwfxFormat.wBitsPerSample = self.bps
            buffer = dsc.CreateCaptureBuffer(cdesc)  # 创建缓冲区对象
            event = win32event.CreateEvent(None, 0, 0, None)
            Notify = buffer.QueryInterface(directsound.IID_IDirectSoundNotify)  # 创建事件通知接口
            Notify.SetNotificationPositions((directsound.DSBPN_OFFSETSTOP, event))
            buffer.Start(0)  # 定长录音
            win32event.WaitForSingleObject(event, int(self.reclen) * 1500)
            event.Close()
            self.recbuffer = buffer.Update(0, bSize)
            _sound_np = np.frombuffer(self.recbuffer, np.dtype('<i2'))  # PCM数据格式为int16
            # _sound_np = _sound_np[::2] # 多通道数据等步长分离
            # _sound_np = _sound_np[1::2] # 多通道数据等步长分离
            # _sound_np.tobytes()   # ndarray可重新转换成bytes
            self.recdata = (_sound_np / 32767).astype(np.float)  # 格式转换int16转float
            return True
        except Exception as e:
            logger.critical("Record Device[%s] Error" % self.iid)
            logger.critical(e)
            return False
    def save_wavefile(self,wavepath):
        wavfile.write(wavepath, self.rate, self.recdata)
        # logger.debug("[Wavfile]%s"%wavepath)
    def get_max(self,set_round=4):
        # vmax = round(np.max(data[:, 0]), 4)  # 多通道,需同步更新sound_rec
        return round(np.max(self.recdata), set_round)
    def get_loudness(self):
        meter = pyln.Meter(self.rate)
        loudness = meter.integrated_loudness(self.recdata)
        return loudness
    def get_psd(self,data):
        return signal.periodogram(data, self.rate)  # Frequencies and PSD
    def check_powerlimit(self,data,powerlimit,frq_min,frq_max):
        f, P = self.get_psd(data)
        dlimit = powerlimit * 1e+16 * P[0]  # 动态调节limit可兼容不同的录音设备
        P_max = np.max(P)
        idx = signal.find_peaks(P, height=dlimit, distance=2)[0]
        logger.debug("Dynamic:%g Max:%g Peak:%s f:%s" % (dlimit, P_max, P[idx], f[idx]))
        result = bool(len(idx))
        for i in idx:
            if (P_max == P[i]):  # 仅判断最大的Peak是否在规定频率
                result = frq_min < f[i] < frq_max
                break
            else:
                result = False
        return result,f,P
    def check_wave(self,powerlimit1=1e+7, judge1=[1000], powerlimit2=1e+7, judge2=[1000], judge_offset=2):
        _info = {}   # 待完善 用于显示 检测结果 预留了show_plot_class 显示box类 ....................................................
        try:
            # print(self.recdata.shape)
            if (self.channel == 1):
                result = False
                for m in judge1:
                    result, f, P = self.check_powerlimit(self.recdata, powerlimit1, m - judge_offset,
                                                         m + judge_offset)
                    if (result):  # 修改为一个频率pass判为通过 20210224
                        break
                return result, _info
            else:
                result1 = False
                for m in judge1:
                    result1, f, P = self.check_powerlimit(self.recdata[:, 0], powerlimit1, m - judge_offset,
                                                          m + judge_offset)
                    if (result1):  # 修改为一个频率pass判为通过 20210224
                        break
                result2 = False
                for m in judge2:
                    result2, f2, P2 = self.check_powerlimit(self.recdata[:, 1], powerlimit2, m - judge_offset,
                                                            m + judge_offset)
                    if (result2):  # 修改为一个频率pass判为通过 20210224
                        break
                return result1 and result2, _info
        except Exception as e:
            print(e)
            logger.critical(e)
        return False,_info
class Modal_PSD_Real(tk.Toplevel):
    def __init__(self, parent, title, data, reclist):
        if (type(data) == type(None)):
            mbox.showinfo("None Data")
            return
        tk.Toplevel.__init__(self, parent, width=400, height=600)
        parent.master.wm_attributes('-topmost', 0)
        # self.geometry("300x280+%d+%d" % (parent.winfo_rootx() + 30, parent.winfo_rooty() + 30))
        self.title(title)
        self.resizable(height=False, width=False)
        self.grab_set()
        self.rec_list = data
        self.rec_names = reclist
        self.recname = self.rec_names[0]
        self.initplt(data)

    def initplt(self, data, showbar=True):

        ctlframe = tk.Frame(self)
        ctlframe.pack(side="top")
        tk.Label(ctlframe, text="录音设备").pack(side="left")
        self.comvalue = tk.StringVar()  # 窗体自带的文本，新建一个值
        comboxlist = ttk.Combobox(ctlframe, textvariable=self.comvalue, state="readonly")  # 初始化
        comboxlist["values"] = self.rec_names
        comboxlist.current(0)  # 选择第一个
        self.recid = self.get_rec_id(self.recname)
        comboxlist.bind("<<ComboboxSelected>>", self.switch)  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        comboxlist.pack(side="left")
        tk.Label(ctlframe, text="采集时长").pack(side="left")
        value = tk.IntVar()
        self.reclen = 1
        value.set(self.reclen)
        testCMD = self.register(self.change)
        tk.Entry(ctlframe, text=value, relief="flat", validate="key", validatecommand=(testCMD, "%P")).pack(side="left")
        tk.Label(ctlframe, text="阈值").pack(side="left")
        value = tk.IntVar()
        self.Peaklimit = 6e-1
        value.set(self.Peaklimit)
        testCMD2 = self.register(self.change2)
        tk.Entry(ctlframe, text=value, relief="flat", validate="key", validatecommand=(testCMD2, "%P")).pack(
            side="left")
        frame = tk.Frame(self)
        frame.pack()
        fig, self.axe = plt.subplots()
        self.axe.set_xlim([0, 22000])
        self.axe.set_ylim([1e-11, 1e4])
        self.axe.set_yscale('log')
        self.axe.set_xlabel(r'Frequency, $\nu$ $[\mathrm{Hz}]$')
        self.axe.set_ylabel(r'PSD, $P$ $[\mathrm{AU^2Hz}^{-1}]$')
        self.axe.grid(which='both')
        self.axe.set_title('Periodogram %s (%s seconds)' % (self.recname, self.reclen))
        self.lna, = self.axe.plot([], [])
        self.lna2, = self.axe.plot([], [])
        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        if (showbar):
            toolbar = NavigationToolbar2Tk(self.canvas, frame)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.loop()

    def get_rec_id(self, tagname):
        return self.rec_list[self.rec_names.index(tagname)]
        # if ("Windows DirectSound" in self.rec_list):
        #     input_list = self.rec_list["Windows DirectSound"]
        # else:
        #     input_list = self.rec_list[0]
        # for i, n in input_list:
        #     if tagname in n:
        #         return i
        # return False

    def change2(self, P, *args):
        if (P):
            try:
                f = float(P)
                self.Peaklimit = f
            except:
                pass
        return True

    def change(self, P, *args):
        if (P):
            try:
                f = float(P)
                if (5 > f > 0.02):
                    self.reclen = f
            except:
                pass
        return True

    def switch(self, *args):
        self.recname = self.comvalue.get()
        self.recid = self.get_rec_id(self.recname)



    def loop(self):
        sound_class = Sound_Man(self.recid, self.reclen)
        result = sound_class.sound_rec()
        sounddevice.wait()
        if result:
            try:
                loudness = sound_class.get_loudness()
            except:
                loudness = float("inf")
            # Amax = np.max(rec_narray[:, 0])
            Amax = sound_class.get_max()
            # f, P = signal.periodogram(rec_narray[:, 0], fs)
            f, P = sound_class.get_psd(sound_class.recdata)
            # print(P)
            p_max = np.max(P)
            self.axe.set_title(
                '%s\n Periodogram Max:%.0g(%ss) Amax:%.3f Loudness:%.2f' % (self.recid, p_max, self.reclen, Amax, loudness))
            self.lna.set_xdata(f)
            self.lna.set_ydata(P)
            self.lna2.set_xdata([0, np.max(f)])
            self.lna2.set_ydata(self.Peaklimit)
            self.canvas.draw()
            # self.canvas.draw_idle()
            p_max = np.max(P)
            if (self.Peaklimit < p_max):
                idx = signal.find_peaks(P, height=self.Peaklimit, distance=2)[0]
                foundlen = len(idx)
                self.axe.set_xlabel(r'Frequency, $\nu$ $[\mathrm{Hz}]$' + " Peak(%s)" % foundlen)
                if (foundlen < 20):
                    if (foundlen < 10):
                        self.axe.set_xlabel(r'Frequency, $\nu$ $[\mathrm{Hz}]$' + " Peak(%s) " % foundlen + str(f[idx]))
                    logger.debug("PSD_Peak:%d %s" % (foundlen, f[idx]))
        self.after(200, self.loop)