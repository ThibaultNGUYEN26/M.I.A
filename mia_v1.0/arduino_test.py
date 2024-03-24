import serial
import time

arduinoData = serial.Serial('COM5', 9600)

test = True

def temperature():
    data = arduinoData.readline()
    print(str(data, 'utf-8'))


while test:
    saisie = int(input("saisie : "))

    try:
        if saisie == 1:
            arduinoData.write("1".encode())
        elif saisie == 0:
            arduinoData.write("0".encode())
        elif saisie == 2:
            arduinoData.write("2".encode())
            temperature()
        else:
            test = False
    except ValueError:
        print()