# Vision-System-For-Robot-Arm-Control

Controls 6-DOF Robot Arm by the camera-based system. Tracks surface movements and adjust the robot's position accordingly.

----
**The camera system** consists of two external cameras (ideally, there should be more) placed on top of the surface (1) and at the bottom on a side (2). This system gives **5-DOF** movement estimations of the surface.

**Tracking algorithm**: a segmentation model (wound segmentation here) to crop ROI, SIFT to extract features from ROI, and FLANN as a feature matcher.

**Used robot**: SEED S6H4D robot arm

**Requirements**: works on **CPU** (tested on: AMD Ryzen 7 5825U | 16 GB RAM)

----
**Demos**: https://drive.google.com/drive/folders/1Gb3p0PHmpOtv9YcD3E61mrooz2xuyRO4?usp=sharing

----
To **run** the program:
`python3 main.py`

----
To **reconfigure** the system update variables in _/config/*_: 
* _camera.py_: cameras' ID, frame properties, calibration coefficients
* _model.py_: used model, threshold, post-processing
* _robot.py_: connection to a robot, home position, used speed 
* _tracker.py_: feature extraction and matching algorithms, matcher threshold, approximation function

Specific to the [SEED](https://seedrobotarm.com/wp-content/uploads/2024/04/Seed_S6H4D_plus-Manual_2023EN.pdf) robot arm a communication protocol: _/helpers/communication.py_.

A wound segmentation model in _/model/_.

If you have more/fewer cameras, change the number of threads in _main.py_.
