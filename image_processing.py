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
    """Pair keypoints with descriptors safely.

    OpenCV may return None for descriptors when no keypoints are found.
    """
    if keypoints is None or len(keypoints) == 0 or descriptors is None:
        return []
    temp_array = []
    for i, point in enumerate(keypoints):
        if i >= len(descriptors):
            break
        temp = (
            point.pt,
            point.size,
            point.angle,
            point.response,
            point.octave,
            point.class_id,
            descriptors[i],
        )
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
    img_width = 0   # cols (x)
    img_height = 0  # rows (y)

    def __init__(self,path):
        self.img = cv2.imread(path)
        # OpenCV images use shape (rows, cols, channels) => (height, width, c)
        self.img_height = self.img.shape[0]
        self.img_width = self.img.shape[1]

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
        self.img_height = self.img.shape[0]
        self.img_width = self.img.shape[1]
        if(offline):
            hmerge = np.hstack((cv2.imread(self.img_path), cv2.imread(self.img_path)))
            cv2.imwrite('demo.png', hmerge)
    
    # Write file for GUI
    def output(self):
        if (self.not_png):
            os.remove(self.img_path)
        self.output_name = os.path.splitext(self.img_path)[0] + "_output.png"
        cv2.imwrite(self.output_name, self.img)
        if os.path.exists("demo.png"):
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
        keypoint, descriptors = sift.detectAndCompute(self.img, None)
        kd_array = pickle_keypoints(keypoint, descriptors)
        
        # x: kd_array[q][0][1]
        # y: kd_array[q][0][0]
        # range: kd_array[q][1]

        if not kd_array:
            return

        h, w = self.img.shape[:2]
        for q in range(len(kd_array)):
            for i in range(int(pixel_number)):
                random_y_1 = round(kd_array[q][0][0] + random.uniform(-kd_array[q][1], kd_array[q][1]))
                random_x_1 = round(kd_array[q][0][1] + random.uniform(-kd_array[q][1], kd_array[q][1]))
                random_y_2 = random_y_1 + random.randint(-3, 3)
                random_x_2 = random_x_1 + random.randint(-3, 3)

                if (
                    random_x_1 <= 0 or random_x_1 >= w or
                    random_y_1 <= 0 or random_y_1 >= h or
                    random_x_2 <= 0 or random_x_2 >= w or
                    random_y_2 <= 0 or random_y_2 >= h
                ):
                    continue
                # Numpy images are indexed as [row(y), col(x)]
                self.img[random_y_1, random_x_1] = self.img[random_y_2, random_x_2]
    
    # Black and white injection
    def keypoint_white_black_salt(self,Salt_and_pepper_Noise_level):
        sift = cv2.xfeatures2d.SIFT_create()
        keypoint, descriptors = sift.detectAndCompute(self.img, None)
        kd_array = pickle_keypoints(keypoint, descriptors)

        # x: kd_array[q][0][1]
        # y: kd_array[q][0][0]
        # range: kd_array[q][1]
   
        if not kd_array:
            return

        h, w = self.img.shape[:2]
        for q in range(len(kd_array)):
            for i in range(int(Salt_and_pepper_Noise_level)):
                random_y_1 = round(kd_array[q][0][0] + random.uniform(-kd_array[q][1], kd_array[q][1]))
                random_x_1 = round(kd_array[q][0][1] + random.uniform(-kd_array[q][1], kd_array[q][1]))

                if (
                    random_x_1 <= 0 or random_x_1 >= w or
                    random_y_1 <= 0 or random_y_1 >= h
                ):
                    continue
                self.img[random_y_1, random_x_1] = [255, 255, 255] if random.randint(0, 1) else [0, 0, 0]
                        
    # Draw line and box
    def Random_Shape_Draw(self,Random_Shape_level,counter):

        h, w = self.img.shape[:2]
        amount1 = random.randint(0, Random_Shape_level) / max(counter, 1)

        for i in range(int(amount1)):
            x1 = random.randint(0, max(w - 1, 0))
            x2 = random.randint(0, max(w - 1, 0))
            y1 = random.randint(0, max(h - 1, 0))
            y2 = random.randint(0, max(h - 1, 0))
            colour1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.img = cv2.line(self.img, (x1, y1), (x2, y2), colour1, random.randint(1, 5))

        amount2 = random.randint(0, Random_Shape_level) / max(counter, 1) * 0.8

        for i in range(int(amount2)):
            x3 = random.randint(0, max(w - 1, 0))
            x4 = random.randint(0, max(w - 1, 0))
            y3 = random.randint(0, max(h - 1, 0))
            y4 = random.randint(0, max(h - 1, 0))
            colour2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.img = cv2.rectangle(self.img, (x3, y3), (x4, y4), colour2, random.randint(1, 5))

    # Crop random pixels form edge. Aviod exact size match
    def Random_Crop(self,Random_Crop_Pixel):
        h, w = self.img.shape[:2]
        max_margin_x = max(0, min(Random_Crop_Pixel, w // 2 - 1) if w > 2 else 0)
        max_margin_y = max(0, min(Random_Crop_Pixel, h // 2 - 1) if h > 2 else 0)
        if max_margin_x < 5 or max_margin_y < 5:
            return
        left = random.randint(5, max_margin_x)
        top = random.randint(5, max_margin_y)
        right = w - random.randint(5, max_margin_x)
        bottom = h - random.randint(5, max_margin_y)
        if right - left > 1 and bottom - top > 1:
            self.img = self.img[top:bottom, left:right]
    
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
        src_img = cv2.imread(self.img_path)
        kp1, des1 = sift.detectAndCompute(src_img, None)
        kp2, des2 = sift.detectAndCompute(self.img, None)

        good = []
        if des1 is not None and des2 is not None and len(des1) > 0 and len(des2) > 0:
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            for m, n in matches:
                if m.distance < 0.8 * n.distance:
                    good.append([m])
            imgC = cv2.drawMatchesKnn(src_img, kp1, self.img, kp2, good[:10000], None, flags=2)
        else:
            # Fallback: show side-by-side if no descriptors
            imgC = np.hstack((src_img, self.img))

        cv2.imwrite('demo.png', imgC)
        img_resize_to_GUI('demo.png')

        return len(good)
        
        
