# Ball Tracker and Localizer using 2-DOF Camera

In this project, I implemented a vision-based tracker and localizer using a 2-DOF camera. A python application detect a green ball on screen and calculate its center in image coordination using open-cv library. Then, a 2-DOF platform with two servo motors run by Arduino UNO tries to put the center of the ball at the center of the screen. After that, a geometry-based localization method calculates the localization of the ball.

##Acknowledgement


## Hardware
In this project, a 640x480 USB camera is installed on a 2-DOF platform running by two low-cost servo motors (MG90s), a USB UART converter, and an Arduino UNO command the servo motors. The hardware setup is shown at following figure. ![figure1](https://dl.dropboxusercontent.com/s/oytsbia24klduvq/Hardware03.jpg?dl=0)

## Prerequisites
For running this project you will need Arduino and python compiler with open-cv and numpy packages, alongside with the above-mentioned hardware.

## Detection
Thanks to Adrian Rosebrock (from [pyimagesearch](https://www.pyimagesearch.com/)) and [Practical-CV](https://github.com/Practical-CV/Color-Based-Ball-Tracking-With-OpenCV) for tutorials and detection code.
The detection is performed based on the color of the ball. Indeed, the detection algorithm detects the green color. I use the center of detected ball for computing the error and command the servo motor to put the ball at the center of the picture. 

## Localization
The localization is performed based on a geometrical method, depicted in the following figure. ![figure2](https://dl.dropboxusercontent.com/s/g6dgh6saj3pjp15/CameraCoordinate01.png?dl=0)

<img align="center" width="234" height="180" src="https://dl.dropboxusercontent.com/s/tblysaoj9mwq775/Equation.JPG?dl=0">

## Results
The output of Python applicaion is shown in following figure.
![figure_Result](https://dl.dropboxusercontent.com/s/mwohe7z5bbnxhu6/Result01.jpg?dl=0)


