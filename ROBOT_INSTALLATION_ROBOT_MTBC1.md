## Manual installation of MockTurtleBotC1-Robot packages on Robot computer
### Refer to separate Manual Installation of MockTurtleBotC1-Desktop on Desktop computer 

### Note: This Procedure installs all base, bringup, description and navigation packages   on the Robot Computer (RaspBerry Pi) that does not necessarily require a connected monitor, though any robot, SLAM & Nav Visualization functions should be done on the Desktop Computer.      

### 1. Install specfic functional Packages from ROS 2 and MockTurtleBotC1-ROBOT Github Repository into the workspace. e.g. mtbc1_ws

#### 1.1 Install and Source your ROS2 distro and workspace
If it's your first time using ROS 2 and haven't created your ROS2 workspace yet, you can check out 
[ROS2 Creating a Workspace](https://docs.ros.org/en/galactic/Tutorials/Workspace/Creating-A-Workspace.html) tutorial. 
The MockTurtleBotC1 code supports ros-distro  = **humble** currently.

    From a Linux Terminal
    sudo apt install ros-humble-joy-linux
    sudo apt install ros-humble-teleop-twist-joy 
    
    source /opt/ros/humble/setup.bash
    
#### 1.2 Install LIDAR ROS2 drivers:

RPLIDAR:

    sudo apt install -y ros-$ROS_DISTRO-rplidar-ros
    Note that this install configures USB udev rules  into /usr/udev/rules.d directory  
   
#### 1.3 Install depth sensor drivers and rgd color camera:

OAK-D Lite Camera:

    sudo apt install ros-$ROS_DISTRO-depthai-ros
    
#### 1.4 Install Create Base Library and driver:

    mkdir -p /mtbc1_ws
    cd create_ws
    git clone -b $ROS_DISTRO https://github.com/ARLunan/autonomy_labs_create_robot.git
    sudo apt update && rosdep update
    rosdep install --from-path src --ignore-src -y
    colcon build
    source install/setup.bash
   
#### 1.5 Configure Serial USB Permissions and Install USB Serial Port udev Rules

USB Permissions
In order to connect to Create over USB, ensure your user is in the dialout group

$ sudo usermod -a -G dialout $USER
Logout and login for permission to take effect

**Install USB udev rules**
With Create 1 Base and RPLidar USB serail connection, it is essential that Linux Device manager interface to assign persistant names for these two serial ports, name. create1 and rplidar.

**Create1**: The udev file *50-create.rule*s is included in the repository mtbc1_bringup/scripts folder 

SUBSYSTEM=="tty", ATTRS{idVendor}=="0403" ATTRS{idProduct}=="6001", MODE:-"0666', SYMLINK+="create1"

In linux terminal, navigate to the mtbc1_bringup/scripts folder and manually execute the following commands:
$ sudo cp 50-create.rules /etc/udev/rules.d
$ sudo service udev reload
$ sudo service udev restart
$ sudo udevadm control --reload && sudo udevadm trigger

**RPLidar**: As this package is installed from Binary, the udev file is located in the system rules directories, /usr/lib/udev/rules.d and /usr/udev/rules.d

To verify the correct functioning of the udev rules, rom a terminal running the following command should list the MockTurtlebotC1 USB serial ports with assigned names:x ports:

ubuntu@rp4-ub22h-mt:~$ ls -l /dev/ |grep USB

lrwxrwxrwx  1 root   root           7 Mar  5 14:02 create1 -> ttyUSB0

lrwxrwxrwx  1 root   root           7 Mar  5 14:02 rplidar -> ttyUSB1

crw-rw-rw-  1 root   dialout 188,   0 Mar  5 14:02 ttyUSB0

crw-rw-rw-  1 root   dialout 188,   1 Mar  5 14:02 ttyUSB1  


#### 1.6 Configure ENV Variables
### 1. Robot Type
Set LINOROBOT2_BASE env variable to the type of robot base that you want to use. This is not required if you're using a custom URDF. The MockTurtleBotC1 is a *2wd*. For example:

    echo "export LINOROBOT2_BASE=2wd" >> ~/.bashrc

Tested sensors are:
*oakdlite* - For example: https://shop.luxonis.com/collections/oak-cameras-1/products/oak-d-lite-1?variant=42583102456031

    echo "export LINOROBOT2_DEPTH_SENSOR=oakdlite" >> ~/.bashrc

#### 2.2 Laser Sensor
The launch files of the tested laser sensors have already been added in bringup.launch.py. You can enable one of these sensors by exporting the laser sensor you're using to `LINOROBOT2_LASER_SENSOR` env variable.

Tested Laser Sensors:
*rplidar* - [RP LIDAR A1](https://www.slamtec.com/en/Lidar/A1)

    echo "export LINOROBOT2_LASER_SENSOR=rplidar" >> ~/.bashrc
    
   If you export a depth sensor to `LINOROBOT2_LASER_SENSOR`, the launch file will run [depthimage_to_laserscan](https://github.com/ros-perception/depthimage_to_laserscan) to convert the depth sensor's depth image to laser.

### 3. Save changes
Source your `~/.bashrc` to apply the changes you made:

    source ~/.bashrc

## Miscellaneous

### 2. Running a launch file during boot-up.

This is a short tutorial on how to make your bringup launch files run during startup.

### 2.1 Create your env.sh

    sudo touch /etc/ros/env.sh
    sudo nano /etc/ros/env.sh 

and paste the following:

    #!/bin/sh

    export LINOROBOT2_BASE=<your_robot_type>
    export LINOROBOT2_LASER_SENSOR=<your_supported_sensor> #(optional)

### 2.2 Create systemd service

    sudo touch /etc/systemd/system/robot-boot.service
    sudo nano  /etc/systemd/system/robot-boot.service

and paste the following:

    [Unit]
    After=NetworkManager.service time-sync.target

    [Service]
    Type=simple
    User=<user>
    ExecStart=/bin/sh -c ". /opt/ros/<your_ros_distro>/setup.sh;. /etc/ros/env.sh;. /home/<user>/<your_ws>/install/setup.sh; ros2 launch linorobot2_bringup bringup.launch.py joy:=true"

    [Install]
    WantedBy=multi-user.target

Remember to replace:
- `user` with your machine's user name (`echo $USER`)
- `your_ros_distro` with the ros2 distro (`echo $ROS_DISTRO`) your machine is running on
- `your_ws` with the location of the ros2 ws where you installed linorobot2

### 2.3 Enable the service

    sudo systemctl enable robot-boot.service

You can check if the service you just created is correct by:

    sudo systemctl start robot-boot.service
    sudo systemctl status robot-boot.service

* You should see the ros2 logs that you usually see when running bringup.launch.py. Once successful, you can now reboot your machine. bringup.launch.py should start running once the machine finished booting up.

### 2.4 Removing the service

    systemctl stop robot-boot.service
    systemctl disable robot-boot.service
    sudo rm /etc/systemd/system/robot-boot.service


Source: https://blog.roverrobotics.com/how-to-run-ros-on-startup-bootup/
