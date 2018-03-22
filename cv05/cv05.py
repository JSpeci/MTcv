import cv2
import numpy as np
import matplotlib.pyplot as plt
import struct

#poslat na email LWZ


def read_bytes_to_list(path):
    vstup = []
    index = 0
    with open(path, "rb") as f:

        byte = f.read(1)
        while byte != '':
            index = index + 1
            vstup.append(struct.unpack('b', byte )[0])
            byte = f.read(1)

            if not byte:
                break
    return vstup

if __name__ == "__main__":
    print(read_bytes_to_list("Cv05_LZW_data.bin"))
    
