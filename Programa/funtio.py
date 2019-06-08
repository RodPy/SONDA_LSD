
import RPi.GPIO as GPIO  
import time              
 

GPIO.setmode(GPIO.BCM)
 
#configuramos el pin GPIO17 como una salida

def setLuz(self, puerto)
    GPIO.setup(puerto, GPIO.OUT)
 
#encendemos y apagamos el led 5 veces
for i in range(0,5):
 
    GPIO.output(puerto, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(puerto, GPIO.LOW)
    time.sleep(1)
    print("Listo")
	
GPIO.cleanup()            #devuelve los pines a su estado inicial