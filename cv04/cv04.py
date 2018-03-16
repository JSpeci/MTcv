import cv2
import numpy as np
import matplotlib.pyplot as plt
import struct


def jasova_korekce(path_img, path_et, c = 255):
    #nacteni
    im1 = cv2.imread(path_img)
    et1 = cv2.imread(path_et)

    #prevod z BGR do RGB
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
    et1 = cv2.cvtColor(et1, cv2.COLOR_BGR2RGB)

    #tvorba vysledne matice o stejnych rozmerech jako vstup
    res = np.zeros(np.shape(et1)).astype('double')

    # in double
    im = im1.astype('double')
    # interval (0,1)
    im = np.multiply(im,(1.0/255))

    # tam kde je etalon nula - dojde k deleni nulou, upravim z nul na jednicky
    et1[et1 == 0] = 1 # pozdeji to bude 1/255 misto 0/255

    # etalon in double
    et = et1.astype('double')
    # etalon v intervalu (0,1)

    et = np.multiply(et,(1.0/255))
    # prevracena hodnota etalonu po prvcich
    et = np.multiply(1.0/et, 1.0)

    #nasobeni matic po prvcich a po vstvach -i
    for i in range(0,3):
        res[:,:,i] = np.multiply(et[:,:,i],im[:,:,i])

    # prevod zpet do urovni (0,255)
    res = np.multiply(res, c)

    # prevod na celociselne matice
    res = res.astype('uint8')

    #plot

    return (et1,im1,res)

if __name__ == "__main__":
    jas1 = jasova_korekce('Cv04_porucha1.bmp','Cv04_porucha1_etalon.bmp')
    jas2 = jasova_korekce('Cv04_porucha2.bmp','Cv04_porucha2_etalon.bmp')

    plt.figure()
    plt.subplot(2,3,1)
    plt.imshow(jas1[0])

    plt.subplot(2,3,2)
    plt.imshow(jas1[1])

    plt.subplot(2,3,3)
    plt.imshow(jas1[2])

    plt.subplot(2,3,4)
    plt.imshow(jas2[0])

    plt.subplot(2,3,5)
    plt.imshow(jas2[1])

    plt.subplot(2,3,6)
    plt.imshow(jas2[2])

    plt.show()
