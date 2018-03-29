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

def do_LZW_Compression(dict_of_abc, list_of_data):
    
    result = []
    
    P = []
    # C je vzdy jeden prvek ze vstupu
    # rozdil mezi None a [] je v pouziti metody extend na listu
    C = []      
    PC = []
    
    #how it works video xplanation https://www.youtube.com/watch?v=MQ4ObKv2L_M
    
    for i in range(len(list_of_data)):
        
        C = []
        C.append(list_of_data[i])
        
        PC = []
        PC.extend(P)
        PC.extend(C)
        
        index_founded = dict_cointains_list(dict_of_abc, PC)
        if index_founded == -1:
            #pokud PC neni ve slovniku, pridam ho tam a P = C
            dict_of_abc[len(dict_of_abc) +1] = PC
            
            #output P key in dictionary
            result.append(dict_cointains_list(dict_of_abc,P))
            
            P = C

        else:
            #pokud PC je ve slovniku P = PC pro dalsi iteraci
            P = PC  
        
        
    #pridani posledniho prvku
    result.append(dict_cointains_list(dict_of_abc,P))
            
    return dict_of_abc, result

def do_LZW_DeCompression(dict_of_abc, list_of_data):
    
    result = []
    
    P = []
    # C je vzdy jeden prvek ze vstupu
    # rozdil mezi None a [] je v pouziti metody extend na listu
    C = []      
    PC = []
    
    #how it works video xplanation https://www.youtube.com/watch?v=MQ4ObKv2L_M
    
    for i in range(len(list_of_data)):
        pass
       
            
    return dict_of_abc, result

    

def dict_cointains_list(dict_of_abc, item_list):
    
    values = list(dict_of_abc.values())
    
    for i in range(len(values)):
        finded = True
        for j in range(len(values[i])):
            if len(item_list)  == len(values[i]):
                finded = finded and item_list[j] == values[i][j] 
            else:
                finded =  False
    
        if finded:
            return i + 1
        
    return -1



if __name__ == "__main__":
    
    data = read_bytes_to_list("Cv05_LZW_data.bin")
    abc = {1:[1],2:[2],3:[3],4:[4],5:[5]}
    
    coded = do_LZW_Compression(abc,data)
    
    # test kompresniho algoritmu
    print("Test komprese")
    print(data)
    dic = coded[0]
    res = coded[1]
    vypis = []
    for i in range(len(res)):
        vypis.extend(dic[res[i]])   
    print(vypis)
        
    
    
    


    
