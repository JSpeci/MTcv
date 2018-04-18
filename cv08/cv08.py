"""
neposilat na email, ukazat cv 19.4.2018
"""

import numpy as np
import matplotlib.pyplot as plt
import pprint as pp
import cv2
import time


def pause(s):
    time.sleep(s)

def rozdil_sum(pole_a, pole_b):
    sum1 = np.sum(pole_a)
    sum2 = np.sum(pole_b)
    T = 700000
    rozdil = 0
    if sum2 > sum1 :
        rozdil = sum2-sum1
    else:
        rozdil = sum1-sum2
    
    if rozdil >= T:
        return rozdil
    else:
        return 0

def suma_rozdilu(pole_a, pole_b):
    rozdil = np.subtract(pole_a, pole_b)
    result = np.sum(rozdil)
    T = 12000000
    
    if result >= T:
        return result
    else:
        return 0
   
def rozdil_histogramu(pole_a, pole_b):
    hist1, bin_edges1 = np.histogram(pole_a,256,[0,256])
    hist2, bin_edges2 = np.histogram(pole_b,256,[0,256])
    
    result = np.subtract(hist1, hist2)
    result = np.abs(result)
    result = np.sum(result)

    
    T = 10000
    if result > T :
        return result
    else:
        return 0   
    
def spocti_dct(obrazek):
    #https://stackoverflow.com/questions/15488700/how-to-get-dct-of-an-image-in-python-using-opencv
    imf1 = np.float64(obrazek)/255.0  # float conversion/scale
    dst1 = cv2.dct(imf1)           # the dct
    imgcv1 = np.uint64(dst1)*255.0    # convert back
    imgcv1 = imgcv1 ** 2
    #zlogaritmovani
    imgcv1 = imgcv1.flatten()
    #https://stackoverflow.com/questions/19666626/replace-all-elements-of-python-numpy-array-that-are-greater-than-some-value
    #arr[arr > 255] = x
    
    #nahradim jednickou - po zlogaritmovani se z ni stane nula - nula neovlivni rozdil a sumu
    imgcv1[imgcv1 == 0] = 1

    """
    imgcv1 = np.sort(imgcv1)
    imgcv1 = imgcv1[-5:]
    """
    
    imgcv1 = np.log(imgcv1)
    return imgcv1

def rozdil_dct_priznaku(pole_a, pole_b):

    dct1 = spocti_dct(pole_a)
    dct2 = spocti_dct(pole_b)
    
    #print(dct1)
        
    result = np.subtract(dct1,dct2)
    result = np.abs(result)
    result = np.sum(result)
    
    T = 0
    if result > T :
        return result
    else:
        return 0    

def aplikuj_metodu(data, metoda):
    
    pocet_obrazku = np.shape(data)[0]
    result = []
    for i in range(pocet_obrazku - 1):  # -1 protoze se divam i na nasledujici
        m = metoda(data[i], data[i + 1])
        result.append(m)
    return result

def nacteni_dat():
    
    obrazky = []
    
    for i in range(1, 305):
        ret = './Cv08_vid/a%.3d.bmp' %i
        bgr = cv2.imread(ret)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        #plt.imshow(gray, cmap='gray')
        #print(np.shape(gray))
        obrazky.append(gray)
    
    return obrazky

def vykresli_ctyri_grafy(list_grafu):
    koef = 1.2
    plt.figure()
    
    for i in range(0, len(list_grafu)):
            
        plt.subplot(2,2,i+1)
        plt.hold(True)
        t = range(0,305)
        v1 = np.zeros(305)
        v1[209] = np.max(list_grafu[i]) * koef
        v2 = np.zeros(305)
        v2[270] = np.max(list_grafu[i]) * koef
        plt.plot(t, v1, linewidth=1, color='r')
        plt.plot(t, v2, linewidth=1, color='g')
        plt.plot(list_grafu[i],linewidth=1, color='b')

    plt.show()
    
def vykresli_prubeh(graf):
    koef = 1.0
    t = range(0,305)
    v1 = np.zeros(305)
    v1[209] = np.max(graf) * koef
    v2 = np.zeros(305)
    v2[270] = np.max(graf) * koef
    plt.figure()
    for i in range(1, 305):
        i = i * 20 # zrychleni prochazeni
        ret = './Cv08_vid/a%.3d.bmp' %i
        bgr = cv2.imread(ret)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        
        plt.imshow(rgb, aspect='auto', extent = [min(t), max(t), min(graf), max(graf)])
        plt.hold(True)
        plt.plot(t, v1, linewidth=1, color='r')
        plt.plot(t, v2, linewidth=1, color='g')
        plt.plot(graf,linewidth=1, color='b')
        plt.axvline(x=i, linewidth=2, color='k')
        plt.axis([min(t), max(t), min(graf), max(graf)])
        plt.hold(False)
        plt.show()
        pause(0.5)
    


if __name__ == "__main__":
    
    data = nacteni_dat()
    #print(np.subtract((data[1]),(data[0])))
    graf1 = aplikuj_metodu(data, rozdil_sum)
    graf2 = aplikuj_metodu(data, suma_rozdilu)
    graf3 = aplikuj_metodu(data, rozdil_histogramu)
    graf4 = aplikuj_metodu(data, rozdil_dct_priznaku)
    
    vykresli_ctyri_grafy([graf1,graf2,graf3,graf4])
    
    vykresli_prubeh(graf3)
    

    

    
    
    
    
