#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import PySimpleGUI as sg
import numpy as np
import cv2
import image_processing
from matplotlib import pyplot as plt
from PIL import Image

def img_processing_SIFT(original_img_path,counter,pixel_number,Salt_and_pepper_Noise_level,Random_Scalar_level,Random_Crop_Pixel):
    user_image = image_processing.usr_img(original_img_path)
    
    shape = user_image.show_demo_1()
    window_width = shape[1]
    window_height = shape[0]

    sg.theme('DarkAmber')
    layout = [
                [sg.Multiline(default_text='开始图像处理\n', size=(window_width, 2),key = '-TEXT-',do_not_clear=True)],
                [sg.Image('demo.png',key = '-IMAGE-')],
          ]
    window = sg.Window('Momus 图像反识别工具',layout, size=(window_width + 2, window_height + 4))
    counter_current = 0

    while counter_current < counter:
        event, values = window.Read(timeout=1)
        if event is None:
            break
        if(pixel_number>0):
            user_image.keypoint_obscure(pixel_number)
        if(Salt_and_pepper_Noise_level>0):
            user_image.keypoint_white_black_salt(Salt_and_pepper_Noise_level)
        if(Random_Scalar_level>0):
            user_image.Random_Scalar_Draw(Random_Scalar_level,counter)

        window.Element('-TEXT-').Update(value=("----------------------------\n第"+str(counter_current)+"次迭代\n"), append=False)
        
        if(counter_current % 3 == 0):
            user_image.show_demo_1()
            window.Element('-IMAGE-').Update('demo.png')
            window.Element('-TEXT-').Update(value="原图对比\n", append=True)

        if(counter_current % 3 == 1):
            user_image.show_demo_2()
            window.Element('-IMAGE-').Update('demo.png')
            window.Element('-TEXT-').Update(value="更新特征值\n", append=True)
          
        if(counter_current % 3 == 2):
            user_image.show_demo_3()
            window.Element('-IMAGE-').Update('demo.png')
            window.Element('-TEXT-').Update(value="KNN匹配\n", append=True)

        
        counter_current += 1
    window.close()

    if(Random_Crop_Pixel>0):
            user_image.Random_Crop(Random_Crop_Pixel)
    user_image.output()
    sg.Popup('完成')

def mainwindow():

    sg.theme('DarkAmber')
    layout = [
            [sg.Text('要处理的图片:')],
            [sg.Input(), sg.FileBrowse()], 
            [sg.Text(' ')],
            [sg.Checkbox('反SIFT (Scale-Invariant Feature Transform) 匹配识别', size=(50,1),default=True)],
            [sg.Checkbox('水印 (未开放)', size=(20,1),default=False)],
            [sg.Text(' ')],
            [sg.Text('干扰手段:')],
            [sg.Checkbox('近似值处理(Pixel Approximation) 密度:', size=(38,1),default=True)],
            [sg.Slider(range=(1, 10), orientation='h', size=(40, 5), default_value=1)],
            [sg.Checkbox('椒盐噪声(Salt-and-pepper Noise) 密度:', size=(38,1),default=True)],
            [sg.Slider(range=(1, 10), orientation='h', size=(40, 5), default_value=1)],
            [sg.Checkbox('随机线段(Random Scalar) 密度:', size=(38,1),default=True)],
            [sg.Slider(range=(1, 10), orientation='h', size=(40, 5), default_value=1)],
            [sg.Checkbox('随机裁剪(Random Crop) 裁剪像素:', size=(40,1),default=True)],
            [sg.Slider(range=(1, 30), orientation='h', size=(40, 5), default_value=3)],
            [sg.Text(' ')],
            [sg.Text('迭代次数: (对于多次无法发送的图片 多迭代小干扰)')],
            [sg.Slider(range=(1, 50), orientation='h', size=(40, 5), default_value=5)],
            [sg.Submit(tooltip='Click to submit this form'), sg.Cancel()],
        ]

    window = sg.Window('Momus 图像反识别工具', layout)
    event, values = window.read()
    window.close()
    return values

def main():
    parameter = mainwindow()
    filepath = parameter[0]
    
    anti_SIFT = parameter[1]
    watermark = parameter[2]
    Gaussian_noise = parameter[3]
    Gaussian_noise_level = parameter[4]
    Salt_and_pepper_Noise = parameter[5]
    Salt_and_pepper_Noise_level = parameter[6]
    Random_Scalar = parameter[7]
    Random_Scalar_level = parameter[8] * 8
    Random_Crop = parameter[9]
    Random_Crop_Pixel = parameter[10]
    counter = parameter[11]

    if(Gaussian_noise):
        pass
    else:
        Gaussian_noise_level = 0
    if(Salt_and_pepper_Noise):
        pass
    else:
        Salt_and_pepper_Noise_level = 0
    if(Random_Scalar):
        pass
    else:
        Random_Scalar_level = 0
    if(Random_Crop):
        pass
    else:
        Random_Crop_Pixel = 0

    if anti_SIFT :
        img_processing_SIFT(filepath,counter,Gaussian_noise_level,Salt_and_pepper_Noise_level,Random_Scalar_level,Random_Crop_Pixel)
     
    
if __name__ == "__main__":
    main()

'''
Reference:
https://link.springer.com/content/pdf/10.1186/1687-417X-2013-8.pdf
https://docs.opencv.org/3.4/d2/d29/classcv_1_1KeyPoint.html
https://docs.opencv.org/3.4/dc/dc3/tutorial_py_matcher.html
https://pysimplegui.readthedocs.io/en/latest/
https://isotope11.com/blog/storing-surf-sift-orb-keypoints-using-opencv-in-python
https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
https://docs.opencv.org/master/d4/d5d/group__features2d__draw.html
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html
'''
