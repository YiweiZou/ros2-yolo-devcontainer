import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np


class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')

        self.pub = self.create_publisher(Image, '/image_raw', 10)
        self.timer = self.create_timer(0.1, self.callback)

        self.counter = 0
        self.get_logger().info("Image Publisher Started")

    def callback(self):
        # =========================
        # 1. generate image
        # =========================
        img = np.zeros((64, 64, 3), dtype=np.uint8)

        # 做一个变化图案（方便观察）
        img[:] = (self.counter % 255, 50, 100)

        # =========================
        # 2. ROS message
        # =========================
        msg = Image()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera"

        msg.height = img.shape[0]
        msg.width = img.shape[1]

        # ⚠️ 必须和 OpenCV一致
        msg.encoding = "bgr8"
        msg.step = msg.width * 3

        msg.data = img.tobytes()

        # =========================
        # 3. publish
        # =========================
        self.pub.publish(msg)

        self.get_logger().info(f"publish frame {self.counter}")

        self.counter += 1


def main():
    rclpy.init()
    node = ImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()