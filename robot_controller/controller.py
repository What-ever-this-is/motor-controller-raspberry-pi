import rclpy as ros
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as g


class Controller(Node):
    def __init__(self,ena,enb,in1,in2,in3,in4,e1a,e1b,e2a,e2b,e3a,e3b,e4a,e4b):
        super().__init__("controller")
        self.subscription = self.create_subscription(
            String,
            "/motorcommands",
            self.listener_callback,
            10
        )
        self.subscription
        self.encoders = {
            "1":0,
            "2":0,
            "3":0,
            "4":0
        }
        self.motorPins = {
            "ena":ena,
            "enb":enb,
            "in1":in1,
            "in2":in2,
            "in3":in3,
            "in4":in4,
        }
        self.encoderPins = {
            "e1":{
            "a":e1a,
            "b":e1b,
            },
            "e2":{
            "a":e2a,
            "b":e2b,
            },
            "e3":{
            "a":e3a,
            "b":e3b,
            },
            "e4":{
            "a":e4a,
            "b":e4b,
            }
        }
        self.motorSignals = {
            "A":g.PWM(self.motorPins["ena"],1000),
            "B":g.PWM(self.motorPins["enb"],1000)
        }
        #region
        g.setmode(g.BOARD)
        g.setup(self.motorPins["ena"],g.OUT)
        g.setup(self.motorPins["enb"],g.OUT)
        g.setup(self.motorPins["in1"],g.OUT)
        g.setup(self.motorPins["in2"],g.OUT)
        g.setup(self.motorPins["in3"],g.OUT)
        g.setup(self.motorPins["in4"],g.OUT)
        g.setup(self.encoderPins["e1"]["a"],g.IN)
        g.setup(self.encoderPins["e1"]["b"],g.IN)
        g.setup(self.encoderPins["e2"]["a"],g.IN)
        g.setup(self.encoderPins["e2"]["b"],g.IN)
        g.setup(self.encoderPins["e3"]["a"],g.IN)
        g.setup(self.encoderPins["e3"]["b"],g.IN)
        g.setup(self.encoderPins["e4"]["a"],g.IN)
        g.setup(self.encoderPins["e4"]["b"],g.IN)
        g.add_event_detect(self.encoderPins["e1"]["a"],g.RISING,callback=\
 lambda: self.readEncoders(1))
        g.add_event_detect(self.encoderPins["e2"]["a"],g.RISING,callback=\
 lambda: self.readEncoders(2))
        g.add_event_detect(self.encoderPins["e3"]["a"],g.RISING,callback=\
 lambda: self.readEncoders(3))
        g.add_event_detect(self.encoderPins["e4"]["a"],g.RISING,callback=\
 lambda: self.readEncoders(4))
        #endregion
        self.motorSignals["A"].start(0)
        self.motorSignals["B"].start(0)
        
    
    def listener_callback(self,msg):
        self.get_logger().info(msg)
        msg = msg.split()
        motorCommands = {
            "Speed":msg[0],
            "Steer":msg[1]
        }
    
    def pid_loop(self,targetposition,motor):
        pass

    def readEncoders(self,encoderID):
        encoderB = g.input(self.encoderPins['e'+str(encoderID)]["b"])
        if(encoderB):
            self.encoders[str(encoderID)]+=1
        else:
            self.encoders[str(encoderID)]-=1
    def resetEncoders(self):
        for i in self.encoders:
            self.encoders[i] = 0
        

def main(args = None):
    ros.init()
    controller = Controller(7,11,12,13,15,16,18,22,29,31,32,33,35,36)
    ros.spin(controller)
    controller.destroy_node()
    ros.shutdown()

if __name__ == 'main':
    main()
