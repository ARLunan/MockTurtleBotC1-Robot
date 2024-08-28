# This launch mtbc1_description.launch.py file was used as a toolchain to develop the Robot xacro 
# Revised by AR Lunan derived from navigation2_tutorials/sambot_description (that has a with jsp gui)
# for use in MockTurtleBot Robot. Environment value not necessary
# Descrpton Package name is mtbc1_description 
# It uses model=mtbc1.urdf.xacro which combines xacros from turtlebot, turtlebot4, autonomylabs create_1
# launches rviz=urdf.config.rviz 
# Note that this launch file/rviz combination does not properly display the create_1 base visual with jsp gui disabled (gui:=false)
# The deployed MockTurtleBotC1 Robot uses the launch file linorobot2/description.launch.py file (that has no jsp gui)
# with this model=mtbc1.urdf.xacro, rviz=urdf_config.rviz from linorobot2 that properly displays the create_1 base image.

import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='mtbc1_description').find('mtbc1_description')
    #default_model_path = os.path.join(pkg_share, 'src/description/mtbc1_description.urdf')
    default_model_path = os.path.join(pkg_share, 'urdf/mtbc1.urdf.xacro')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf.config.rviz')
    
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        arguments=[default_model_path],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )
    
    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                            description='Flag to enable joint_state_publisher_gui'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ])
