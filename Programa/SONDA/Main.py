import sqlite3
from Sensores import sensor_temperatura
from Sensores import i2c


##Lectura de Sensores


DO= i2c.leerSensores("R","DO")
PH= i2c.leerSensores("R","PH")
CE= i2c.leerSensores("R","CE")
OPR= i2c.leerSensores("R","OPR")
##T= sensor_temperatura.read_temp()
T=[1,2]


SEN= {"Temp":T[0],"DO":DO,"OPR":98,"PH":PH, "CE":CE[0:4],"TDS": CE[5], "S": CE[7:11]}
print (SEN)

#para usar la bomba 

bomba("D", 15)

#print (OPR)
##print ("CE: "+ str(CE[0:4]))
##print ("TDS: "+ str(CE[5]))
##print ("S: "+ str(CE[7:11]))


## Almacenamiento en BD
