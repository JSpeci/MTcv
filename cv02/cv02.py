import numpy as np
import matplotlib.pyplot as plt
import struct

"""
Trida reprezentujici nacteny wav
"""
class MyWave:

    def __init__(self, path):
        self.path = path
        self.readHead()
        self.validateHead()
        self.readData()
        self.divideIntoChannels()
    
    def readHead(self):
        with open(self.path, 'rb') as f:
            #head
            f.seek(4)
            self.A1 = struct.unpack('i', f.read(4))[0]

            #wave
            f.seek(8)
            self.typ = f.read(4)

            #riff
            f.seek(0)
            self.riff = f.read(4)

            f.seek(22)
            #h - short 2 bytes
            self.C = struct.unpack('h', f.read(2))[0]

            f.seek(24)
            self.VF = struct.unpack('i', f.read(4))[0]

            # VB-velikost „bloku“ vzorků [B] (2xB) - velikost vzorku * počet kanálů / 8
            f.seek(32)
            self.VB = struct.unpack('h', f.read(2))[0]

            # VV-velikost vzorku [b] (2xB)
            f.seek(34)
            self.VV = struct.unpack('h', f.read(2))[0]

            # A2-počet bytů do konce souboru (4xB)
            f.seek(40)
            self.A2 = struct.unpack('i', f.read(4))[0]

            #cislo potrebne pro deleni na kanaly a nacteni do struktur
            self.pocet_bytu_na_vzorek = int(self.VV / 8)

            #kolik vzorku ma jednotlivy kanal => pro osu X grafu a indexovani pole vzorku
            self.pocet_vzorku_na_kanal = int((self.A2/self.pocet_bytu_na_vzorek)/self.C)

    def readData(self):
        self.vzorky = []

        #pro ktery python datovy typ se budou bajty skladat
        formatString = 'i'
        if self.pocet_bytu_na_vzorek == 1:
            formatString = 'b' # signed byte
        if self.pocet_bytu_na_vzorek == 2:
            formatString = 'h' # short
        if self.pocet_bytu_na_vzorek == 4:
            formatString = 'i' # integer
        if self.pocet_bytu_na_vzorek == 8:
            formatString = 'q' # long

        with open(self.path, 'rb') as f:
            #konstantni cislo 44 konec hlavicky
            f.seek(44)

            # pres vsecky nactene vzorky
            for i in range(0, int(self.A2/self.pocet_bytu_na_vzorek)):

                # ctu jednotlive vzorky a vkladam do listu
                buf = f.read(self.pocet_bytu_na_vzorek)
                try:
                    vzorek = struct.unpack(formatString, buf)[0] 
                    self.vzorky.append(vzorek)
                except:
                    i = self.A2 #ukonceni smycky nacitani
                    raise TypeError("Nekompletní data. Chyba na bufferu: ",buf, " Ocekvano ",self.pocet_bytu_na_vzorek,"bajtu.")
    
    def validateHead(self):

        #pomoci logickeho soucinu zachytavam platnost vsech podminek spravnosti hlavicky
        valid = True
        valid &= self.typ.lower() != "wave"
        valid &= self.riff.lower() != "riff"
        valid &= self.VB == (self.C * self.VV)/8
        valid &= self.VF > 0
        valid &= self.VV > 0
        valid &= self.A1 > self.A2
        valid &= self.A1 == (self.A2 + 44 - 8)
        # zbytek po deleni 8 je nulovy => vzorky jsou v celych bytech
        valid &= ((self.VV / 8) % 1) == 0 
        valid &= (self.pocet_vzorku_na_kanal * self.pocet_bytu_na_vzorek * self.C) == self.A2

        if not valid:
            raise TypeError('Nekonzistentni informace v hlavicce souboru')

    def divideIntoChannels(self):
        #list listu - dvojrozmerne pole
        self.SIG = []

        #prvni rozmer je jaky kanal signalu
        for i in range(0, self.C):
            self.SIG.append(np.zeros(self.pocet_vzorku_na_kanal))
        
        #druhy rozmer jsou konkretni vzorky signalu
        for i in range(0,len(self.vzorky)):
            # vybírám každý c-tý vzorek
            c = i % self.C  #napr 0 1 2 3 0 1 2 3 0 1 2 3
            self.SIG[c][int(i / self.C)] = self.vzorky[i]  #napr 0 0 0 0 1 1 1 2 2 2 2
        
    def printHead(self):
        #prosty vypis do konzole
        print("File ", self.path)
        print("C ", self.C)
        print("VV ", self.VV)
        print("PBnV", self.pocet_bytu_na_vzorek)
        print("VB ", self.VB)
        print("VF ", self.VF)
        print("A2 ", self.A2)
        print("PVnK ", self.pocet_vzorku_na_kanal)

    def plotSIG(self):

        #osa X
        t = np.arange(self.pocet_vzorku_na_kanal).astype(float)/self.VF
        fig = plt.figure()

        if self.C == 1:
            plt.plot(t, self.SIG[0])
            plt.xlabel('t[s]')
            plt.ylabel('A[-]')          

        if self.C == 2:
            axes = fig.subplots(nrows=1, ncols=2)

            for i in range(0, self.C):
                plt.subplot(1,2,i+1)
                plt.plot(t,self.SIG[i])
                plt.xlabel('t[s]')
                plt.ylabel('A[-]')

        if self.C == 4:
            axes = fig.subplots(nrows=2, ncols=2)

            for i in range(0, self.C):
                plt.subplot(2,2,i+1)
                plt.plot(t,self.SIG[i])
                plt.xlabel('t[s]')
                plt.ylabel('A[-]')

        plt.show()



if __name__ == "__main__":

    print("----Wave opener-----------------------------------\n")
    mw = MyWave('cv02_wav_03.wav')
    mw.printHead()
    mw.plotSIG()

