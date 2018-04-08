"""
Aritmeticke kodovani Poslat na email
"""

import pprint as pp
import struct
import operator

def read_bytes_to_list(path):
    """
    Nacte bajty ze vstupniho binarniho souboru a preve je na uint8
    a vrati jako list
    """
    vstup = []
    index = 0
    with open(path, "rb") as my_file:

        byte = my_file.read(1)
        while byte != '':
            index = index + 1
            vstup.append(struct.unpack('b', byte)[0])
            byte = my_file.read(1)

            if not byte:
                break
    return vstup

def probability_of_elements(list_of_data):
    """
    Vytvori slovnik vstupni abecedy a jejich cetností/pocet vsech znaku vstupu
    {1: 0.4, 2: 0.2, 3: 0.3, 4: 0.1}
    """
    result = {}
    #najdu vsecky unikatni hodnoty do slovniku
    for i in range(len(list_of_data)):
        prvek = list_of_data[i]
        if not prvek in result:
            result[prvek] = 0

    #spoctu cetnosti
    for i in range(len(list_of_data)):
        prvek = list_of_data[i]
        result[prvek] = result[prvek] +1

    #normalizace do intervalu (0,1)
    for key in result:
        result[key] /= len(list_of_data)

    #sort dict by key
    sorted_result = sorted(result.items(), key=operator.itemgetter(0), reverse=False)

    #build result dict
    result = {}
    for i in range(len(sorted_result)):
        result[sorted_result[i][0]] = sorted_result[i][1]

    return result

def kumulativni_pst(dict_of_data):
    """
    Vstup s abecedou 1234
    Vypocte intervaly kumulativni pravdepodobnosti na intervalu (0,1)
    {1: (0.0, 0.4), 2: (0.4, 0.6), 3: (0.6, 0.9), 4: (0.9, 1.0)}
    """
    result = {}
    poc = 0.0
    kon = 0.0

    for key in dict_of_data:
        kon += dict_of_data[key]
        kon = round(kon, 12)
        result[key] = (poc, kon)
        poc += dict_of_data[key]
        poc = round(poc, 12)

    return result

def arithmetic_coding(dict_of_intervals, data):
    """
    Postupně jsou brány znaky z datového řetězce, k nim známe IZ = <ZL, ZH)
    Nová hodnota intervalu IN = <L + ZL*(H - L), L + ZH*(H - L))

    https://www.youtube.com/watch?v=ZCLsJdlZzAw
    """

    #inicializovany interval
    interval = (0.0, 1.0)

    #pro zajimavost do vypisu
    list_of_interval = []

    for i in range(len(data)):
        L = interval[0]
        H = interval[1]
        ZL = dict_of_intervals[data[i]][0]
        ZH = dict_of_intervals[data[i]][1]
        #novy interval na zaklade vypoctu
        NL = (L + ZL*(H - L))
        NH = (L + ZH*(H - L))
        #zaokrouhleni - zbaveni se zaokrouholovacich chyb
        NL = round(NL, 14)
        NH = round(NH, 14)
        interval = (NL, NH)

        list_of_interval.append(interval)

    #vysledek komprese je stredni hodnota posledniho intervalu
    #a slovnik kumulativnich pravdepodobnosti
    coded = (interval[0] + interval[1])/2

    return coded, list_of_interval

def arithmetic_decoding(dict_of_intervals, tag_value):
    """
    2) dekódování znaku: K = ((C – L) / (H – L)); ZL <= K < ZH >>> nalezneme
    odpovídající znak
    3) počítáme nový interval IN = <L + ZL*(H - L), L + ZH*(H - L))
    """

    result = [] #dekomprivoane
    #pro zajimavost do vypisu
    list_of_interval = []
    middles = []
    Ks = []

    #inicializovany interval
    interval = (0.0, 1.0)
    C = tag_value
    continue_decoding = True

    while continue_decoding:
        list_of_interval.append(interval)

        H = interval[1]
        L = interval[0]

        K = ((C - L) / (H - L))
        K = round(K, 14)
        Ks.append(K)

        interval_found = () #nalezeny interval v kumulativnich pst
        for key in dict_of_intervals:
            if is_in_interval(K, dict_of_intervals[key]):
                result.append(key)
                interval_found = dict_of_intervals[key]
                break

        #vypocet noveho intervalu
        ZL = interval_found[0]
        ZH = interval_found[1]
        NL = L + ZL*(H - L)
        NH = L + ZH*(H - L)

        NL = round((L + ZL*(H - L)), 14)
        NH = round((L + ZH*(H - L)), 14)
        interval = (NL, NH)

        middle_of_interval = round((interval[0] + interval[1])/2, 14)
        middles.append(middle_of_interval)

        #ukoncnei cyklu pokud uz jsem na poslednim intervalu
        continue_decoding = middle_of_interval != tag_value

    return result, list_of_interval, middles, Ks

def is_in_interval(number, interval):
    """
    interval <L,H)
    """
    if interval[0] >= interval[1]:
        return False

    return number >= interval[0] and number < interval[1]

def print_coding_decoding_example():
    """
    Detailni vypis
    """
    data = read_bytes_to_list('Cv07_Aritm_data.bin')
    #data = ['C','B','A','A','B','C','A','D','A','C'] # data z prednasky
    #data = ['m','n','o','p','p','p','p','p','p','p']

    print("\nKOMPRESE\n\nVstupni data")
    pp.pprint(data)

    print("\nPravděpodobnosti")
    data_prob = probability_of_elements(data)
    pp.pprint(data_prob)

    print("\nKumulativní pravděpodobnost - intervaly <L,H)")
    kum = kumulativni_pst(data_prob)
    pp.pprint(kum)

    print("\nAritmetické kódování s meziintervaly")
    coded = arithmetic_coding(kum, data)
    pp.pprint(coded[1])

    print("\nVýsledné číslo")
    pp.pprint(coded[0])

    print("\nDEKOMPRESE")
    decoded = arithmetic_decoding(kum, coded[0])

    print("\nVstupni kumulativni pravdepodobnosti")
    pp.pprint(kum)

    print("\nVstupni cislo")
    pp.pprint(coded[0])

    print("\nVznikajici interval pri dekompresi")
    pp.pprint(decoded[1])

    print("\nUkonceni dekompresni smycky, rovnost Vstupniho cisla a stredni",
          "\nhodnoty intervalu iterace a Vstupniho cisla ", coded[0])
    pp.pprint(decoded[2])

    print("\ncislo K v prubehu dekomprese")
    pp.pprint(decoded[3])

    print("\nVystupni dekomprimovana sekvence")
    pp.pprint(decoded[0])

    print("\nPro srovnani puvodni data")
    pp.pprint(data)

if __name__ == "__main__":
    print_coding_decoding_example()
