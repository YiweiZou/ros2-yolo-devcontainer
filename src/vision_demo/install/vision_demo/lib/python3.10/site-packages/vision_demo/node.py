import rclpy
from rclpy.node import Node
import cv2


class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.get_logger().info("Vision Node Started")

        self.cap = cv2.VideoCapture(0)

    def run(self):
        while rclpy.ok():
            ret, frame = self.cap.read()
            if not ret:
                continue

            cv2.imshow("camera", frame)
            cv2.waitKey(1)


def main():
    rclpy.init()
    node = VisionNode()
    node.run()
    node.destroy_node()
    rclpy.shutdown()