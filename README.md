# Vision-System-For-Robot-Arm-Control

Controls 6-DOF Robot Arm by the camera-based system. Tracks surface movements and adjust the robot's position accordingly.

----
**The camera system** consists of two external cameras (ideally, there should be more) placed on top of the surface (1) and at the bottom on a side (2). This system gives **5-DOF** movement estimations of the surface.

**The tracking algorithm**: a segmentation model (wound segmentation here) to crop ROI, SIFT to extract features from ROI, and FLANN as a feature matcher.

**Used robot**: SEED S6H4D robot arm

**Requirements**: works on **CPU** (tested on: AMD Ryzen 7 5825U | 16 GB RAM)

----
**Demos**: https://drive.google.com/drive/folders/1Gb3p0PHmpOtv9YcD3E61mrooz2xuyRO4?usp=sharing
