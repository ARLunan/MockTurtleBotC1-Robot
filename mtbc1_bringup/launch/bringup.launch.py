# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
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

    '''
    default_robot_launch_path = PathJoinSubstitution(
        [FindPackageShare('mtbc1_bringup'), 'launch', 'default_robot.launch.py']
    ) 
    '''
    default_robot_launch_path = PathJoinSubstitution(
        [FindPackageShare('create_bringup'), 'launch', 'create_1.launch.py']
    )

    return LaunchDescription([

    DeclareLaunchArgument(
        name='base_serial_port', 
        default_value='/create1',
        description='Mtbc1 Base Serial Port',
    ),

    DeclareLaunchArgument(
        name='odom_topic', 
        default_value='/odom',
        description='EKF out odometry topic'
    ),
    
    DeclareLaunchArgument(
        name='joy', 
        default_value='false',
        description='Use Joystick'
    ),            

    DeclareLaunchArgument(
        name='imn', 
        default_value='true',
        description='Enable IMU'
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
        PythonLaunchDescriptionSource(default_robot_launch_path),
        launch_arguments={
            'base_serial_port': LaunchConfiguration("base_serial_port")
        }.items()
    )
    
])