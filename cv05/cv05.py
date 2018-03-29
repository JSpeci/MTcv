import numpy as np
import matplotlib.pyplot as plt
import struct
import collections

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

def doLZW(dict_of_abc, list_of_data):

    #zdroj https://www.youtube.com/watch?v=rTYOQbIeUNs

    result = []
    
    data = np.array(list_of_data)
    dic = np.array(list(dict_of_abc.values()))
    
   
    P = None
    PC = None
    for i in range(0,len(data)):
        C = data[i]
        if i==0:
            PC = np.array([C])
        else:
            PC = np.append(P,C)
            
        
        #pokud existuje PC ve slovniku
        if np.sum(np.isin(dic, PC)) > 0:
            #P neposlat na vystup
            #PC presunout do P
            P = np.copy(PC)
        else:
            P = np.copy(C)
            print("append")
            dic = np.append(dic,PC)
            #PC = np.array([])
        #pokud neexistuje PC ve slovniku
            #C presunout do P
            #PC pridat do slovniku
    
        print(PC)

        
    

    return result

if __name__ == "__main__":
    data = read_bytes_to_list("Cv05_LZW_data.bin")
    abc = {1:1,2:2,3:3,4:4,5:5}

    data2 = ['w','a','b','b','a','w','a','b','b','a']

    abc2 = {
        1:['a'],
        2:['b'],
        3:['w']
    }
    
    coded = doLZW(abc,data)
    
    a = np.array([1,2,3,4,5])
    b = np.isin([7,8],a)
    print(np.sum(b))


    
