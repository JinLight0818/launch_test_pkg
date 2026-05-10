import unittest

import launch
import launch_ros.actions
import launch_testing
import launch_testing.actions
import launch_testing.markers
import pytest

import rclpy
from std_msgs.msg import String


@pytest.mark.launch_test
@launch_testing.markers.keep_alive
def generate_test_description():
    talker_node = launch_ros.actions.Node(
        package='launch_test_pkg',
        executable='talker',
        name='talker',
        output='screen',
    )

    return launch.LaunchDescription([
        talker_node,
        launch_testing.actions.ReadyToTest(),
    ])


class TestTalkerNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        rclpy.init()
        cls.node = rclpy.create_node('test_listener_node')

    @classmethod
    def tearDownClass(cls):
        cls.node.destroy_node()
        rclpy.shutdown()

    def test_talker_publishes(self):
        """Talker нод chatter topic-д мессеж илгээж байгаа эсэхийг шалгах"""
        received_messages = []

        subscription = self.node.create_subscription(
            String,
            'chatter',
            lambda msg: received_messages.append(msg.data),
            10,
        )

        timeout = self.node.get_clock().now() + rclpy.duration.Duration(seconds=10)
        while len(received_messages) < 1:
            rclpy.spin_once(self.node, timeout_sec=0.1)
            if self.node.get_clock().now() > timeout:
                break

        self.node.destroy_subscription(subscription)

        assert len(received_messages) > 0, 'chatter topic-оос мессеж ирсэнгүй'
        assert 'Hello World' in received_messages[0], \
            f"Мессеж 'Hello World' агуулах ёстой, авсан: {received_messages[0]}"

    def test_talker_multiple_messages(self):
        """Олон мессеж ирж байгаа эсэхийг шалгах"""
        received_messages = []

        subscription = self.node.create_subscription(
            String,
            'chatter',
            lambda msg: received_messages.append(msg.data),
            10,
        )

        timeout = self.node.get_clock().now() + rclpy.duration.Duration(seconds=15)
        while len(received_messages) < 3:
            rclpy.spin_once(self.node, timeout_sec=0.1)
            if self.node.get_clock().now() > timeout:
                break

        self.node.destroy_subscription(subscription)

        assert len(received_messages) >= 3, \
            f"Хамгийн багадаа 3 мессеж ирэх ёстой, ирсэн: {len(received_messages)}"
