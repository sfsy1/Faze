#  **Faze**
###  Face & Gaze Detection for Attention Prediction
Shifeng, May 2020
![screenshot](https://raw.githubusercontent.com/sfsy1/Faze/master/images/overview.jpg)


## Requirements
* python >=3.5
* jupyter (lab/notebook) https://jupyter.org/install
* run `pip install requirements.txt` to install specific python packages
* have a webcam located at the center-top of your monitor, facing in the same direction as the screen
* make sure your face is well-lit & large eyes are strongly preferred
* a CUDA-enabled GPU is recommended for high frame-rate

*Calibration of camera/monitor might be slightly off but the visualization should still work conceptually*


## Running
* Just open `gaze_detector.ipynb` in jupyter and follow the run the codes inside


## Summary
![screenshot](https://raw.githubusercontent.com/sfsy1/Faze/master/images/workflow.jpg)


## Features
1. **Face & landmark detections**
    * out of the box cascade detection from OpenCV is used to crop face from the image
    * with the cropped face, key landmarks of the eyes and nose are detected using an OpenCV cascade detector as well
2. **Gaze prediction**
    * Landmarks are used to crop out the left and right eyes. The GazeML model, using VGG-16 as the backbone, is then used to predict the {pitch,yaw} of the gaze for each eye. https://github.com/swook/GazeML
3. **3D Head location**
    * Using the size of the face, the depth is estimated and the head position is projected into 3D.
4. **Emotion analysis**
    * A stacked hourglass CNN classification model is used to predict the emotions present in the detected face. The various emotions are summarized into a single value to measure how positive/negative the emotions are.
5. **Putting them together & Visualization**
    * With the above inputs {3d head location, gaze directions of each eye}, I plot everything using matplotlib.

## Possible Applications & Add-Ons
* **Applications**
  * Productivity tracking
    * break reminders if your emotions are negative while staring at the screen.
    * general productivity measure
  * Content control
    * block adult content if a child is looking at the screen
    * monitor content of screen if sudden onset of emotions?
  * Accessiblity features
    * auto-zoom into regions of gaze, if squinting is detected
    * eye cursor controls
  * Security
    * check for gazes in the background
* **Improvements**
    * Model compression, optmization and training on more diverse datasets
    * Combine all 3 tasks into a single CNN?
    * Use tracking instead of detectinge every frame

## References
* Landmark detection & Gaze prediction https://github.com/david-wb/gaze-estimation
* Emotion prediction https://github.com/WuJie1010/Facial-Expression-Recognition.Pytorch
* OpenCV docs https://docs.opencv.org/
* Matplotlib docs https://matplotlib.org/2.1.2/
* Sample pictures from some of my favorite movies: Donnie Darko (2001), Amélie (2001), Lilya 4-ever (2002)
