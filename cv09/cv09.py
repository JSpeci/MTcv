"""
neposilat na email, ukazat cv 26.4.2018
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2

def nacteni_dat(cesta):
    
    bgr = cv2.imread(cesta)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb

if __name__ == "__main__":
    
    im = nacteni_dat("./Cv09_obr.bmp")
    z = np.zeros(np.shape(im[:,:,0])).astype('uint8')
    
    r = im[:,:,0]
    g = im[:,:,1]
    b = im[:,:,2]    
    r = np.transpose([r,z,z],(1,2,0))    
    g = np.transpose([z,g,z],(1,2,0))  
    b = np.transpose([z,z,b],(1,2,0))  
    
    gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
    
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.title('Red')
    plt.imshow(r)
    plt.subplot(2, 2, 2)
    plt.title('Green')
    plt.imshow(g)
    plt.subplot(2, 2, 3)
    plt.title('Blue')
    plt.imshow(b)
    plt.subplot(2, 2, 4)
    plt.title('Grayscale')
    plt.imshow(gray, cmap='gray')
    plt.show()
    
    r = im[:,:,0]
    g = im[:,:,1]
    b = im[:,:,2]    
    r = r.flatten().astype('int32')
    g = g.flatten().astype('int32')
    b = b.flatten().astype('int32')
    
    stredni_vektor = ((1.0/3.0) * np.add(r, np.add(g,b))).astype('int32')
    
    ri = np.subtract(r,stredni_vektor)
    bi = np.subtract(g,stredni_vektor)
    gi = np.subtract(b,stredni_vektor)
    
    W = np.zeros((np.shape(ri)[0],3)).astype('int32')
    W[:,0] = ri
    W[:,1] = gi
    W[:,2] = bi
    
    covm = np.dot(np.transpose(W), W)
    lambdas, vectors = np.linalg.eig(covm)
    
    #kontrola rovnosti eig A1=A2
    A1 = np.dot(lambdas[0], vectors[:,0])
    A2 = np.dot(covm, vectors[:,0])
    
    
    # Matice Ep (M x M) 
    Ep = np.zeros((3,3))
    
    #Ep vytvořená z vlastních vektorů setříděných dle vlastních čísel:
    min_e = np.inf
    index_min = 0
    for i in range(0, len(lambdas)):
        for j in range(0, len(lambdas)):
            if lambdas[j] < min_e:
                min_e = lambdas[j]
                index_min = j

        Ep[:,i] = vectors[:,index_min]
        lambdas[index_min] = np.inf
        min_e = np.inf     
    
    #vlastni prostor
    E = np.dot(W,Ep)
    
    #unflatten 
    K1 = np.reshape(E[:, 0] + stredni_vektor, (np.shape(im[:,:,0])))
    K2 = np.reshape(E[:, 1] + stredni_vektor, (np.shape(im[:,:,0])))
    K3 = np.reshape(E[:, 2] + stredni_vektor, (np.shape(im[:,:,0])))
    
    #plot K1 - K3
    plt.figure()
    plt.subplot(2, 2, 1)
    plt.title('Original')
    plt.imshow(im)
    plt.subplot(2, 2, 2)
    plt.title('K1')
    plt.imshow(K1, cmap='gray')
    plt.subplot(2, 2, 3)
    plt.title('K2')
    plt.imshow(K2, cmap='gray')
    plt.subplot(2, 2, 4)
    plt.title('K3')
    plt.imshow(K3, cmap='gray')
    plt.show()

    #compare Grayscale original and K1
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title('K1')
    plt.imshow(K1, cmap='gray')    
    plt.subplot(1, 2, 2)
    plt.title('Grayscaled original')
    plt.imshow(gray, cmap='gray')
    plt.show()
    
    
    
    
    
    
    

    