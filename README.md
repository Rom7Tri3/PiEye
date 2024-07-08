## PiEye
# Introduction
This project aims to implement face recognition using Raspberry Pi devices, with a dedicated Raspberry Pi to display the results. We are using three Raspberry Pi 5 8GB models, named PiEyeA, PiEyeB, and PiBrain. Initially, we planned to use the Pi Zero 2W, but they proved too slow for our purposes, necessitating the switch to the more powerful models.

PiEyeA and PiEyeB are equipped with Zero Cam Noir cameras to capture faces. The Zero Cam Noir is a standard camera without infrared sensors, as IR capabilities were not needed for our purposes.

The setup consists of two Raspberry Pi devices (PiEyeA and PiEyeB) with cameras, connected to each other and constantly communicating with PiBrain, which displays the results. Since PiEyeA and PiEyeB are interconnected, there should be no conflicting results. It is important to note that this project will only be used in private settings and will not infringe on individuals’ privacy.
