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

    joy_launch_path = PathJoinSubstitution(
        [FindPackageShare('mtbc1_bringup'), 'launch', 'joy_teleop.launch.py']
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

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(joy_launch_path)                         
    ),

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource(default_robot_launch_path)                         
    )


])