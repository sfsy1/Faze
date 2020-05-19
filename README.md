#  **Faze**
###  Face & Gaze Detection for Attention Prediction
Shifeng, May 2020
![screenshot](https://raw.githubusercontent.com/sfsy1/Faze/master/pics/overview.png)

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

## Summary of Features
In this version there's only be the essential features.

1. **Face & landmark detections**
    * out of the box cascade detection from OpenCV is used to crop face from the image
    * with the cropped face, key landmarks of the eyes and nose are detected using an OpenCV cascade detector as well
2. **Gaze prediction**
    * Landmarks are used to crop out the left and right eyes. The GazeML model is then used to predict the {pitch,yaw} of the gaze for each eye. https://github.com/swook/GazeML
3. **3D Head location**
    * Using the size of the face, the depth is estimated and the head position is projected into 3D.
4. **Emotion analysis**
    * A CNN classification model is used to predict the emotions present in the detected face. The various emotions are summarized into a single value to measure how positive/negative the emotions are.
5. Putting them together & Visualization
    * With the above inputs {3d head location, gaze directions of each eye}, I plot everything using matplotlib.
    

## References
* Landmark detection & Gaze prediction https://github.com/david-wb/gaze-estimation
* Emotion prediction https://github.com/WuJie1010/Facial-Expression-Recognition.Pytorch
* OpenCV docs https://docs.opencv.org/
* Matplotlib docs https://matplotlib.org/2.1.2/
