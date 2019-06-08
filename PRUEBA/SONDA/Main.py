import sqlite3
import time
from Sensores import sensor_temperatura
from Sensores import i2c


##Lectura de Sensores
conn = sqlite3.connect('prueba.db')
c = conn.cursor()

while True:
    temp=sensor_temperatura.read_temp()[0]
    reading_time = time.ctime(time.time())
    #DO= i2c.leerSensores("R","DO")
    #PH= i2c.leerSensores("R","PH")
    #CE= i2c.leerSensores("R","CE")
    #
    #SEN= {"DO":DO,"OPR":98,"PH":PH, "CE":CE[0:4],"TDS": CE[5], "S": CE[7:11]}
    #print (SEN)

    print (temp)
    print (reading_time)
    ##print ("CE: "+ str(CE[0:4]))
    ##print ("TDS: "+ str(CE[5]))
    ##print ("S: "+ str(CE[7:11]))


    ## Almacenamiento en BD



    c.execute("INSERT INTO lecturas VALUES (datetime('now','localtime'), ?, ?)",
                  ('Humidity', temp,))

    conn.commit()

    time.sleep(2.0)

