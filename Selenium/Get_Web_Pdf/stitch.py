import cv2
import numpy as np
def stitch_v(Img1, Img2, Imgname):
  h1 = Img1.shape[0]
  h2 = Img2.shape[0]
  h = min(h1, h2)
  for i in range(h):
    Ary1 = Img1[h1 - h + i: h1]
    Ary2 = Img2[0: h-i]
    if float((Ary1 == Ary2).sum()) / (Ary1.shape[0] * Ary1.shape[1] * Ary1.shape[2]) > 0.98:
      Ary = np.concatenate((Img1[0: h1 - h + i], Img2), axis = 0)
      break
  cv2.imwrite(Imgname, Ary)

def stitch_s(Img1, Img2, step, Imgname):
  Ary = np.concatenate((Img1[0:-step], Img2), axis = 0)
  cv2.imwrite(Imgname, Ary)
