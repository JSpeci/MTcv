import numpy as np
import matplotlib.pyplot as plt
import struct


class MyWave:
    
    type = "unknown yet"

    def __init__(self, path):
        self.data = []
        self.readType(path)
    
    def readType(self, path):
        with open(path, 'rb') as f:
            #head
            
            f.seek(8)
            data = f.read(4)

            """
            A1 = struct.unpack('i', f.read(4))[0]
            print(A1)
            """
            
            #todo
            self.type = data


if __name__ == "__main__":
    print("----Hello-----------------------------------\n")

    mw = MyWave('cv02_wav_01.wav')

    print(mw.type)


