# -*- coding: utf-8 -*-
import os
import time
import stitch
import cv2
def Webshot(url, left_crop, right_crop, browser, tmp_folder):
  browser.get(url)
  position = 0
  browser.execute_script('window.scroll(0,' + str(position) + ');')
  time.sleep(5)
  browser.save_screenshot(os.path.join(tmp_folder, "shot1.png"))
  width = cv2.imread(os.path.join(tmp_folder, "shot1.png")).shape[1]
  Img1 = cv2.imread(os.path.join(tmp_folder, "shot1.png"))[:, left_crop:width-right_crop, :]
  position = 100
  browser.execute_script('window.scroll(0,' + str(position) + ');')
  time.sleep(1)
  browser.save_screenshot(os.path.join(tmp_folder, "shot2.png"))
  Img2 = cv2.imread(os.path.join(tmp_folder, "shot2.png"))[:, left_crop:width-right_crop, :]
  stitch.stitch_v(Img1, Img2, os.path.join(tmp_folder, "shot.png"))
  while not (Img1 == Img2).all():
    position += 100
    browser.execute_script('window.scroll(0,' + str(position) + ');')
    time.sleep(1)
    browser.save_screenshot(os.path.join(tmp_folder, "shot2.png"))
    Img1 = Img2.copy()
    Img2 = cv2.imread(os.path.join(tmp_folder, "shot2.png"))[:, left_crop:width-right_crop, :]
    Img = cv2.imread(os.path.join(tmp_folder, "shot.png"))
    try:
      stitch.stitch_v(Img, Img2, os.path.join(tmp_folder, "shot.png"))
    except:
      stitch.stitch_s(Img, Img2, 100, os.path.join(tmp_folder, "shot.png"))
