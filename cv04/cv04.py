import cv2
import numpy as np
import matplotlib.pyplot as plt


def jasova_korekce(path_img, path_et, c=255):
    """
    pr1
    :param path_img:
    :param path_et:
    :param c:
    :return:
    """
    # nacteni
    im1 = cv2.imread(path_img)
    et1 = cv2.imread(path_et)

    # prevod z BGR do RGB
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
    et1 = cv2.cvtColor(et1, cv2.COLOR_BGR2RGB)

    # tvorba vysledne matice o stejnych rozmerech jako vstup
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

    et = np.multiply(et, (1.0/255))
    # prevracena hodnota etalonu po prvcich
    et = np.multiply(1.0/et, 1.0)

    # nasobeni matic po prvcich a po vstvach -i
    for i in range(0,3):
        res[:, :, i] = np.multiply(et[:, :, i], im[:, :, i])

    # prevod zpet do urovni (0,255)
    res = np.multiply(res, c)

    # prevod na celociselne matice
    res = res.astype('uint8')

    # tuple
    return et1, im1, res


def img_hist(im):
    """
    vypocteni normalizovaneho histogramu
    :param im:
    :return:
    """
    size = im.shape
    width = size[0]
    height = size[1]
    h = [0.0] * 256
    for i in range(0, width, 1):
        for j in range(0, height, 1):
            h[im[i, j]] += 1

    return np.array(h) / (width * height)


def cum_sum(histogram):
    """
    kumulativni suma
    :param histogram:
    :return:
    """
    return [sum(histogram[:i + 1]) for i in range(len(histogram))]


def histeq(im):
    """
    cela funkce
    :param im:
    :return:
    """
    # vypocitani histogramu
    orig_hist = img_hist(im)

    # kumulativni distribucni funkce
    kdf = np.array(cum_sum(orig_hist))

    # hledani hodnot prenosove funkce
    sk = np.uint8(255 * kdf)
    sizes = im.shape
    width = sizes[0]
    height = sizes[1]

    result_image = np.zeros_like(im)

    # aplikovani zmenenych hodnot na kazdy pixel
    for i in range(0, width):
        for j in range(0, height):
            result_image[i, j] = sk[im[i, j]]

    result_hist = img_hist(result_image)

    return result_image, orig_hist, result_hist


if _name_ == "_main_":

    jas1 = jasova_korekce('Cv04_porucha1.bmp','Cv04_porucha1_etalon.bmp')
    jas2 = jasova_korekce('Cv04_porucha2.bmp','Cv04_porucha2_etalon.bmp')

    plt.figure(1)
    plt.subplot(2, 3, 1)
    plt.imshow(jas1[0])

    plt.subplot(2, 3, 2)
    plt.imshow(jas1[1])

    plt.subplot(2, 3, 3)
    plt.imshow(jas1[2])

    plt.subplot(2, 3, 4)
    plt.imshow(jas2[0])

    plt.subplot(2, 3, 5)
    plt.imshow(jas2[1])

    plt.subplot(2, 3, 6)
    plt.imshow(jas2[2])

    plt.show()

    orig_image = cv2.imread('Cv04_rentgen.bmp')

    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2GRAY)

    # zobrazeni orig
    plt.figure(2, figsize=(10, 7))  # uprava velikosti vysledneho grafu
    plt.subplot(221)
    plt.imshow(orig_image, cmap='gray')
    plt.title('original')
    # plt.set_cmap('gray') == cmap='gray'

    new_img, orig_h, new_h = histeq(image)

    # zobrazeni upraveneho img
    plt.subplot(223)
    plt.imshow(new_img)
    plt.title('new')
    plt.set_cmap('gray')

    # dosazeni histogramu
    plt.subplot(222)
    plt.plot(orig_h)
    plt.title('original')

    plt.subplot(224)
    plt.plot(new_h)
    plt.title('new')

    plt.show()