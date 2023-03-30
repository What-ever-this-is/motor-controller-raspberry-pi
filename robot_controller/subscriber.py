import rclpy as ros
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import rclpy.qos as q
import RPi.GPIO as g
import time as t

WHEEL_CIRCUMFERENCE = 18.84958
TRACK_WIDTH = 27
TRACK_WIDTH_CIRCUMFERENCE = 84.823
SPEED_FOR_1_DEGREE = WHEEL_CIRCUMFERENCE


class LaserReader(Node):
    def __init__(self,v1,v2,in1,in2,in3,in4,e1a,e1b,e2a,e2b):
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
        self.scan = None
        self.pins = {
            "v1":v1,
            "v2":v2,
            "in1":in1,
            "in2":in2,
            "in3":in3,
            "in4":in4,
            "e1a":e1a,
            "e1b":e1b,
            "e2a":e2a,
            "e2b":e2b,
        }
        g.setmode(g.BOARD)
        g.setup(e1a,g.IN)
        g.setup(e1b,g.IN)
        g.setup(e2a,g.IN)
        g.setup(e2b,g.IN)
        g.setup(v1,g.OUT)
        g.setup(v2,g.OUT)
        g.setup(in1,g.OUT)
        g.setup(in2,g.OUT)
        g.setup(in3,g.OUT)
        g.setup(in4,g.OUT)
        self.notstarted = True
    def laser_recieved(self,msg):
        self.scan = msg
        if self.notstarted:
            self.drive_loop()
            self.notstarted = False
    def drive_loop(self):
        minimumIndex = self.scan.ranges.index(self.scan.range_min)
        minimumAngle = self.scan.angle_increment*minimumIndex
        self.get_logger().info(minimumIndex,minimumAngle,self.scan.range_min)
        t.sleep(1/30)
        self.drive_loop()

        

                

def main(args = None):
    ros.init()
    laser_reader = LaserReader(7,11,12,13,15,16,18,22,29,31)
    laser_reader.get_logger().info("NODE INITIATED SUCCESSFULLY")
    print(dir(LaserScan))
    ros.spin(laser_reader)
    laser_reader.destroy_node()
    ros.shutdown()

if __name__ == '__main__':
    main()