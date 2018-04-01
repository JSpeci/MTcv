"""
poslat na email LWZ

"""
import struct
import pprint


def read_bytes_to_list(path):
    """
    Nacte bajty ze vstupniho binarniho souboru a preve je na uint8
    a vrati jako list
    """
    vstup = []
    index = 0
    with open(path, "rb") as f:

        byte = f.read(1)
        while byte != '':
            index = index + 1
            vstup.append(struct.unpack('b', byte)[0])
            byte = f.read(1)

            if not byte:
                break
    return vstup

def do_LZW_Compression(dict_of_abc, list_of_data):
    """
    LZW komprese
    
    dict_of_abc je vstupni slovnik dat
        na kazdem indexu slovniku je list
        v prubehu komprese se do nej pridavaji polozky
    
    list_of_data je posloupnost cisel ke kompresi
    """
    
    # rozdil mezi None a [] je v pouziti metody extend na listu
    
    result = []
    P = []
    C = [] # C je vzdy jeden prvek ze vstupu
    PC = []
    
    #how it works video xplanation https://www.youtube.com/watch?v=MQ4ObKv2L_M
    
    for i in range(len(list_of_data)):
        """
        Cyklus pres vsecky vstupni prvky
        """

        C = []
        C.append(list_of_data[i])

        #PC je vzdy kombinace P a C
        PC = []
        PC.extend(P)
        PC.extend(C)

        index_founded = dict_cointains_list(dict_of_abc, PC)
        if index_founded == -1:
            #pokud PC neni ve slovniku, pridam ho tam a P = C
            dict_of_abc[len(dict_of_abc) +1] = PC
            #output P key in dictionary
            result.append(dict_cointains_list(dict_of_abc, P))
            P = C
        else:
            #pokud PC je ve slovniku P = PC pro dalsi iteraci
            P = PC
    #pridani posledniho prvku
    result.append(dict_cointains_list(dict_of_abc, P))
    return dict_of_abc, result

def do_LZW_DeCompression(dict_of_abc, list_of_data):
    """
    LZW Dekomprese
    
    dict_of_abc je vstupni slovnik dat
        na kazdem indexu slovniku je list
        v prubehu komprese se do nej pridavaji polozky
    
    list_of_data je posloupnost cisel pro dekompresi
    """
    
    #https://www.youtube.com/watch?v=MQM_DsX-LBI
    
    out = []
    predchozi_out = []
    for i in range(len(list_of_data)):
        new = []
        new.extend(predchozi_out)
        if list_of_data[i] in dict_of_abc:
            o = dict_of_abc[list_of_data[i]]
            out.extend(o)
            predchozi_out = o
            
            #pokud je o list, beru z nej pouze prvni prvek
            if len(o) > 1:
                new.append(o[0])
            else:
                new.extend(o)

            index_founded = dict_cointains_list(dict_of_abc, new)
            if index_founded == -1:
                #pokud new neni ve slovniku, pridam ho tam
                dict_of_abc[len(dict_of_abc) +1] = new

    return dict_of_abc, out

def dict_cointains_list(dict_of_abc, item_list):
    """
    dict_of_abc vypada napriklad takto
    3: [3],
    4: [4],
    5: [5],
    6: [5, 4],
    9: [4, 3],
    8: [3, 5],
    9: [5, 4, 1],
    
    item_list vypada napriklad takto [5,4,1]
    
    Metoda vraci, zda ve vstupnim slovniku je nejaka polozka typu list
    a orvky toho listu jsou shodne s druhym vstupnim parametrem
    
    """

    values = list(dict_of_abc.values())

    #projdu vsecky listy ve slovniku
    for i in range(len(values)):
        #predpokladam ze ve slovniku je
        finded = True
        
        for j in range(len(values[i])):
            if len(item_list) == len(values[i]):
                # kontrola po jednotlivych hodnotach
                # logicky soucin - pokud jednou False, navzdy False
                finded = finded and item_list[j] == values[i][j]
            else:
                finded = False

        if finded:
            # cyklus indexuje od 0, slovnik ale indexujeme-klicujeme od 1
            return i + 1 

    return -1

def vypis_komprese(coded, vstupni_slovnik, vstupni_data):
    """
    Formatovany vystup komprese
    """
    # test kompresniho algoritmu
    print("Test komprese")
    print("  Vstupni data")
    print(vstupni_data)
    
    print("\n Vstupni slovnik")
    pprint.pprint(vstupni_slovnik)

    dic = coded[0]
    res = coded[1]
    vypis = []
    for i in range(len(res)):
        vypis.extend(dic[res[i]])

    print("\n  Vysledek")
    print(res)

    print("\n  Kompresni poměr")
    komp_pomer = round(len(res)/len(data) * 100)
    print(komp_pomer, " % z puvodni delky dat")

    print("\n  Slovnik")
    pprint.pprint(dic)

    print("\n  Zpetne sestaveni vstup a sestaveni ")
    print(data)
    print(vypis)

def vypis_dekomprese(decoded, vstupni_slovnik, vstupni_data):
    """
    Komentar
    """
    # test dekompresniho algoritmu
    print("\n  Test dekomprese")
    print("  Vstupni data")
    print(vstupni_data)

    print("\n Vstupni slovnik")
    pprint.pprint(vstupni_slovnik)

    dic = decoded[0]
    res = decoded[1]
    vypis = []
    for i in range(len(res)):
        vypis.extend(dic[res[i]])

    print("\n  dekomprimovany Vysledek")
    print(res)

    print("\n  Slovnik vznikly pri dekompresi")
    pprint.pprint(dic)

if __name__ == "__main__":

    data = read_bytes_to_list("Cv05_LZW_data.bin")

    abc = {1:[1], 2:[2], 3:[3], 4:[4], 5:[5]}
    vstupni_slovnik = abc.copy()
    coded = do_LZW_Compression(abc, data)
    vypis_komprese(coded, vstupni_slovnik, data)

    abc = {1:[1], 2:[2], 3:[3], 4:[4], 5:[5]}
    vstupni_slovnik = abc.copy()
    vstupni_data = coded[1].copy()
    decoded = do_LZW_DeCompression(abc, coded[1])

    vypis_dekomprese(decoded, vstupni_slovnik, vstupni_data)
