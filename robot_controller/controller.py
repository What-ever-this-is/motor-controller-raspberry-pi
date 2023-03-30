import rclpy as ros
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as g

class Controller(Node):
    def __init__(self,v1,v2,in1,in2,in3,in4,e1a,e1b,e2a,e2b):
        super().__init__('controller_subscriber')
        self.