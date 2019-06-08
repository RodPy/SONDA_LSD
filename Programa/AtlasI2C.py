#!/usr/bin/python

# AtlasScientifics

import io         # usado para crear secuencias de archivos
import fcntl      # utilizado para acceder a los parametros I2C como direcciones
import time       # utilizado para el retraso del suehno y las marcas de tiempo
import string     # ayuda a analizar cadenas

class AtlasI2C():
    
    	long_timeout    = 1.5         	# el tiempo de espera necesario para consultar lecturas y calibraciones
	short_timeout   = 0.5         	# tiempo de espera para los comandos regulares
	default_bus     = 1         	   # el bus predeterminado para I2C en el Raspberry Pis mas nuevo, ciertos tableros mas antiguos usan el bus 0
	default_address = 98     	  # la direccion predeterminada para el sensor
	current_addr    = default_address

def __init__(self, address=default_address, bus=default_bus):
		# abrir dos cadenas de archivos, una para leer y otra para escribir
		# el canal I2C especifico se selecciona con el bus
		# por lo general es 1, a excepcion de revisiones antiguas donde es 0
		# wb y rb indican lectura y escritura binarias
		self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
		self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

		# inicializa I2C a una direccion predeterminada o especificada por el usuario
		self.set_i2c_address(address)

	def set_i2c_address(self, addr):
		# establecer las comunicaciones I2C al esclavo especificado por la direccion
		# Los comandos para el desarrollador I2C que usa las funciones ioctl se especifican en
		# el archivo i2c-dev.h de i2c-tools
		I2C_SLAVE = 0x703
		fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
		fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
		self.current_addr = addr

	def write(self, cmd):
		# agrega el caracter nulo y envia la cadena sobre I2C
		cmd += "\00"
		self.file_write.write(cmd)

	def read(self, num_of_bytes=31):
		# lee un numero especifico de bytes de I2C, luego analiza y muestra el resultado
		res = self.file_read.read(num_of_bytes)         # # leido del tablero
		response = filter(lambda x: x != '\x00', res)     # eliminar los caracteres nulos para obtener la respuesta
		if ord(response[0]) == 1:             # si la respuesta no es un error
			# cambie MSB a 0 para todos los caracteres recibidos excepto el primero y obtenga una lista de caracteres
			char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
			# NOTA: tener que cambiar el MSB a 0 es un fallo en el pi de frambuesa, y no deberia tener que hacer esto
			return "Command succeeded " + ''.join(char_list)     # convertir la lista de caracteres en una cadena y la devuelve
		else:
			return "Error " + str(ord(response[0]))

	def query(self, string):
		# escriba un comando en la pizarra, espere el tiempo de espera correcto y lea la respuesta
		self.write(string)

		# los comandos de lectura y calibracion requieren un tiempo de espera mas largo
		if((string.upper().startswith("R")) or
			(string.upper().startswith("CAL"))):
			time.sleep(self.long_timeout)
		elif string.upper().startswith("SLEEP"):
			return "sleep mode"
		else:
			time.sleep(self.short_timeout)

		return self.read()

	def close(self):
		self.file_read.close()
		self.file_write.close()

	def list_i2c_devices(self):
		prev_addr = self.current_addr # guardar la direccion actual para que podamos restaurarla despues
		for i in range (0,128):
			try:
				self.set_i2c_address(i)
				self.read()
				i2c_devices.append(i)
			except IOError:
				pass
		self.set_i2c_address(prev_addr) # restore the address we were using
		return i2c_devices