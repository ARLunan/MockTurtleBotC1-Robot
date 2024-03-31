# MockTurtleBot
MockTurtleBot Project - iRobot© Create1 Base

The requirement of the work in this repository is to document the development and post the release of  packages that migrate the original "Willow Garage" / Open Robotics Turtlebot (tm) where the last released repository was ROS Indigo, to ROS 2 Humble/Navigation 2 autonomous navigation, called "MockTurtleBot" using this orgiginal iRobot Create 1 Base. It should be mentioned that while this repository is written to support a Create 1 base, it should be mentioned that the installed base drive package (Autonomy Labs) includes support for the Roomba (e.g. Model 500 or 600) and Create2 base. To use enable these drivers, a manual revison must be made to the mtbc1_bringup launch file that is installed in the mtbc1_ws workspace, and recompiled.  

**Installation of ROS 2 Packages and Dependancies on the Robot (SBC) and Desktop Computer.** This material references the ROS 2 and dependancies installation documented in the linorobot2 repository *https://github.com/linorobot/linorobot2/blob/humble/ROBOT* , and adds iinstructions specfically for this MockTurtleBotC1 robot model.

**Installation of ROS 2 on Robot (SDB) and Remote Desktop Computer**

This "install" script on the ros2me repository script below will install **ROS 2 humble distro** and a number of python3 libraries and dependancies for the Ubuntu 22.04 Jammy Release meta-package: 

ros-humble-desktop on a "x86_64" machine,  or 

ros-humble-base (barebones) on a "aarch64", i.e Raspberry Pi or MAC M1. 

Note that if your Remote Desktop Machine is an "aarch64" such as a MAC M1, as it installs the -base, you must manually run an additional script "~/sudo apt install ros-humble-desktop to add the necessary packages to upgrade the install to a "Desktop" (e.g. rviz, teleop, joy, rqt)  

While not essential the following Ubuntu packages can be helpful in running and trouble-shotting your Robot & Desktop computers. All install with "~/sudo apt install" openssh-server, avahi-daemon, htop, 

From the Ubuntu home directory, *~/git clone https://github.com/linorobot/ros2me* , then run **~/ ./install**

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

1.1 Create 1 Dependancy from Autonomy Lab at SFU  *https://github.com/AutonomyLab* 

$ sudo apt-get install build-essential cmake libboost-system-dev libboost-thread-dev

$ cd mtbc1_ws/src
$ git clone https://github.com/AutonomyLab/create_robot
$ git checkout humble
$ git clone https://github.com/AutonomyLab/create_robotInstall dependencies

$ cd ~/mtbc1_ws
$ rosdep update
$ rosdep install --from-paths src -i

Build

$ cd ~/create_ws
$ colcon build

USB Permissions
In order to connect to Create over USB, ensure your user is in the dialout group

$ sudo usermod -a -G dialout $USER
Logout and login for permission to take effect

Running the driver
Setup

After compiling from source, don't forget to source your workspace:

$ source ~/mtbc1_ws/install/setup.bash

1.2 **SLAMTECH RPLIDAR** ):
Installed from binaries provided by the manufacturer, SLAMTECH: https://github.com/Slamtec/rplidar_ros.tree/ros2

$ sudo sudo apt install rplidar_ros
This installs the necessary packages to run the device and configure udev rules with a persistant USB name: rplidar . 

1.3 **OAK-D Camera:**
sudo apt install ros-humble-depthai-ros
The camera function is to display publish a color rgb image to view with the ros 2 utility: $ ros2 run rqt_image view rqt_image_view or in rviz.

2. Download **MockTurtleBotC1** and its dependencies:

2.1 Download MockTurtleBotC1:

cd mtbc1_ws
git clone -b  https://github.com/MockTurtleBotC1/mtbc1 src/mtcbc1

cd ~/mtbc1_ws
rosdep update && rosdep install --from-path src --
colcon build
source install/setup.bash

3. Save changes
Source your ~/.bashrc to apply the changes you made:

$ source ~/.bashrc

**Install USB udev rules** for the Create 1 Base and RPLidar to assign persistant names for these two serial ports, name. create1 and rplidar.

4. **Host Machine / Development Computer - RVIZ Configurations**



