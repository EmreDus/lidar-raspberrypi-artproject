# Lidar-Enabled Interactive Art Project

This repository showcases an exciting interactive art project that utilizes Raspberry Pi and Lidar technology. The project features a specially designed mirror intended for display in an art gallery, which responds to the visitors' interactions.

## Project Overview

The main objective of this project is to detect individuals approaching the mirror using a Lidar sensor and manipulate the mirror's movement to create an interactive experience. The sensor continuously scans the positions of people in front of the mirror, and based on calculations performed on the detected individuals, determines the direction and extent of mirror rotation.

One notable aspect of this interactive art project is its unique feature. If the first person approaching the mirror encounters another person directly across from them, the mirror remains parallel to the two individuals. This creates intriguing reflections for the visitors to observe.

In addition to mirror rotation and stabilization, the project also controls music and lighting elements. A Programmable Logic Controller (PLC) is utilized for these operations. Raspberry Pi transfers the calculated stopping angle of the mirror to the PLC via Modbus, which then stops the servo motor at the desired angle to stabilize the mirror. Furthermore, Raspberry Pi handles the control of other interactive components such as music and lighting.

## Repository Contents

This repository contains the Raspberry Pi source code developed for the project. The code is written to process data from the Lidar sensor, calculate mirror movement, establish Modbus communication, and control other interactive elements. Additionally, necessary documentation and explanations are provided to assist other developers and art enthusiasts in understanding the project.

## Getting Started

1. git clone https://github.com/EmreDus/lidar-raspberrypi-artproject.git
2. cd lidar-raspberrypi-artproject
3. sudo chmod +x install.sh
4. ./install.sh

