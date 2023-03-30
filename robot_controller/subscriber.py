import rclpy as ros
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import rclpy.qos as q
import time as t

WHEEL_CIRCUMFERENCE = 18.84958
TRACK_WIDTH = 27
TRACK_WIDTH_CIRCUMFERENCE = 84.823
SPEED_FOR_1_DEGREE = WHEEL_CIRCUMFERENCE


class LaserReader(Node):
    def __init__(self):
        super().__init__("laser_subscriber")
        qos_profile = q.QoSProfile(depth=10)
        qos_profile.reliability = q.QoSReliabilityPolicy.BEST_EFFORT
        qos_profile.durability = q.QoSDurabilityPolicy.VOLATILE
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_recieved,
            qos_profile
        )
        self.subscription
        self.thenewyorktimes = self.create_publisher(String,'topic',10)
        self.scan = None
        self.notstarted = True
    def laser_recieved(self,msg):
        self.scan = msg
        minimumIndex = self.scan.ranges.index(self.scan.range_min)
        minimumAngle = self.scan.angle_increment*minimumIndex
        self.get_logger().info(self.scan.range)
        # if self.notstarted:
            # self.drive_loop()
            # self.notstarted = False
    def drive_loop(self):
        minimumIndex = self.scan.ranges.index(self.scan.range_min)
        minimumAngle = self.scan.angle_increment*minimumIndex
        self.get_logger().info(minimumIndex,minimumAngle,self.scan.range_min)
        commands = {
            "A":0,
            "B":0
        }
        # Do some magic
        msg = String()
        msg.data = str(commands["A"])+","+str(commands["B"])
        self.thenewyorktimes.publish(msg)
        t.sleep(1/30)
        self.drive_loop()

        

                

def main(args = None):
    ros.init()
    laser_reader = LaserReader()
    laser_reader.get_logger().info("NODE INITIATED SUCCESSFULLY")
    print(dir(LaserScan))
    laser_reader.get_logger().info("Spinning until program terminated")
    ros.spin(laser_reader)
    laser_reader.destroy_node()
    ros.shutdown()

if __name__ == '__main__':
    main()