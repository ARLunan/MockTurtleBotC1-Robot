# MockTurtleBot
MockTurtleBot Project - iRobot© Create1/Roomba 500 Base

The requirement of the work in this repository is to document the development and post the release of  ROS 2 Packages that migrate the original "Willow Garage" / Open Robotics Turtlebot (tm) where the last released repository was ROS Indigo, to ROS 2 Humble/Navigation 2 autonomous navigation'. This new repository called "MockTurtleBot" uses this orgiginal iRobot Create (™) 1 Base. It should be mentioned that while this repository is written to use with a iRobot Create 1, the installed base drive package (Autonomy Labs ™) includes support for the Roomba Model 500 or 600) and Create 2 base. To enable these drivers, a manual revison must be made to the mtbc1_bringup launch file that is installed in the mtbc1_ws workspace, and recompiled.  

**Installation of ROS 2 Packages and Dependancies on the Robot (Raspberry Pi Single Board Computer-SBC) and Desktop Computer.** This Repository material references the ROS 2 and dependencies installation documented in the linorobot2 repository *https://github.com/linorobot/linorobot2/blob/humble/ROBOT* , and adds instructions specfically for this MockTurtleBotC1 robot model.

**Installation of ROS 2 on Robot (Rasberry Pi Single Board Computer - SBC) and Remote Desktop Computer**

This "install" script on the ros2me repository script below will install **ROS 2 humble distro** and a number of python3 libraries and dependancies for the Ubuntu 22.04 Jammy Release meta-package: 

ros-humble-desktop on a "x86_64" machine,  or 

ros-humble-base (barebones) on a "aarch64", i.e Raspberry Pi or MAC M1. 

Note that if your Remote Desktop Machine is an "aarch64" such as a MAC M1, as it installs the -base, you must manually run an additional script "~/sudo apt install ros-humble-desktop to add the necessary packages to upgrade the install to a "Desktop" (e.g. rviz, teleop, joy, rqt)  

While not essential the following Ubuntu packages can be helpful in running and trouble-shotting your Robot & Desktop computers. Install these ubuntu packages with with "~/sudo apt install" openssh-server, avahi-daemon, htop, nload . 

From the Ubuntu home directory, *~/git clone https://github.com/linorobot/ros2me* , then run **~/ .install**

**Manual installation of MockTurtleBotC1**, which is a Create 1 varient of the MockTurtleBot robot package on ***robot*** **(SBC)** computer. 

1. Install dependencies

1.1 Source your ROS 2 distro, which is **humble** in this documentation and workspace
source /opt/ros/humble/setup.bash
cd mtbc1_ws
colcon build
source install/setup.bash

add this script to the ~/.bashrc in your home directory to make this designation persistant for any terminal instance

$ export "source /opt/ros/humble/setup.bash"

The <your_ws> workspace is designated as **mtbc1_ws/src**, or whatever you desire to use.

$ sudo apt-get install build-essential cmake libboost-system-dev libboost-thread-dev

1.2 Configure .gitignore in root directory of Remote Desktop and Robot SBC (Single Board Computer)
Suggest use the sample file ROS.gitignore file from [https://github.com/github/gitignore]() . Suggest using the ROS.gitignore file and add these several additional lines if VSCode is deployed on the Desktop and Robot machines and you use Git.

\# VSCode   
/.vscode/  
**/.vscode/  
log/  
build/  
install/   

\# .gitignore  
/.gitignore

\# .DS_Store  
.DS_Store



