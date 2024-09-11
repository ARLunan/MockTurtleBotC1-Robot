#  Revised for bringup.launch.py package mtcb1_bringup package by ARLunan August 2024
#  Copyright (c) 2021 Juan Miguel Jimeno
#
# Licensed under the Apache License, Version 2.0
# you may not use this file except in compliance with the License. (the "License");
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():

    sensors_launch_path = PathJoinSubstitution(
        [FindPackageShare('mtbc1_bringup'), 'launch', 'sensors.launch.py']
    )
    
    joy_launch_path = PathJoinSubstitution(
        [FindPackageShare('mtbc1_bringup'), 'launch', 'joy_teleop.launch.py']
    )
    
    description_launch_path = PathJoinSubstitution(
        [FindPackageShare('mtbc1_description'), 'launch', 'description.launch.py']
    )
    
    ekf_config_path = PathJoinSubstitution(
        [FindPackageShare("mtbc1_base"), "config", "ekf.yaml"]
    )

    default_robot_launch_path = PathJoinSubstitution(
        [FindPackageShare('mtbc1_bringup'), 'launch', 'default_robot.launch.py']
    )
        
    return LaunchDescription([ 
        DeclareLaunchArgument(
        name='joy', 
        default_value='false',
        description='Use Joystick'
    ),  

    DeclareLaunchArgument(
        name='odom_topic', 
        default_value='/odom',
        description='EKF out odometry topic'
    ),    
    
    DeclareLaunchArgument(
        name='madgwick',
        default_value='false',
        description='Use madgwick to fuse imu and magnetometer'
    ),

    DeclareLaunchArgument(
        name='orientation_stddev',
        default_value='0.003162278',
        description='Madgwick orientation stddev'
    ),

    DeclareLaunchArgument(
        name='joy', 
        default_value='false',
        description='Use Joystick'
    ),
    
    Node(
        condition=IfCondition(LaunchConfiguration("madgwick")),
        package='imu_filter_madgwick',
        executable='imu_filter_madgwick_node',
        name='madgwick_filter_node',
        output='screen',
        parameters=[
            {'orientation_stddev' : LaunchConfiguration('orientation_stddev')}
        ]
    ),

    Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[
            ekf_config_path
        ],
        remappings=[("odometry/filtered", LaunchConfiguration("odom_topic"))]
    ),

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(joy_launch_path)                         
    ),

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(default_robot_launch_path)                         
    )

])