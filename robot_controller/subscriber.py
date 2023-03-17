import rclpy as ros
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
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
        self.thenewyorktimes = self.create_publisher(
            String,
            '/motorcommands',
            10
        )
        self.subscription
        self.get_logger().info("DDDDDD")
    def listener_callback(self,msg):
        calculatedSpeed = calculateMotorSpeed(msg)
        self.thenewyorktimes.publish(calculatedSpeed)

def calculateMotorSpeed(scan):
    myMotorSpeed = {
        "A":1,
        "B":1
    }

    # Some random codes

    exportMotorSpeed = str(myMotorSpeed["Speed"])+" "+str(myMotorSpeed["Steer"])
    
    return exportMotorSpeed
    

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