import RPi.GPIO as GPIO
import time

ADS_SCLK = 0x17  
ADS_DIN = 0x13 
ADS_DOUT = 0x15  
ADS_DRDY = 0x0B  
ADS_CS = 0x0F   
ADS_REST = 0x0C   

ADS1256_CMD_WAKEUP = 0x00 
ADS1256_CMD_RDATA = 0x01 
ADS1256_CMD_RDATAC = 0x03 
ADS1256_CMD_SDATAC = 0x0f 
ADS1256_CMD_RREG = 0x10 
ADS1256_CMD_WREG = 0x50 
ADS1256_CMD_SELFCAL = 0xf0 
ADS1256_CMD_SELFOCAL = 0xf1 
ADS1256_CMD_SELFGCAL = 0xf2 
ADS1256_CMD_SYSOCAL = 0xf3 
ADS1256_CMD_SYSGCAL = 0xf4 
ADS1256_CMD_SYNC = 0xfc 
ADS1256_CMD_STANDBY = 0xfd 
ADS1256_CMD_REST = 0xfe 

ADS1256_STATUS = 0x00   
ADS1256_MUX = 0x01   
ADS1256_ADCON = 0x02   
ADS1256_DRATE = 0x03   
ADS1256_IO = 0x04   
ADS1256_OFC0 = 0x05   
ADS1256_OFC1 = 0x06   
ADS1256_OFC2 = 0x07   
ADS1256_FSC0 = 0x08   
ADS1256_FSC1 = 0x09   
ADS1256_FSC2 = 0x0A 

ADS1256_MUXP_AIN0 = 0x00 
ADS1256_MUXP_AIN1 = 0x10 
ADS1256_MUXP_AIN2 = 0x20 
ADS1256_MUXP_AIN3 = 0x30 
ADS1256_MUXP_AIN4 = 0x40 
ADS1256_MUXP_AIN5 = 0x50 
ADS1256_MUXP_AIN6 = 0x60 
ADS1256_MUXP_AIN7 = 0x70 
ADS1256_MUXP_AINCOM = 0x80 

ADS1256_MUXN_AIN0 = 0x00 
ADS1256_MUXN_AIN1 = 0x01 
ADS1256_MUXN_AIN2 = 0x02 
ADS1256_MUXN_AIN3 = 0x03 
ADS1256_MUXN_AIN4 = 0x04 
ADS1256_MUXN_AIN5 = 0x05 
ADS1256_MUXN_AIN6 = 0x06 
ADS1256_MUXN_AIN7 = 0x07 
ADS1256_MUXN_AINCOM = 0x08   

ADS1256_GAIN_1 = 0x00 
ADS1256_GAIN_2 = 0x01 
ADS1256_GAIN_4 = 0x02 
ADS1256_GAIN_8 = 0x03 
ADS1256_GAIN_16 = 0x04 
ADS1256_GAIN_32 = 0x05 
ADS1256_GAIN_64 = 0x06 
 
ADS1256_DRATE_30000SPS = 0xF0 
ADS1256_DRATE_15000SPS = 0xE0 
ADS1256_DRATE_7500SPS = 0xD0 
ADS1256_DRATE_3750SPS = 0xC0 
ADS1256_DRATE_2000SPS = 0xB0 
ADS1256_DRATE_1000SPS = 0xA1 
ADS1256_DRATE_500SPS = 0x92 
ADS1256_DRATE_100SPS = 0x82 
ADS1256_DRATE_60SPS = 0x72 
ADS1256_DRATE_50SPS = 0x63 
ADS1256_DRATE_30SPS = 0x53 
ADS1256_DRATE_25SPS = 0x43 
ADS1256_DRATE_15SPS = 0x33 
ADS1256_DRATE_10SPS = 0x23 
ADS1256_DRATE_5SPS = 0x13 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ADS_SCLK, GPIO.OUT)
GPIO.setup(ADS_DIN, GPIO.OUT)
GPIO.setup(ADS_DOUT, GPIO.IN)
GPIO.setup(ADS_DRDY, GPIO.IN)
GPIO.setup(ADS_CS, GPIO.OUT)
GPIO.setup(ADS_REST , GPIO.OUT)

GPIO.output(ADS_SCLK, GPIO.LOW)
GPIO.output(ADS_DIN, GPIO.LOW)
GPIO.output(ADS_CS, GPIO.HIGH)
GPIO.output(ADS_REST, GPIO.HIGH)


def delayMicroseconds(m):
    for i in range(0, m):
        for i in range(0, 1000):
            pass

def ADS1256SPI(m):
    i = 0
    r = 0
    delayMicroseconds(2)
    for i in range(0, 8):
        ADS_SCLK = 1
        r = r << 1
        if m & 0x80:
            ADS_DIN = 1
        else:
            ADS_DIN = 0
        m = m << 1
        ADS_SCLK = 0
        if ADS_DOUT == 1:
            r = r + 1
    return r


def ADS1256WREG(regaddr, databyte):
    ADS_CS = 0

    while(ADS_DRDY):
        pass
    
    ADS1256SPI(ADS1256_CMD_WREG | (regaddr & 0xF))
    ADS1256SPI(0)
    ADS1256SPI(databyte)
    ADS_CS = 1

'''
def ADS1256RREG(regaddr):
    r = 0
    ADS_CS = 0

    # while(ADS_DRDY):

    ADS1256SPI(ADS1256_CMD_RREG+(regaddr & 0xF))
    ADS1256SPI(0)
    r = ADS1256SPI(0)
    ADS_CS = 1
    return r


def ADS1256DRDY():
    delayMicroseconds(10);

    r = ADS1256RREG(ADS1256_STATUS)
    if r & 0x1:
        return 1
    else:
        return 0
'''

def ADS1256ReadData():
    i = 0
    sum = 0
    r = 0
    ADS_CS = 0

    while(ADS_DRDY):
        pass
    
    ADS1256SPI(ADS1256_CMD_SYNC)
    ADS1256SPI(ADS1256_CMD_WAKEUP)           
    ADS1256SPI(ADS1256_CMD_RDATA)
    ADS_SCLK = 0

    delayMicroseconds(10);

    for i in range(0, 3):
        sum = sum << 8
        r = ADS1256SPI(0)
        sum = sum | r

    ADS_CS = 1
    return sum

def ADS1256_Init():
    ADS_CS = 0
    ADS_REST = 1
    ADS1256WREG(ADS1256_STATUS,0x00)
    ADS1256WREG(ADS1256_MUX,0x08)
    ADS1256WREG(ADS1256_ADCON,0x00)
    ADS1256WREG(ADS1256_DRATE,ADS1256_DRATE_5SPS)
    ADS1256WREG(ADS1256_IO,0x00)
    ADS_CS = 1

def ADS_sum(road):
    results = 0
    ADS1256WREG(ADS1256_MUX,road)
    #ADS1256SPI(ADS1256_CMD_SELFCAL)
    results = ADS1256ReadData()
    return results

if __name__ == "__main__":

    #test delaytime    
    while True:
        time_1 = time.time()
        delayMicroseconds(1000)
        time_2 = time.time() - time_1
        print("time_1 = ", time_1)
        print("time_2 = ", time_2)
        print("time = ", time_2 - time_1)


    '''

    delayMicroseconds(10000)
    ADS1256_Init()
    delayMicroseconds(10000)

    while True:
        res1 = ADS_sum(ADS1256_MUXP_AIN0 | ADS1256_MUXN_AINCOM)
        print("res1 = ", res1)
        res2 = ADS_sum(ADS1256_MUXP_AIN1 | ADS1256_MUXN_AINCOM)
        print("res2 = ", res2)
        res3 = ADS_sum(ADS1256_MUXP_AIN2 | ADS1256_MUXN_AINCOM)
        print("res3 = ", res3)
        res4 = ADS_sum(ADS1256_MUXP_AIN3 | ADS1256_MUXN_AINCOM)
        print("res4 = ", res4)
        res5 = ADS_sum(ADS1256_MUXP_AIN4 | ADS1256_MUXN_AINCOM)
        print("res5 = ", res5)
        res6 = ADS_sum(ADS1256_MUXP_AIN5 | ADS1256_MUXN_AINCOM)
        print("res6 = ", res6)
        res7 = ADS_sum(ADS1256_MUXP_AIN6 | ADS1256_MUXN_AINCOM)
        print("res7 = ", res7)
        res8 = ADS_sum(ADS1256_MUXP_AIN7 | ADS1256_MUXN_AINCOM)
        print("res8 = ", res8)
    '''
