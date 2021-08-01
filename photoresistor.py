#!/usr/bin/env python3

import ADC0832
import time

def init():
    ADC0832.setup()

def loop():
    while True:
        #The ADC0832 has two channels
        #res = ADC0832.getResult()   <-- It reads channel 0 by default. Equivalent to getResult(0)
        #res = ADC0832.getResult(1)  <-- Use this to read the second channel
        
        total_count = 1
        n = 1
        res_total = 0
        while total_count <= 60:
            res = ADC0832.getResult() - 80
           
            if res < 0:
                res = 0
            if res > 100:
                res = 100
            print (str(n) + '回目の輝度 res = %d' % res)

            res_total += res
            total_count += 1
            n += 1 
            time.sleep(1)
        
        res_mean = int(res_total/60)
        print('1分間の平均値は' + str(res_mean))

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('Cleanup ADC!')
