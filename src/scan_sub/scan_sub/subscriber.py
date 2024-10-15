import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

class LaserScanSubscriber(Node):
    def __init__(self):
        super().__init__('laser_scan_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_scan_callback,
            10
        )
        self.publisher_ = self.create_publisher(Bool, 'obstacle_detected', 10)
        //閾値30cm
        self.threshold = 0.3
        self.get_logger().info('LaserScanSubscriber has been started.')

    def laser_scan_callback(self, msg):
        min_range = min(msg.ranges)

        if min_range < self.threshold:
            obstacle_detected = True
        else:
            obstacle_detected = False

        msg_bool = Bool()
        msg_bool.data = obstacle_detected
        self.publisher_.publish(msg_bool)
        self.get_logger().info(f'Obstacle detected: {obstacle_detected} (min range: {min_range:.2f})')

def main(args=None):
    rclpy.init(args=args)
    node = LaserScanSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
