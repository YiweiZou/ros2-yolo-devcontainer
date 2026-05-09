import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')

        self.sub = self.create_subscription(
            Image,
            '/image_raw',
            self.callback,
            10
        )

        self.bridge = CvBridge()
        self.window_name = "ROS2 Image Viewer"

        # 🔥 强制创建窗口（避免多个窗口残留）
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

        self.running = True

        self.get_logger().info("Subscriber Started (press q to quit)")

    def callback(self, msg):
        if not self.running:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        cv2.imshow(self.window_name, frame)

        key = cv2.waitKey(1) & 0xFF

        # =========================
        # 🔥 关键退出逻辑
        # =========================
        if key == ord('q'):
            self.get_logger().info("Quit requested")

            self.running = False
            rclpy.shutdown()

            cv2.destroyAllWindows()


def main():
    rclpy.init()
    node = ImageSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

    # 🔥 双保险
    cv2.destroyAllWindows()