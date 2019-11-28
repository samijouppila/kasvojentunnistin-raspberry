import serial
import io 




#s = serial.Serial('COM4')
s = serial.Serial('/dev/ttyACM0')


def Lukija():
    while True:
        #lukee sarjaporttia ja antaa valuen        s = serial.Serial('COM4')
        res = s.read()
        value1 = res
        #muuttaan serialista luetun stringin kokonaisluvuksi
        muutettuValue = int(value1)
                

        if muutettuValue == 1:
            print("testi")
            return True
        






#Lukija()