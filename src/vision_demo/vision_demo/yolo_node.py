import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import torch
from ultralytics import YOLO


class YOLONode(Node):
    def __init__(self):
        super().__init__('yolo_node')

        # 订阅输入图像
        self.sub = self.create_subscription(
            Image,
            '/image_raw',
            self.callback,
            10
        )

        # 发布检测结果图像
        self.pub = self.create_publisher(Image, '/image_yolo', 10)

        self.bridge = CvBridge()

        # =========================
        # YOLO模型（最小版本）
        # =========================
        self.model = YOLO("yolov8n.pt")

        self.device = 0 if torch.cuda.is_available() else "cpu"

        self.get_logger().info(f"YOLO started on {self.device}")

    def callback(self, msg):
        # ROS → OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        # =========================
        # YOLO 推理
        # =========================
        results = self.model.predict(
            source=frame,
            device=self.device,
            verbose=False
        )

        # 带框图像
        annotated = results[0].plot()

        # OpenCV → ROS
        out_msg = self.bridge.cv2_to_imgmsg(annotated, encoding="bgr8")
        out_msg.header = msg.header

        self.pub.publish(out_msg)


def main():
    rclpy.init()
    node = YOLONode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()