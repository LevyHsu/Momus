import os
import math
import random
import cv2
from matplotlib import pyplot as plt
from PIL import Image

def pickle_keypoints(keypoints, descriptors):
    i = 0
    temp_array = []
    for point in keypoints:
        temp = (point.pt, point.size, point.angle, point.response, point.octave,
        point.class_id, descriptors[i])     
        ++i
        temp_array.append(temp)
    return temp_array

def unpickle_keypoints(array):
    keypoints = []
    descriptors = []
    for point in array:
        temp_feature = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], _response=point[3], _octave=point[4], _class_id=point[5])
        temp_descriptor = point[6]
        keypoints.append(temp_feature)
        descriptors.append(temp_descriptor)
    return keypoints, np.array(descriptors)

def keypoint_obscure(original_img_path,pixel_number):
    sift = cv2.xfeatures2d.SIFT_create()
    img = cv2.imread('temp_1.png')
    keypoint, descriptors = sift.detectAndCompute(img,None)
    kd_array = pickle_keypoints(keypoint, descriptors)

    # x: kd_array[q][0][0]
    # y: kd_array[q][0][1]
    #range: kd_array[q][1]
    width = img.shape[0]
    height = img.shape[1]

    for q in range(len(kd_array)):
        for i in range(int(pixel_number)):
            random_y_1 = round(kd_array[q][0][0] + random.uniform(-kd_array[q][1],kd_array[q][1]))
            random_x_1 = round(kd_array[q][0][1] + random.uniform(-kd_array[q][1],kd_array[q][1]))
            random_y_2 = random_y_1 + random.randint(0, 3)
            random_x_2 = random_x_1 + random.randint(0, 3)
            
            if(random_x_1 >= width or random_x_2 >= width or random_y_1 >= height or random_y_2 >= height or random_y_1 <= 0 or random_x_1 <= 0 or random_y_2 <= 0 or random_x_2 <= 0):
                pass
            else:
                img[random_x_1,random_y_1] = img[random_x_2,random_y_2]
    
    cv2.imwrite('temp_1.png', img)

def keypoint_white_black_salt(original_img_path,Salt_and_pepper_Noise_level):
    sift = cv2.xfeatures2d.SIFT_create()
    img = cv2.imread('temp_1.png')
    keypoint, descriptors = sift.detectAndCompute(img,None)
    kd_array = pickle_keypoints(keypoint, descriptors)

    # x: kd_array[q][0][0]
    # y: kd_array[q][0][1]
    #range: kd_array[q][1]
    width = img.shape[0]
    height = img.shape[1]
   
    for q in range(len(kd_array)):
        for i in range(int(Salt_and_pepper_Noise_level)):
            random_y_1 = round(kd_array[q][0][0] + random.uniform(-kd_array[q][1],kd_array[q][1]))
            random_x_1 = round(kd_array[q][0][1] + random.uniform(-kd_array[q][1],kd_array[q][1])) 
            print(random_y_1)
            print(random_x_1)
            print("------------------")
            seed = random.randint(0, 1)
            if(random_x_1 >= width or random_y_1 >= height or random_x_1 <= 0 or random_y_1 <= 0):
                pass
            else:
                if (seed == 0):
                    img[random_x_1,random_y_1] = [255,255,255]
                else:
                    img[random_x_1,random_y_1] = [0,0,0]
    
    cv2.imwrite('temp_1.png', img)


def jpg_to_png(original_img_path):

    base = os.path.splitext(original_img_path)[0]
    im = Image.open(original_img_path)
    im.save(base + ".png")
    
    return base + ".png"