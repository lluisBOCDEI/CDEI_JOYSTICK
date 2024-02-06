from launch import LaunchDescription
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    #joy_params = os.path.join(get_package_share_directory('AGRO_joy_proc'),'config','joystick.yaml')

    joy_node = Node(
        package='joy',
        executable='joy_node',
        #name='joy_node',
        #parameters=[joy_params],
    )

    gui_joy = Node(
        package='joy_tester',
        executable='test_joy',
    )

    consignes_joystick = Node(
        package='AGRO_joystick',
        executable= 'consignes_joystick',
    )

    return LaunchDescription([joy_node,gui_joy,consignes_joystick])