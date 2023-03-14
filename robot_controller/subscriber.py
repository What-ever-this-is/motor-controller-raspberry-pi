import rclpy as ros
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LaserReader(Node):
    def __init__(self):
        super().__init__("laser_subscriber")
        self.subscription = self.create_subscription(
            LaserScan,
            'topic'.
            self.listener_callback,
            10
        )
        self.subscription
    def listener_callback(self,msg):
        self.get_logger().info("AAAAAAA")
def main(args=None):
    ros.init(args=args)
    print(dir(LaserScan))
    laser_reader = LaserReader()
    ros.spin(laser_reader)
    laser_reader.destroy_node()
    ros.shutdown()

if __name__ == '__main__':
    main()