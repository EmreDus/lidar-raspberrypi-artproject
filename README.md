# Lidar-Enabled Interactive Art Project

This GitHub repository showcases an exciting interactive art project that utilizes Raspberry Pi and Lidar technology. The project features a specially designed mirror intended for display in an art gallery, which responds to the visitors' interactions.

The main objective of this project is to detect individuals approaching the mirror using a Lidar sensor and manipulate the mirror's movement to create an interactive experience. The sensor continuously scans the positions of people in front of the mirror, and based on calculations performed on the detected individuals, determines the direction and extent of mirror rotation.

One notable aspect of this interactive art project is its unique feature. If the first person approaching the mirror encounters another person directly across from them, the mirror remains parallel to the two individuals. This creates intriguing reflections for the visitors to observe.

In addition to mirror rotation and stabilization, the project also controls music and lighting elements. A Programmable Logic Controller (PLC) is utilized for these operations. Raspberry Pi transfers the calculated stopping angle of the mirror to the PLC via Modbus, which then stops the servo motor at the desired angle to stabilize the mirror. Furthermore, Raspberry Pi handles the control of other interactive components such as music and lighting.





#!/bin/bash

git clone https://github.com/EmreDus/lidar-vol2.git
cd lidar-vol2
sudo chmod +x install.sh
./install.sh
