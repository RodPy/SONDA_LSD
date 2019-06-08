#!/usr/bin/python


class Fraccion:

    def __init__(self,arriba,abajo):

        self.num = arriba
        self.den = abajo

    def mostrar(self):
     print(self.num,"/",self.den)