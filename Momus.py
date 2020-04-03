#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import PySimpleGUI as sg

import cv2
import random
import image_processing
from matplotlib import pyplot as plt
from PIL import Image

def img_processing_SIFT(mode,auto_target_similarity,original_img_path,counter,pixel_number,Salt_and_pepper_Noise_level,Random_Shape_level,Random_Crop_Pixel):
    user_image = image_processing.usr_img(original_img_path)
    
    shape = user_image.show_demo_1()
    window_width = shape[1]
    window_height = shape[0]

    original_matches = user_image.show_demo_3()/3
    #print("original_matches: "+ str(original_matches))
    match_proportion = 100

    sg.theme('DarkAmber')
    layout = [
                [sg.Multiline(default_text='开始图像处理\n', size=(window_width, 2),key = '-TEXT-',do_not_clear=False)],
                [sg.ProgressBar(100, orientation='h', size=(window_width, 20), key='progressbar')],
                [sg.Image('demo.png',key = '-IMAGE-')],
          ]
    window = sg.Window('Momus 图像反识别工具',layout,no_titlebar=True, size=(window_width + 2, window_height + 30))
    progress_bar = window['progressbar']
    counter_current = 0
    
    #Manual
    if (mode == 0):
        while counter_current < counter:
            event, values = window.Read(timeout=1)
            if event is None:
                break
        
            if(pixel_number>0):
                user_image.keypoint_obscure(pixel_number)
            if(Salt_and_pepper_Noise_level>0):
                user_image.keypoint_white_black_salt(Salt_and_pepper_Noise_level)
            if(Random_Shape_level>0):
                user_image.Random_Shape_Draw(Random_Shape_level,counter)

            progress_bar.UpdateBar(counter_current/counter*100)
            window.Element('-TEXT-').Update(value=("第"+str(counter_current)+"次迭代\n 匹配度: " + "%5.3f" % (match_proportion) + "%\n"), append=True)
        
            if(counter_current % 3 == 0):
                user_image.show_demo_1()
                window.Element('-IMAGE-').Update('demo.png')
                window.Element('-TEXT-').Update(value="原图对比\n", append=True)

            if(counter_current % 3 == 1):
                user_image.show_demo_2()
                window.Element('-IMAGE-').Update('demo.png')
                window.Element('-TEXT-').Update(value="更新特征值\n", append=True)
          
            if(counter_current % 3 == 2):
                match_proportion = user_image.show_demo_3()/original_matches *100
                #print("match_proportion: "+ str(match_proportion))
                window.Element('-IMAGE-').Update('demo.png')
                window.Element('-TEXT-').Update(value="KNN匹配\n", append=True)
            
            counter_current += 1
    #Auto
    if (mode == 1):  
        while match_proportion > auto_target_similarity:
            event, values = window.Read(timeout=1)
            if event is None:
                break
            
            user_image.keypoint_obscure(1)
            if (auto_target_similarity < 70):
                user_image.keypoint_white_black_salt(1)
            if (auto_target_similarity < 25):
                user_image.Random_Shape_Draw(20,15)

            window.Element('-TEXT-').Update(value=("第"+str(counter_current)+"次迭代\n 匹配度: " + "%5.3f" % (match_proportion) + "%\n"), append=True)
        
            if(counter_current % 3 == 0):
                user_image.show_demo_1()
                window.Element('-IMAGE-').Update('demo.png')
                window.Element('-TEXT-').Update(value="原图对比\n", append=True)

            if(counter_current % 3 == 1):
                user_image.show_demo_2()
                window.Element('-IMAGE-').Update('demo.png')
                window.Element('-TEXT-').Update(value="更新特征值\n", append=True)
          
            if(counter_current % 3 == 2):
                match_proportion = user_image.show_demo_3()/original_matches *100
                #print("match_proportion: "+ str(match_proportion))
                window.Element('-IMAGE-').Update('demo.png')
                window.Element('-TEXT-').Update(value="KNN匹配\n", append=True)
            
            counter_current += 1

    window.close()

    if(Random_Crop_Pixel>0 and mode == 0):
            user_image.Random_Crop(Random_Crop_Pixel)
    if(mode == 1):
            user_image.Random_Crop(random.randint(10,20))
    user_image.output()
    sg.SystemTray.notify('处理完成 ', '文件：'+ user_image.output_name)

def mainwindow():

    sg.theme('DarkAmber') 
    auto_layout =  [
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Text('目标相似度(Target Similarity)：')],
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Slider(range=(10, 100), orientation='h', size=(40, 5), default_value=30)],
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Text(' ')],
                    [sg.Submit(tooltip='Click to start',size=(20,1)), sg.Cancel(size=(20,1))],
                ]
    manual_layout =  [
                    [sg.Text('干扰手段:')],
                    [sg.Checkbox('近似值处理(Pixel Approximation) 密度:', size=(38,1),default=True)],
                    [sg.Slider(range=(1, 10), orientation='h', size=(40, 5), default_value=1)],
                    [sg.Checkbox('椒盐噪声(Salt-and-pepper Noise) 密度:', size=(38,1),default=True)],
                    [sg.Slider(range=(1, 10), orientation='h', size=(40, 5), default_value=1)],
                    [sg.Checkbox('随机线段(Random Shape) 密度:', size=(38,1),default=True)],
                    [sg.Slider(range=(1, 10), orientation='h', size=(40, 5), default_value=1)],
                    [sg.Checkbox('随机裁剪(Random Crop) 裁剪像素:', size=(40,1),default=True)],
                    [sg.Slider(range=(5, 50), orientation='h', size=(40, 5), default_value=10)],
                    [sg.Text(' ')],
                    [sg.Text('迭代次数: (对于多次无法发送的图片 多迭代小干扰)')],
                    [sg.Slider(range=(1, 50), orientation='h', size=(40, 5), default_value=5)],
                    [sg.Submit(tooltip='Click to start',size=(20,1)), sg.Cancel(size=(20,1))],
                ]
    layout = [
            [sg.Text('要处理的图片:')],
            [sg.Input(), sg.FileBrowse()], 
            [sg.Text(' ')],
            [sg.Checkbox('反SIFT (Scale-Invariant Feature Transform) 匹配识别', size=(50,1),default=True)],
            [sg.Checkbox('水印 (未开放)', size=(20,1),default=False)],
            [sg.Text(' ')],
            [sg.TabGroup([[sg.Tab('自动(Auto)', auto_layout), sg.Tab('手动(Manual)', manual_layout)]])],
        ]
    

    window = sg.Window('Momus 图像反识别工具', layout, no_titlebar=True,size=(430,580))
    event, values = window.read()
    window.close()
    return values,event

def main():
    parameter = mainwindow()
    if(parameter[1] == "Submit0"):
        mode = 0
    elif(parameter[1] == "Submit"):
        mode = 1
    else:
        exit(0)
    filepath = parameter[0][0]
    anti_SIFT = parameter[0][1]
    watermark = parameter[0][2]
    auto_target_similarity = parameter[0][3]
    Gaussian_noise = parameter[0][4]
    Gaussian_noise_level = parameter[0][5]
    Salt_and_pepper_Noise = parameter[0][6]
    Salt_and_pepper_Noise_level = parameter[0][7]
    Random_Shape = parameter[0][8]
    Random_Shape_level = parameter[0][9] * 8
    Random_Crop = parameter[0][10]
    Random_Crop_Pixel = parameter[0][11]
    counter = parameter[0][12]

    if(Gaussian_noise == False):
        Gaussian_noise_level = 0
    
    if(Salt_and_pepper_Noise== False):
        Salt_and_pepper_Noise_level = 0
    
    if(Random_Shape== False):
        Random_Shape_level = 0

    if(Random_Crop== False):
        Random_Crop_Pixel = 0

    if anti_SIFT :
        img_processing_SIFT(mode,auto_target_similarity,filepath,counter,Gaussian_noise_level,Salt_and_pepper_Noise_level,Random_Shape_level,Random_Crop_Pixel)
     
    
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
https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_OpenCV.py
'''
