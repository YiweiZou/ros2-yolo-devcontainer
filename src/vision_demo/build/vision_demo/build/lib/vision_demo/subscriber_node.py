import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np


class ImageSubscriber(Node):
    def __init__(self):
        # 初始化节点
        super().__init__('image_subscriber')

        # 创建订阅者
        # 监听 /image_raw topic
        self.sub = self.create_subscription(
            Image,
            '/image_raw',
            self.callback,
            10
        )

        self.get_logger().info("Image Subscriber Started")

        # 用于统计帧数
        self.count = 0

    def callback(self, msg):
        # -----------------------------
        # 1. 将 ROS Image 转回 numpy
        # -----------------------------
        # msg.data 是 bytes，需要 decode
        img = np.frombuffer(msg.data, dtype=np.uint8)

        # reshape 成 (H, W, 3)
        img = img.reshape((msg.height, msg.width, 3))

        # -----------------------------
        # 2. 简单“视觉处理”
        # -----------------------------
        # 这里用 mean 模拟“特征提取”
        mean_val = img.mean()

        # -----------------------------
        # 3. 打印结果（模拟 inference 输出）
        # -----------------------------
        self.count += 1

        # 每 10 帧打印一次（避免刷屏）
        if self.count % 10 == 0:
            self.get_logger().info(f"mean pixel value = {mean_val:.2f}")


def main():
    # 初始化 ROS2
    rclpy.init()

    # 创建节点
    node = ImageSubscriber()

    # 进入循环监听 topic
    rclpy.spin(node)

    # 释放资源
    node.destroy_node()
    rclpy.shutdown()