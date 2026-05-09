import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np


class ImagePublisher(Node):
    def __init__(self):
        # 初始化 ROS2 节点，名字叫 image_publisher
        super().__init__('image_publisher')

        # 创建一个 publisher
        # topic 名字：/image_raw
        # 消息类型：Image（标准 ROS2 图像消息）
        self.pub = self.create_publisher(Image, '/image_raw', 10)

        # 创建定时器：每 0.1 秒触发一次 callback
        # 相当于模拟“相机 10Hz 帧率”
        self.timer = self.create_timer(0.1, self.callback)

        # 帧计数器
        self.counter = 0

        self.get_logger().info("Image Publisher Started")

    def callback(self):
        # -----------------------------
        # 1. 生成 fake image（模拟相机图像）
        # -----------------------------
        # shape: 64x64 RGB 图像
        # 每一帧用不同灰度值模拟变化
        img = np.ones((64, 64, 3), dtype=np.uint8) * (self.counter % 255)

        # -----------------------------
        # 2. 构造 ROS2 Image message
        # -----------------------------
        msg = Image()

        # 时间戳（用于同步不同传感器）
        msg.header.stamp = self.get_clock().now().to_msg()

        # frame_id（类似 camera 坐标系）
        msg.header.frame_id = "camera"

        # 图像基本信息
        msg.height = 64
        msg.width = 64

        # 图像编码格式（RGB）
        msg.encoding = "bgr8"

        # 每一行字节数
        msg.step = 64 * 3

        # 将 numpy 图像转为 bytes（ROS底层传输格式）
        msg.data = img.tobytes()

        # -----------------------------
        # 3. 发布消息
        # -----------------------------
        self.pub.publish(msg)

        self.get_logger().info(f"publish frame {self.counter}")

        self.counter += 1


def main():
    # 初始化 ROS2 Python client
    rclpy.init()

    # 创建节点
    node = ImagePublisher()

    # 进入循环（持续运行 callback）
    rclpy.spin(node)

    # 释放资源
    node.destroy_node()
    rclpy.shutdown()