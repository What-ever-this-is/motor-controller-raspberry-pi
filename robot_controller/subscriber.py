import rclpy as ros
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import rclpy.qos as q
class LaserReader(Node):
    def __init__(self):
        super().__init__("laser_subscriber")
        qos_profile = q.QoSProfile(depth=10)
        qos_profile.reliability = q.QoSReliabilityPolicy.BEST_EFFORT
        qos_profile.durability = q.QoSDurabilityPolicy.VOLATILE
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            qos_profile
        )
        self.subscription
        self.get_logger().info("DDDDDD")
    def listener_callback(self,msg):
        self.get_logger().info(str(msg.ranges[0]))
def main(args = None):
    ros.init()
    laser_reader = LaserReader()
    laser_reader.get_logger().info("Why does this not work")
    print(dir(LaserScan))
    ros.spin(laser_reader)
    laser_reader.destroy_node()
    ros.shutdown()

if __name__ == '__main__':
    main()