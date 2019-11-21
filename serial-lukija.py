import serial
import time

s = serial.Serial('COM4')
t_end = time.time() + 60 * 2


while time.time() < t_end:
     res = s.read()
     print(res)
