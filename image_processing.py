#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import random
import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image

# Unpack ketpoints
def pickle_keypoints(keypoints, descriptors):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave,
        point.class_id, descriptors[i])     
        ++i
        temp_array.append(temp)
    return temp_array

# Resize image to fit GUI
def img_resize_to_GUI(file_path):
    img = cv2.imread(file_path)
    width = img.shape[1]
    height = img.shape[0]

    if (1366/width < 768/height):
        scale_percent = 1366/width
    else:
        scale_percent = 768/height
    
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(file_path, resized)
    return resized.shape

class image:
    img = ''
    width = 0
    height = 0

    def __init__(self,path):
        self.img = cv2.imread(path)
        self.width = self.img.shape[0]
        self.height = self.img.shape[1]

# Inheritance from image
class usr_img(image):
    output_name = ''
    not_png = False
    _img_path = ''
    
    def __init__(self,path,offline):
        if (os.path.splitext(path)[1] != ".png"):
            base = os.path.splitext(path)[0]
            im = Image.open(path)
            im.save(base + ".png")
            self.img_path = base + ".png"
            self.not_png = True
        else:
            self.img_path = path

        self.img = cv2.imread(self.img_path)
        self.width = self.img.shape[0]
        self.height = self.img.shape[1]
        if(offline):
            hmerge = np.hstack((cv2.imread(self.img_path), cv2.imread(self.img_path)))
            cv2.imwrite('demo.png', hmerge)
    
    # Write file for GUI
    def output(self):
        if (self.not_png):
            os.remove(self.img_path)
        self.output_name = os.path.splitext(self.img_path)[0] + "_output.png"
        cv2.imwrite(self.output_name, self.img)
        os.remove("demo.png")

    # Write file for Flask
    def output_flask(self):   
        if (self.not_png):
            os.remove(self.img_path)
        self.output_name = os.path.splitext(self.img_path)[0] + "_output.png"
        cv2.imwrite(self.output_name, self.img)
        im1 = Image.open(self.output_name)
        jpg_name = os.path.splitext(self.img_path)[0] + "_output.jpg"
        im1.save(jpg_name)
        os.remove(self.output_name)
        return jpg_name

    # Pick near pixel to reduce quality loss
    def keypoint_obscure(self,pixel_number):
        sift = cv2.xfeatures2d.SIFT_create()
        keypoint, descriptors = sift.detectAndCompute(self.img,None)
        kd_array = pickle_keypoints(keypoint, descriptors)
   
        # x: kd_array[q][0][1]
        # y: kd_array[q][0][0]
        # range: kd_array[q][1]

        for q in range(len(kd_array)):
            for i in range(int(pixel_number)):
                random_y_1 = round(kd_array[q][0][0] + random.uniform(-kd_array[q][1],kd_array[q][1]))
                random_x_1 = round(kd_array[q][0][1] + random.uniform(-kd_array[q][1],kd_array[q][1]))
                random_y_2 = random_y_1 + random.randint(-3, 3)
                random_x_2 = random_x_1 + random.randint(-3, 3)
            
                if(random_x_1 >= self.width or random_x_2 >= self.width or random_y_1 >= self.height or random_y_2 >= self.height or random_y_1 <= 0 or random_x_1 <= 0 or random_y_2 <= 0 or random_x_2 <= 0):
                    pass
                else:
                    self.img[random_x_1,random_y_1] = self.img[random_x_2,random_y_2]
    
    # Black and white injection
    def keypoint_white_black_salt(self,Salt_and_pepper_Noise_level):
        sift = cv2.xfeatures2d.SIFT_create()
        keypoint, descriptors = sift.detectAndCompute(self.img,None)
        kd_array = pickle_keypoints(keypoint, descriptors)

        # x: kd_array[q][0][1]
        # y: kd_array[q][0][0]
        # range: kd_array[q][1]
   
        for q in range(len(kd_array)):
            for i in range(int(Salt_and_pepper_Noise_level)):
                random_y_1 = round(kd_array[q][0][0] + random.uniform(-kd_array[q][1],kd_array[q][1]))
                random_x_1 = round(kd_array[q][0][1] + random.uniform(-kd_array[q][1],kd_array[q][1])) 

                if(random_x_1 >= self.width or random_y_1 >= self.height or random_x_1 <= 0 or random_y_1 <= 0):
                    pass
                else:
                    self.img[random_x_1,random_y_1] = [255,255,255] if random.randint(0, 1) else [0,0,0]
                        
    # Draw line and box
    def Random_Shape_Draw(self,Random_Shape_level,counter):

        amount1 = random.randint(0, Random_Shape_level)/counter

        for i in range(int(amount1)):
            random_x_1 = random.randint(0,self.height)
            random_x_2 = random.randint(0,self.height)
            random_y_1 = random.randint(0,self.width)
            random_y_2 = random.randint(0,self.width)
            colour1 = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.img = cv2.line(self.img, (random_x_1, random_y_1), (random_x_2, random_y_2), colour1,random.randint(1,5))       
    
        amount2 = random.randint(0, Random_Shape_level)/counter*0.8
    
        for i in range(int(amount2)):
            random_x_3 = random.randint(0,self.height)
            random_x_4 = random.randint(0,self.height)
            random_y_3 = random.randint(0,self.width)
            random_y_4 = random.randint(0,self.width)
            colour2 = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.img = cv2.rectangle(self.img, (random_x_3, random_y_3), (random_x_4, random_y_4), colour2, random.randint(1,5))

    # Crop random pixels form edge. Aviod exact size match
    def Random_Crop(self,Random_Crop_Pixel):
        x = int(self.width - random.randint(5,Random_Crop_Pixel))
        y = int(self.height - random.randint(5,Random_Crop_Pixel))
        self.img = self.img[int(Random_Crop_Pixel):x,int(Random_Crop_Pixel):y]
    
    # Demo1: Original Image | Processed Image
    def show_demo_1(self):
        hmerge = np.hstack((cv2.imread(self.img_path), self.img))
        cv2.imwrite('demo.png', hmerge)
        return img_resize_to_GUI('demo.png')
    
    # Demo2: Original Image | SIFT Keypoint
    def show_demo_2(self):
        img2_B = cv2.imread(self.img_path)
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(self.img,None)
        cv2.drawKeypoints(self.img,kp1,img2_B,color=(255,50,255))
        hmerge = np.hstack((cv2.imread(self.img_path), img2_B))
        cv2.imwrite('demo.png', hmerge)
        img_resize_to_GUI('demo.png')

    # Demo3: Show KNN match
    def show_demo_3(self):
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(cv2.imread(self.img_path),None)
        kp2, des2 = sift.detectAndCompute(self.img,None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        good = []
        
        for m,n in matches:
            if m.distance < 0.8*n.distance:
                good.append([m])
        
        imgC = cv2.drawMatchesKnn(cv2.imread(self.img_path),kp1,self.img,kp2,good[:10000],None,flags=2)
        cv2.imwrite('demo.png', imgC)
        img_resize_to_GUI('demo.png')
        
        return len(good)
        
        