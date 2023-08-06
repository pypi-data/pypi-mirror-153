# YICHIP 仪器控制

UPDATE:
- 2022-02-17：第三次更新,修改示波器获取电压函数,现在更加精准
- 2022-02-17：第二次更新,新增RIGOL DP832A三通道直流电源驱动
- 2022-01-29：第一次更新,初始代码可对示波器(ZDS1104,ZDS2014),电源(AgilentE3649A,Agilent66319D),台式万用表(Agilent34410A)

## YC-PYVISA介绍

VISA，虚拟仪器软件架构，是对带有GPIB、VXI、PXI、串口(RS232/485)、以太网、USB和/或IEEE 1394接口的仪器系统进行配置、编程和故障排除的标准。简单的说就是两个人沟通，类似于语言的中介，VISA将你的语言转换变成仪器能听懂的命令.

PyVisa是通过上述接口用来控制各种各样的测量仪器的Python包.

本项目对YICHIP使用的部分仪器通过PyVisa进行了二次封装,以达到更方便的控制仪器,进行自动化测试的目的

## 安装

Using pip:

```cmd
pip3 install yc-pyvisa
```

## 物理接口

前面说到visa是对带有GPIB、VXI、PXI、串口(RS232/485)、以太网、USB和/或IEEE 1394接口的仪器系统进行配置、编程和故障排除的标准,所以针对不同的接口,需要安装不同的驱动,不能直接安装使用.以下任意一个接口连接到电脑,且安装好驱动,都可直接被pyvisa控制.

### GPIB接口

比较通用的是GPIB接口,大概长这样
<center>
    <img src="https://qzxx.com/wp-content/uploads/2017/11/788e43dadc14671.jpg" width="400">
    <center>GPIB控制器</center>
</center>
<center>
    <img src="https://media.rs-online.com/t_large/F7600341-01.jpg" width="400">
    <center>GPIB接口</center>
</center>

注意:一个GPIB控制器可以控制多个GPIB设备,通过以下线材可拓展多个接口

<center>
    <img src="https://gss0.baidu.com/9fo3dSag_xI4khGko9WTAnF6hhy/zhidao/wh%3D600%2C800/sign=40cb661ad93f8794d3aa4028e22b22cc/a6efce1b9d16fdfa7ddf434cb98f8c5495ee7be5.jpg" width="400">
</center>

### USB接口

USB接口应该比较方便辨认,通常是type-B(2.0)接口,就我们平时电脑连接Jlink的线材,我就不贴图片了

一般情况下USB设备的驱动都可以在对应的厂商的官网找到,但是个人觉得打驱动比较麻烦,所以如果仪器有GPIB接口并且你有GPIB控制器的话最好直接用GPIB去连接仪器,不过我发现我们公司的示波器都没有GPIB接口,而且我目前控制的ZLG的示波器,按照官网提供的方法是没有办法在Win10上安装驱动的,所以后面我会提供一篇教程,专门用于ZLG示波器的驱动安装

### RS-232接口

用串口来进行收发指令和数据,这也是我比较推荐的一种方式,毕竟打串口驱动是一件相对容易的事情,只需要一根RS-232的线就好了,大概长这样
<center>
    <img src="https://image-c.ehsy.com/uploadfile/opc/img/2018/09/10/20180910142455231.jpg" width="400">
    <center>RS-232</center>
</center>

### 网口

关于网口直接连接就行,一般仪器里面都可以直接设置,具体需要大家自己翻手册.

## 驱动安装

必要安装:下载[NI VISA](https://www.ni.com/zh-cn/support/downloads/drivers/download.ni-visa.html#442805),完成后直接一直下一步安装即可,里面集成了GPIB的控制器驱动,并可为部分仪器提供USB驱动,同时为pyvisa提供后端支持

Agilent_34410A台式万用表USB驱动:

由于安装文件巨大,所以这里不提供该驱动,在内网进行下载:\\192.168.2.16\public\xubo\Agilent 34410A Driver.zip

- 安装IntruiLinkApp，安装文件路径：CD1\IntuiLinkApp\Setup.exe
- 安装IOLib，安装文件路径：CD2\Autorun\auto.exe
- 安装IVI_COM，安装文件路径：CD1\ivi-com\Agilent34410.1.0.18.0.msi
- 安装完后重启电脑即可通过USB控制台式万用表

ZLG示波器驱动USB驱动安装:

目前只提供ZDS1104 和 ZDS2014 usb驱动文件,由于该驱动是通过`NI-VISA DRIVER WIZARD`生成,未经过签名,所以win10是不允许安装的,需要[禁用驱动程序强制签名](https://iknow.lenovo.com.cn/detail/dc_132524.html),然后双击安装文件即可

串口驱动安装:

RS232的线在公司是比较稀少的，里面的串口芯片是比较老的存在，直接插上win10 是不识别的，这个时候进驱动管理器会发现驱动已经安装，但是不能使用，这个时候只需要发动万能的BING就可以了[PL2303win10驱动安装教程](https://blog.csdn.net/wtf3505/article/details/104138727)，安装完之后就可以愉快的使用串口对仪器进行控制了，但是需要注意的是，串口仪器是不能直接使用的因为串口涉及到波特率的问题，所以我们还是需要设置一下波特率，一般仪器支持串口控制，波特率是可以修改的，如果无法找到就去官网下载手册看看哪里有问题。具体设置波特率的代码我已经在ZLG2014上进行体现了,如果你们用其他仪器的话，就复制粘贴这句话到它的对象初始化函数里面去，去设置对应的波特率就好了

```python
self.instr.baud_rate = 115200
```

网口:

网口是不需要安装驱动的,只需要该电脑和设备处于同一网段即可(注意 ZLG系列的示波器LAN控制不稳定,不建议使用)

## 代码控制

在上面安装完模块过后直接导入本模块

```python
from yc-pyvisa import *
```

然后初始化对应的仪器,里面有默认的对应设备的仪器地址,若地址有变动在初始化的时候填入地址参数就好

```python
oscilloscope = ZLG1104()#示波器
oscilloscope2 = ZLG2014()#示波器
multimeter  = Agilent_34410A()#台式万用表
power = Agilent_66319d()#电源
power2 = AgilentE3649A()#电源
```

GPIB的地址需要通过仪器自己去设置,也可通过在上面安装完 NI VISA之后出现的一个配置管理软件(`NI MAX`),遍历对应的设别地址，也可通过代码去遍历对应的设备地址。

``` python
rm = visa.ResourceManager()
new = rm.list_resources()#返回一个数组，里面包含了所有的地址
```

但是在我实践下来发现通过代码ZLG的示波器是不能够遍历到他的USB地址的，所以这个时候你只能通过`NI MAX`去遍历它的地址，同时ZLG示波器的USB地址都是完全一样的且无法更改，所以当你需要同时控制两台以上的示波器的时候，只能通过1个USB+n个串口去控制示波器。

后面控制仪器就用对应的函数控制就好,比如:

```python
fre = oscilloscope.Get_Frequency(1)
```

就能够获取到对应示波器通道1的输入频率

## 进阶

如果我提供的库里面的函数无法满足需求，也不必担心，示波器的功能很多，由于时间原因只实现了目前用得到的一些函数和功能，可以通过去官网下载对应的手册，（同时这里也会提供一些我下载到的手册，在同目录下）去查找它对应的某些功能的SCIP指令，然后整理成函数就好。当然如果能通过gitee 提交上来就更好了，我会把每一次正确提交都发布上去，供大家使用，当然希望大家能够对自己提交的每一个对象（仪器），函数都写好注释，方便大家理解其功能（虽然第一版有很多函数都没写注释。。。，但是后面有时间会改的）

## 完整样例代码

下面是YC3122的应急筛片程序提供一个样例

```python
from ast import While
from distutils import extension
from email import charset
import os
import glob
from pickle import FALSE, NONE, TRUE
from time import sleep
import sys
from webbrowser import get
from yc_pyvisa import *
import openpyxl
import threading
from logger import *
max_val = 0
otp_buff = []
def get_cmd_result(cmd):
    result = os.popen(cmd)
    res = result.read()
    return res
def e_p():
    while('CPU Stopped' not in get_cmd_result("e p")):
        continue
    return
def e_c():
    while('CPU Running' not in get_cmd_result("e c")):
        continue
    return
def file_name(file_name):
    global max_val
    file_txt = glob.glob(file_name)
    if(file_txt == []):
        max_val = 0x100
        return
    for filename in file_txt:
        try:
            str1 = str(os.path.basename(filename))
            str1 = str1.replace('.txt',"").replace("id","")
            str1 = int(str1,16)
            if(max_val < str1):
                max_val = str1
        except Exception as e:
            print(e)
            pass
    max_val += 1
def count_bits_2(value):
    count = 0
    while(value):
        value &= value - 1
        count += 1
    return count
def auto_set_fre():
    get_cmd_result("e 20004 0155")
    sleep(0.2)
    get_cmd_result("e 20000 02")
    sleep(1)
    if("01" not in get_cmd_result("e 20001")):
        return FALSE
    fre1 = oscilloscope.Get_Frequency()
    print(fre1)
    get_cmd_result("e 20004 0165")
    get_cmd_result("e 20000 02")
    sleep(0.2)
    if("01" not in get_cmd_result("e 20001")):
        return FALSE
    fre2 = oscilloscope.Get_Frequency()
    print(fre2)
    fer = int((fre2-fre1)/16)
    result = int(0x155 + (24000000 - fre1)/fer)
    get_cmd_result("e 20004 " + hex(result).replace("0x",""))
    get_cmd_result("e 20000 02")
    sleep(0.2)
    if("01" not in get_cmd_result("e 20001")):
        return FALSE
    fre3 = oscilloscope.Get_Frequency()
    print(fre3)
    if(fre3 <24050000 and fre3 >23950000):
        return result
    while(fre3 >24050000):
        result-=1
        get_cmd_result("e 20004 " + hex(result-30).replace("0x",""))
        get_cmd_result("e 20000 02")
        sleep(0.2)
        if("01" not in get_cmd_result("e 20001")):
            return FALSE
        fre3 = oscilloscope.Get_Frequency()
        if(fre3 <24050000 and fre3 >23950000):
            return result
    while(fre3 < 23950000):
        result+=1
        get_cmd_result("e 20004 " + hex(result).replace("0x",""))
        get_cmd_result("e 20000 02")
        sleep(0.2)
        if("01" not in get_cmd_result("e 20001")):
            return FALSE
        fre3 = oscilloscope.Get_Frequency()
        if(fre3 <24050000 and fre3 >23950000):
            return result
    return result
    # power.setVoltage(5,2)
    # set_rc192_val(0x5c)
    # power.setVoltage(0,2)
    # sleep(0.1)
    # power.setVoltage(5,2)
    # fre1 = oscilloscope.Get_Frequency()
    # print(fre1)
    # set_rc192_val(0x65)
    # power.setVoltage(0,2)
    # sleep(0.1)
    # power.setVoltage(5,2)
    # fre2 = oscilloscope.Get_Frequency()
    # print(fre2)
    # fer = int((fre2-fre1)/16)
    # result = int(0x55 + (24000000 - fre1)/fer)
    # set_rc192_val(result)
    # fre3 = oscilloscope.Get_Frequency()
    # power.setVoltage(0,2)
    # sleep(0.1)
    # power.setVoltage(5,2)
    # print(fre3)
    # if(fre3 <24050000 and fre3 >23950000):
    #     return result
    # while(fre3 >24050000):
    #     result-=1
    #     set_rc192_val(result)
    #     fre3 = oscilloscope.Get_Frequency()
    #     power.setVoltage(0,2)
    #     sleep(0.1)
    #     power.setVoltage(5,2)
    #     if(fre3 <24050000 and fre3 >23950000):
    #         return result
    # while(fre3 < 23950000):
    #     result+=1
    #     set_rc192_val(result)
    #     fre3 = oscilloscope.Get_Frequency()
    #     power.setVoltage(0,2)
    #     sleep(0.1)
    #     power.setVoltage(5,2)
    #     if(fre3 <24050000 and fre3 >23950000):
    #         return result
    # return result
def set_rc192_val(input_val):
    while(True):
        if('CPU Stopped' in get_cmd_result("e p")):
            get_cmd_result("e f0c18 00000000")
            get_cmd_result("e f0c1c 00000000")
            get_cmd_result("e f0c49 30")
            get_cmd_result("e f8703 10")
            get_cmd_result("e faaa0 55")
            get_cmd_result("e faaa0 aa")
            get_cmd_result("e faaa0 17")
            get_cmd_result("e faaa4 01")
            get_cmd_result("e fa802 " + hex(input_val).replace("0x",""))
            print("input_val = %x"%input_val)
            break

def down_otp(cmd):
    get_cmd_result("e 20000 "+ cmd)
    sleep(0.1)
    while("01" not in get_cmd_result("e 20001")):
        continue
    # while(True):
    #     if('CPU Stopped' in get_cmd_result("e p")):
    #         get_cmd_result("e f853c 88")
    #         if('f8530 :                                     88'in get_cmd_result("e f853c")):
    #             get_cmd_result("e r pc c0")
    #             if('read cm0 reg f = c0\n'in get_cmd_result("e r pc")):
    #                 get_cmd_result("e otw 12c " + hex(input_val).replace("0x",""))
    #                 if(count_bits_2(input_val) % 2 == 1):
    #                     get_cmd_result("e otw 12d 81")
    #                 elif(count_bits_2(input_val) % 2 == 0):
    #                     get_cmd_result("e otw 12d c1")
    #                 break
    return
def RC192_test():
    cail_val = auto_set_fre()
    if(cail_val == None):
        error("RC192 cail_val ERROR " + str(cail_val))
    print(cail_val)
    otp_buff.append(hex(cail_val))
    down_otp("03")

def down_ft_code():
    e_p()
    os.system("tool\d.bat")

def osc_32k_cal():
    get_cmd_result("e 20000 04")
    sleep(0.1)
    if("01" not in get_cmd_result("e 20001")):
        return False
    oscilloscope.Set_Timebase("10us")
    osc32k_cail_val = oscilloscope.Get_Frequency()
    oscilloscope.Set_Timebase("100us")
    oscilloscope.write(":CHANnel1:DISPlay OFF")
    print(osc32k_cail_val)
    otp_buff.append((hex)(osc32k_cail_val))
    get_cmd_result("e 20004 " + to_hex(osc32k_cail_val))
    down_otp("05")
    return osc32k_cail_val
def DVDD_test():
    DVDD_V = oscilloscope.Get_Vol(2)
    if(DVDD_V>1.3 or DVDD_V<1.15):
        error("DVDD_V ERROR "+str(DVDD_V))
def ft_test_init():
    power.setVoltage(0,2)
    sleep(1)
    CURR_VUBT = multimeter.Read_Curr()
    if(CURR_VUBT<1e-06 or CURR_VUBT>3e-06):
        error("VBUT ERROR"+ str(CURR_VUBT))
    power.setVoltage(5,2)
    power.setVoltage(3.3,1)
    DVDD_test()
    bist_test()
    down_ft_code()
    sleep(0.6)

def xw_toExcel(data,excelname):  # xlsxwriter库储存数据到excel
    try:
        workbook = openpyxl.load_workbook(excelname)  # 打开工作簿
        worksheet1 = workbook.active  # 创建子表
    except Exception as a:
        print(a)
        workbook = openpyxl.Workbook(excelname)
        workbook.save(filename= excelname)  # 关闭表
        workbook.close()
        workbook = openpyxl.load_workbook(excelname)  # 打开工作簿
        worksheet1 = workbook.active
    rows = worksheet1.max_row
    j = 0
    for i in data:
        j+=1
        worksheet1.cell(row=rows+1,column = j).value = i
    workbook.save(filename= excelname)  # 关闭表
    workbook.close()
def Creat_Thread(thread,*args1):
    thread_uart_read=threading.Thread(target=thread,args=args1)
    thread_uart_read.setDaemon(True)
    thread_uart_read.start()
def Check_CurrThread():
    while True:
        CURR_CHARG_IN = power.Get_Curr(2)
        if(CURR_CHARG_IN > 0.02):
            error("CURR_CHARG_IN ERROR " + str(CURR_CHARG_IN))
        sleep(1)
def read_id_txt(max_val):
    with open(".\AB_NEW_ID\id"+ hex(max_val).replace("0x","") + ".txt","r") as f:
        str = f.read().replace("\n","")
    return str
def Write_OtpBySelf():
    power.setVoltage(5,2)
    # val = int(otp_buff[6],16)
    # xor_val = 0
    # for i in range(0,4):
    #     xor_val^=val>>i&0x1
    # val|=0x80
    # val|=xor_val<<6
    # input_check = input("确认烧录otp？(y/n):")
    # if((input_check.lower() != 'y')):
    #     sys.exit()
    power.setVoltage(0,2)
    sleep(0.5)
    power.setVoltage(5,2)
    xw_toExcel(otp_buff,"3122_opt.xlsx")
    while(True):
        if('CPU Stopped' in get_cmd_result("e p")):
            get_cmd_result("e f853c 88")
            if('f8530 :                                     88'in get_cmd_result("e f853c")):
                get_cmd_result("e r pc c0")
                if('read cm0 reg f = c0\n'in get_cmd_result("e r pc")):
                    get_cmd_result("e otp .\AB_NEW_ID\id"+ hex(max_val).replace("0x","") + ".txt 2")
                    sleep(0.1)
                    get_cmd_result("e otp flash_178.txt 178")
                    sleep(0.1)
                    get_cmd_result("e otw 139 8f")
                    break
def bist_test():
    os.system(r"tool\bist.bat")
    str = get_cmd_result("e f8518l8")
    if("ff ff 03 00 00 00 00 00" not in str):
        error("bist test_error")
def gen_id():
    dir = (os.getcwd() + r"\AB_NEW_ID\*.txt")
    file_name(dir)
    str1 = "python f_gen3122id.py " + hex(max_val).replace("0x","")
    get_cmd_result(str1)
    otp_buff.append(read_id_txt(max_val))
def to_hex(val):
    return hex(val).replace("0x","")
def HvLdo_test():
    cail_val = 0x6
    get_cmd_result("e 20004 06")
    sleep(0.2)
    get_cmd_result("e 20000 0a")
    sleep(1)
    if("01" not in get_cmd_result("e 20001")):
        return FALSE
    vol = oscilloscope.Get_Vol(3)
    if(vol<=3.35 and vol >=3.25):
        return cail_val
    while(vol<=3.25):
        cail_val-=1
        get_cmd_result("e 20004 0"+ to_hex(cail_val))
        sleep(0.2)
        get_cmd_result("e 20000 0a")
        sleep(1)
        if("01" not in get_cmd_result("e 20001")):
            return FALSE
        vol = oscilloscope.Get_Vol(3)
        if(vol<=3.35 and vol >=3.25):
            return cail_val
        if(cail_val <= 0x0):
            return False
    while(vol>=3.35):
        cail_val+=1
        get_cmd_result("e 20004 0"+ to_hex(cail_val))
        sleep(0.2)
        get_cmd_result("e 20000 0a")
        sleep(1)
        if("01" not in get_cmd_result("e 20001")):
            return FALSE
        vol = oscilloscope.Get_Vol(3)
        if(vol<=3.35 and vol >=3.25):
            return cail_val
        if(cail_val >= 0xf):
            return False
    return cail_val
def Vcard_test(val):
    cail_val = 0x4
    if (val==0):
        valmax = 1.85
        valmin = 1.75
    if(val == 1):
        valmax = 3.05
        valmin = 2.95
    get_cmd_result("e 20004 010"+to_hex(cail_val)+"0"+str(val))
    sleep(0.2)
    get_cmd_result("e 20000 0e")
    sleep(1)
    if("01" not in get_cmd_result("e 20001")):
        return FALSE
    vol = oscilloscope.Get_Vol(4)
    if(vol<valmax and vol >valmin):
        return cail_val
    while(vol<valmin):
        cail_val+=1
        get_cmd_result("e 20004 010"+to_hex(cail_val)+"0"+str(val))
        sleep(0.2)
        get_cmd_result("e 20000 0e")
        sleep(1)
        if("01" not in get_cmd_result("e 20001")):
            return FALSE
        vol = oscilloscope.Get_Vol(4)
        if(vol<valmax and vol >valmin):
            return cail_val
        if(cail_val >= 0xf):
            return False
    while(vol>valmax):
        cail_val-=1
        get_cmd_result("e 20004 010"+to_hex(cail_val)+"0"+str(val))
        sleep(0.2)
        get_cmd_result("e 20000 0e")
        sleep(1)
        if("01" not in get_cmd_result("e 20001")):
            return FALSE
        vol = oscilloscope.Get_Vol(4)
        if(vol<valmax and vol >valmin):
            return cail_val
        if(cail_val <= 0):
            return False
    return cail_val
def charg_test():
    get_cmd_result("e fa820 321800")
    cail_val = 0x8
    get_cmd_result("e fa823 0"+to_hex(cail_val))
    sleep(0.2)
    vol = oscilloscope2.Get_Vol(1)
    valmax = 4.25
    valmin = 4.15
    if(vol<valmax and vol >valmin):
        return cail_val
    while(vol<valmin):
        cail_val+=1
        get_cmd_result("e fa823 0"+to_hex(cail_val))
        sleep(0.2)
        vol = oscilloscope2.Get_Vol(1)
        if(vol<valmax and vol >valmin):
            return cail_val
        if(cail_val >= 0xf):
            return False
    while(vol>valmax):
        cail_val-=1
        get_cmd_result("e fa823 0"+to_hex(cail_val))
        sleep(0.2)
        vol = oscilloscope2.Get_Vol(1)
        if(vol<valmax and vol >valmin):
            return cail_val
        if(cail_val <= 0):
            return False
    return cail_val
oscilloscope = ZLG1104()
oscilloscope2 = ZLG2014()
multimeter  = Agilent_34410A()
power = Agilent_66319d()
# zlg_2014 = ZLG1104("USB0::0x04CC::0x121C::123456789::RAW")
# os.environ['BAUD']="320"
if __name__ == "__main__":
    power.setVoltage(0,2)
    sleep(0.1)
    power.setVoltage(5,2)
    while(True):
        if('CPU Stopped' in get_cmd_result("e p")):
            get_cmd_result("e f853c 88")
            if('f8530 :                                     88'in get_cmd_result("e f853c")):
                get_cmd_result("e r pc c0")
                if('read cm0 reg f = c0\n'in get_cmd_result("e r pc")):
                    get_cmd_result("e otw 0 1111")
                    break
    ft_test_init()
    Creat_Thread(Check_CurrThread)
    gen_id()
    RC192_test()
    print(osc_32k_cal())

    val = HvLdo_test()
    otp_buff.append(val)
    print(val)
    down_otp("0b")
    val = Vcard_test(0)
    otp_buff.append(val)
    print(val)
    down_otp("0f")

    val = Vcard_test(1)
    otp_buff.append(val)
    print(val)
    down_otp("0f")
    # char_val = charg_test()
    # otp_buff.append(char_val)
    # print(char_val)

    print(otp_buff)
    Write_OtpBySelf()

```
