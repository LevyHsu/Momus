# Momus
### Momus is a cross-platform image processing tool that designed to counter image matching on social media platform.
### Momus是一款用来绕过社交平台AI图片匹配的跨平台工具

#### Monus uses SIFT（Scale Invariant Feature Transform） from opencv to detect all keypoint on img then inject noise to avoid auto-detection.
#### Monus使用opencv库中的SIFT（Scale Invariant Feature Transform）算法来标记所有的关键点，然后添加噪音来避免社交平台的图片自动匹配
****
### Online Demo(WITH FLASK):

[Momus Online](http://momus.levyhsu.com/)<br/>

![](Demo/online_demo_1.jpg)

Extra library needed:
```
flask
```
Run:
```bash
python3 Momus_flask.py
```

****

### Offline version(WITH GUI):
Libraries:
```
PySimpleGUI
numpy
cv2
matplotlib
pillow
```

Install:
```bash
pip3 install -r requirements.txt
```
Run:
```bash
python3 Momus.py
```
Pack to exe:
```
pyinstaller -F -i logo.ico -w Momus.py -p image_processing.py
```
<br/>
Download Release:

[Github](https://github.com/LevyHsu/Momus/releases)<br/>
[levyhsu.com](https://levyhsu.com/uploads/Momus.exe)
<br/>

output file(Under same dir):
```
originalname_output.png
```
Mac version is currently unavailable due to [Issue on tkinte under MacOS 10.14.6](https://discussions.apple.com/thread/250549297)<br/>
****
### Demo:
#### Version: 1.2:
![](Demo/Momus_Demo.gif)
#### Version: 1.4:
![](Demo/Momus_Demo_2.gif)
#### Counter OCR demo:
![](Demo/Merge2.jpg)
![](Demo/Merge.jpg)

