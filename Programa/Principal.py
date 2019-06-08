#!/usr/bin/python

import io         # usado para crear secuencias de archivos
import fcntl      # utilizado para acceder a los parámetros I2C como direcciones

import time       # utilizado para el retraso del sueño y las marcas de tiempo
import string     # ayuda a analizar cadenas


class AtlasI2C:
	long_timeout = 1.5         	# el tiempo de espera necesario para consultar lecturas y calibraciones
	short_timeout = .5         	# tiempo de espera para los comandos regulares
	default_bus = 1         	   # el bus predeterminado para I2C en el Raspberry Pis más nuevo, ciertos tableros más antiguos usan el bus 0
	default_address = 98     	  # la dirección predeterminada para el sensor
	current_addr = default_address

	def __init__(self, address=default_address, bus=default_bus):
		# abrir dos cadenas de archivos, una para leer y otra para escribir
		# el canal I2C específico se selecciona con el bus
		# por lo general es 1, a excepción de revisiones antiguas donde es 0
		# wb y rb indican lectura y escritura binarias
		self.file_read = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
		self.file_write = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)

		# inicializa I2C a una dirección predeterminada o especificada por el usuario
		self.set_i2c_address(address)

	def set_i2c_address(self, addr):
		# establecer las comunicaciones I2C al esclavo especificado por la dirección
		# Los comandos para el desarrollador I2C que usa las funciones ioctl se especifican en
		# el archivo i2c-dev.h de i2c-tools
		I2C_SLAVE = 0x703
		fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
		fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
		self.current_addr = addr

	def write(self, cmd):
		# agrega el carácter nulo y envía la cadena sobre I2C
		cmd += "\00"
		self.file_write.write(cmd)

	def read(self, num_of_bytes=31):
		# lee un número específico de bytes de I2C, luego analiza y muestra el resultado
		res = self.file_read.read(num_of_bytes)         # # leído del tablero
		response = filter(lambda x: x != '\x00', res)     # eliminar los caracteres nulos para obtener la respuesta
		if ord(response[0]) == 1:             # si la respuesta no es un error
			# cambie MSB a 0 para todos los caracteres recibidos excepto el primero y obtenga una lista de caracteres
			char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
			# NOTA: tener que cambiar el MSB a 0 es un fallo en el pi de frambuesa, ¡y no debería tener que hacer esto!
			return "Command succeeded " + ''.join(char_list)     # convertir la lista de caracteres en una cadena y la devuelve
		else:
			return "Error " + str(ord(response[0]))

	def query(self, string):
		# escriba un comando en la pizarra, espere el tiempo de espera correcto y lea la respuesta
		self.write(string)

		# los comandos de lectura y calibración requieren un tiempo de espera más largo
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
		prev_addr = self.current_addr # guardar la dirección actual para que podamos restaurarla después
		for i in range (0,128):
			try:
				self.set_i2c_address(i)
				self.read()
				i2c_devices.append(i)
			except IOError:
				pass
		self.set_i2c_address(prev_addr) # restore the address we were using
		return i2c_devices

		
def main():
	device = AtlasI2C() 	# creates the I2C port object, specify the address or bus if necessary

	print(">> Atlas Scientific sample code")
	print(">> Any commands entered are passed to the board via I2C except:")
	print(">>   List_addr lists the available I2C addresses.")
	print(">>   Address,xx changes the I2C address the Raspberry Pi communicates with.")
	print(">>   Poll,xx.x command continuously polls the board every xx.x seconds")
	print(" where xx.x is longer than the %0.2f second timeout." % AtlasI2C.long_timeout)
	print(">> Pressing ctrl-c will stop the polling")
	
	# main loop
	while True:
		input = raw_input("Enter command: ")

		if input.upper().startswith("LIST_ADDR"):
			devices = device.list_i2c_devices()
			for i in range(len (devices)):
				print devices[i]

		# address command lets you change which address the Raspberry Pi will poll
		elif input.upper().startswith("ADDRESS"):
			addr = int(string.split(input, ',')[1])
			device.set_i2c_address(addr)
			print("I2C address set to " + str(addr))

		# continuous polling command automatically polls the board
		elif input.upper().startswith("POLL"):
			delaytime = float(string.split(input, ',')[1])

			# check for polling time being too short, change it to the minimum timeout if too short
			if delaytime < AtlasI2C.long_timeout:
				print("Polling time is shorter than timeout, setting polling time to %0.2f" % AtlasI2C.long_timeout)
				delaytime = AtlasI2C.long_timeout

			# get the information of the board you're polling
			info = string.split(device.query("I"), ",")[1]
			print("Polling %s sensor every %0.2f seconds, press ctrl-c to stop polling" % (info, delaytime))

			try:
				while True:
					print(device.query("R"))
					time.sleep(delaytime - AtlasI2C.long_timeout)
			except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
				print("Continuous polling stopped")

		# if not a special keyword, pass commands straight to board
		else:
			if len(input) == 0:
				print "Please input valid command."
			else:
				try:
					print(device.query(input))
				except IOError:
					print("Query failed \n - Address may be invalid, use List_addr command to see available addresses")


if __name__ == '__main__':
	main()

