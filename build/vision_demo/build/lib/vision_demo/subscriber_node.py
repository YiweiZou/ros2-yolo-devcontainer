import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# 🔥 ROS ↔ OpenCV 转换工具
from cv_bridge import CvBridge

import cv2


class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')

        # 订阅图像 topic
        self.sub = self.create_subscription(
            Image,
            '/image_raw',
            self.callback,
            10
        )

        # cv_bridge 初始化
        self.bridge = CvBridge()

        self.get_logger().info("OpenCV Subscriber Started")

    def callback(self, msg):
        # =========================
        # 1. ROS Image → OpenCV
        # =========================
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # =========================
        # 2. 简单处理（验证数据流）
        # =========================
        h, w, _ = frame.shape

        cv2.putText(
            frame,
            f"{w}x{h}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # =========================
        # 3. 显示窗口
        # =========================
        cv2.imshow("ROS2 Image Viewer", frame)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = ImageSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

    cv2.destroyAllWindows()