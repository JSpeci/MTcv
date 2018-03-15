import cv2
import numpy as np
import matplotlib.pyplot as plt
import struct

bgr = cv2.imread('cv03_objekty1.bmp')
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

height = gray.shape[0] 
width = gray.shape[1]

print("H: ",height)
print("W: ",width)

plt.close('all')
plt.figure()
#
# plt.imshow(gray)

plt.imshow(gray, cmap='gray')
#plt.colorbar()

plt.show()