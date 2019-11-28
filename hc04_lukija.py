import serial
import time
import io 

s = serial.Serial('COM4')


res = s.read()

value1 = res

#muuttaan serialista luetun stringin kokonaisluvuksi
muutettuValue = int(value1)


if muutettuValue == 1:
    print("Aktivoitu")

elif muutettuValue == 0:
    print("Ei aktiivinen")
else:
    print("Vaara luku")