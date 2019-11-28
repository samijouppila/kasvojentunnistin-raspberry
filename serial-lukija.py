import serial
import time

s = serial.Serial('COM4')
t_end = time.time() + 60 * 2

luku = input("Anna 0 tai 1  ")

if luku == 1:

     while time.time() < t_end:
               res = s.read()
               print(res)
luku = input("Anna luku uudestaan  ")