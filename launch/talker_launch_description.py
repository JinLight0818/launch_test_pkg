import launch
from launch_ros.actions import Node


def generate_launch_description():
    return launch.LaunchDescription([
        Node(
            package='launch_test_pkg',
            executable='talker',
            name='talker',
            output='screen',
        ),
    ])
