import rclpy as ros
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as g


class Controller(Node):
    def __init__(self,ena,enb,in1,in2,in3,in4):
        super().__init__("controller")
        self.subscription = self.create_subscription(
            String,
            "/motorcommands",
            self.listener_callback,
            10
        )
        self.subscription
        self.motorPins = {
            "ena":ena,
            "enb":enb,
            "in1":in1,
            "in2":in2,
            "in3":in3,
            "in4":in4,
        }
        self.motorSignals = {
            "A":g.PWM(self.motorPins["ena"],1000),
            "B":g.PWM(self.motorPins["enb"],1000)
        }
        g.setmode(g.BOARD)
        g.setup(self.motorPins["ena"],g.OUT)
        g.setup(self.motorPins["enb"],g.OUT)
        g.setup(self.motorPins["in1"],g.OUT)
        g.setup(self.motorPins["in2"],g.OUT)
        g.setup(self.motorPins["in3"],g.OUT)
        g.setup(self.motorPins["in4"],g.OUT)
        self.motorSignals["A"].start(0)
        self.motorSignals["B"].start(0)
    
    def listener_callback(self,msg):
        self.get_logger().info(msg)
        msg = msg.split()
        motorCommands = {
            "Speed":msg[0],
            "Steer":msg[1]
        }
        

def main(args = None):
    ros.init()
    controller = Controller(1,2,3,4,5,6)
    ros.spin(controller)
    controller.destroy_node()
    ros.shutdown()

if __name__ == 'main':
    main()
