#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import PySimpleGUI as sg
import numpy as np
import cv2
import time
import image_processing
from matplotlib import pyplot as plt
from PIL import Image

def img_processing_SIFT(original_img_path,counter,pixel_number,Salt_and_pepper_Noise_level):
    hmerge = np.hstack((cv2.imread(original_img_path), cv2.imread(original_img_path)))
    cv2.imwrite('temp.png', hmerge)
    cv2.imwrite('temp_1.png', cv2.imread(original_img_path))
    sg.theme('DarkAmber')
    layout = [
          [sg.Image('temp.png',key = '-IMAGE-')],
          [sg.Multiline(default_text='开始图像处理\n', size=(100, 20),key = '-TEXT-',do_not_clear=True)],
          ]
    window = sg.Window('Momus 图像反识别工具', layout)
    counter_current = 0
    loop = 0
    
    while counter_current < counter:
        
        event, values = window.Read(timeout=1)
        if event is None:
            break
        if(pixel_number>0):
            image_processing.keypoint_obscure(original_img_path,pixel_number)
        if(Salt_and_pepper_Noise_level>0):
            image_processing.keypoint_white_black_salt(original_img_path,Salt_and_pepper_Noise_level)
        
        window.Element('-TEXT-').Update(value=("----------------------------\n第"+str(counter_current)+"次迭代\n"), append=False)
        #图片|处理后图片
        
        if(loop == 0):
            hmerge = np.hstack((cv2.imread(original_img_path), cv2.imread('temp_1.png')))
            cv2.imwrite('temp_A.png', hmerge)
            window.Element('-IMAGE-').Update('temp_A.png')

        #原图|图片特征值
        
        if(loop == 1):
            sift = cv2.xfeatures2d.SIFT_create()
            kp1, des1 = sift.detectAndCompute(cv2.imread('temp_1.png'),None)
            img2_B = cv2.drawKeypoints(cv2.imread('temp_1.png'),kp1,cv2.imread('temp_1.png'),color=(255,50,255))
            hmerge2 = np.hstack((cv2.imread(original_img_path), img2_B))
            cv2.imwrite('temp_B.png', hmerge2)
            window.Element('-IMAGE-').Update('temp_B.png')
          
        #原图|处理后图片匹配
        
        if(loop == 2):
            kp2, des2 = sift.detectAndCompute(cv2.imread(original_img_path),None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des2,des1, k=2)
            good = []
            for m,n in matches:
                if m.distance < 0.001*n.distance:
                    good.append([m])
            imgC = cv2.drawMatchesKnn(cv2.imread(original_img_path),kp2,cv2.imread('temp_1.png'),kp1,matches,None,flags=2)
            cv2.imwrite('temp_C.png', imgC)
            window.Element('-IMAGE-').Update('temp_C.png')

        window.Element('-TEXT-').Update(value="更新特征值中\n", append=True)
        counter_current += 1
        loop += 1
        if (loop == 3):
            loop = 0
    window.close()
    sg.Popup('完成')
    cv2.imwrite('output.png', cv2.imread('temp_1.png'))
      
    
#def img_processing_SURF(img_path):


def mainwindow():

    sg.theme('DarkAmber')
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Help', '&About...'], ]

# ------ Column Definition ------ #
    column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

    layout = [
            [sg.Text('要处理的图片或文件夹:')],
            [sg.Input(), sg.FileBrowse()], 
            [sg.Checkbox('反OCR识别', size=(12,1),default=False),  sg.Checkbox('反SIFT匹配识别(BFmatcher)', size=(37,1),default=True)],
            [sg.Checkbox('水印', size=(12,1),default=False), sg.Checkbox('反SURF匹配识别(FlannBasedMatcher)', size=(37,1),default=False)],
            [sg.Text(' ')],
            [sg.Text('干扰手段:')],
            [sg.Checkbox('近似值处理(Pixel Approximation) 密度:', size=(38,1),default=True)],
            [sg.Slider(range=(1, 20), orientation='h', size=(40, 5), default_value=2)],
            [sg.Checkbox('(推荐)椒盐噪声(Salt-and-pepper Noise) 密度:', size=(38,1),default=True)],
            [sg.Slider(range=(1, 20), orientation='h', size=(40, 5), default_value=2)],
            [sg.Text(' ')],
            [sg.Text('迭代次数:')],
            [sg.Slider(range=(1, 100), orientation='h', size=(40, 5), default_value=20)],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()],
        ]

    window = sg.Window('Momus 图像反识别工具', layout)
    event, values = window.read()
    window.close()
    return values

def cleanup(filepath):
    os.remove("temp.png")
    os.remove("temp_1.png")
    os.remove("temp_A.png")
    os.remove("temp_B.png")

def main():
    parameter = mainwindow()
    filepath = parameter[0]
    anti_OCR = parameter[1]
    anti_SIFT_BFmatcher = parameter[2]
    anti_SURF_FlannBasedMatcher = parameter[3]
    watermark = parameter[4]
    Gaussian_noise = parameter[5]
    Gaussian_noise_level = parameter[6]
    Salt_and_pepper_Noise = parameter[7]
    Salt_and_pepper_Noise_level = parameter[8]
    counter = parameter[9]
    filepath = image_processing.jpg_to_png(filepath)
    if(Gaussian_noise):
        pass
    else:
        Gaussian_noise_level = 0
    if(Salt_and_pepper_Noise):
        pass
    else:
        Salt_and_pepper_Noise_level = 0
    img_processing_SIFT(filepath,counter,Gaussian_noise_level,Salt_and_pepper_Noise_level)
   
    
    cleanup(filepath);
    
if __name__ == "__main__":
    main()

'''
Reference:
https://link.springer.com/content/pdf/10.1186/1687-417X-2013-8.pdf
https://docs.opencv.org/3.4/d2/d29/classcv_1_1KeyPoint.html
https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
https://pysimplegui.readthedocs.io/en/latest/
https://isotope11.com/blog/storing-surf-sift-orb-keypoints-using-opencv-in-python
'''
