import rclpy as ros
from rclpy.node import Node
from std_msgs.msg import String
from time import sleep
from timeit import default_timer
import RPi.GPIO as g


class Controller(Node):
    def __init__(self,ena,enb,in1,in2,in3,in4,e1a,e1b,e2a,e2b):
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
        g.add_event_detect(self.encoderPins["e1"]["a"],g.RISING,callback=\
 lambda: self.readEncoders(1))
        g.add_event_detect(self.encoderPins["e2"]["a"],g.RISING,callback=\
 lambda: self.readEncoders(2))
        #endregion
        self.motorSignals = {
            "1":g.PWM(self.motorPins["ena"],1000),
            "2":g.PWM(self.motorPins["enb"],1000)
        }
        self.motorSignals["1"].start(0)
        self.motorSignals["2"].start(0)
        g.output(self.motorPins["in1"],g.HIGH)
        g.output(self.motorPins["in2"],g.LOW)
        g.output(self.motorPins["in3"],g.HIGH)
        g.output(self.motorPins["in4"],g.LOW)
        self.targetPositions = {
            "1":0,
            "2":0
        }
        self.pidGains = {
            "p":1,
            "d":0,
            "i":0
        }
        self.pidVaribles = {
            "prevTime":0,
            "prevE":0,
            "integralE":0,
            "currentT":0,
            "encoderCountsPerPIDLoop":0,
            "deltaTime":0,
            "started":False,
            "prevEncoderValues":{
                "1":0,
                "2":0
            },
            "E":0,
        }
        self.running = False
        self.pidLoopsPerSecond = 30
        self.encoderCountsPerRevolution = 100
        
    def listener_callback(self,msg):
        self.get_logger().info(msg)
        msg = msg.split()
        motorCommands = {
            "Speed":msg[0],
            "Steer":msg[1]
        }
    
    def pid_loop(self):
        if self.running:
            if not self.pidVariables["started"]:
                self.pidVariables["started"] = True
                self.pidVariables["prevTime"] = default_timer()
                self.pidVariables["prevEncoderValues"]["1"] = self.encoders["1"]
                self.pidVariables["prevEncoderValues"]["2"] = self.encoders["2"]
            self.pidVariables["encoderCountsPerPIDLoop"] = self.encoderCountsPerRevolution/self.pidLoopsPerSecond
            for i in self.targetSpeeds:
                self.pidVariables["currentTime"] = default_timer()
                self.pidVariables["deltaTime"] = self.pidVariables["currentTime"] - self.pidVariables["prevTime"]
                self.pidVariables["prevTime"] = self.pidVariables["currentTime"]
                self.pidVariables["E"] = self.encoders[i]-self.targetPositions[i]
                dedt = self.pidVariables["prevE"]/self.pidVariables["deltaTime"]
                self.pidVariables["integralE"] = self.pidVariables["integralE"] + self.pidVariables["E"]*self.pidVariables["deltaTime"]
                u = self.pidGains["P"]*self.pidVariables["E"]+self.pidGains["I"]*self.pidVariables["integralE"]+self.pidGains["D"]+dedt
                power = abs(u)
                if(power>100):
                    power = 100
                dir = 1
                if(u<0):
                    dir=0
                self.setMotorSpeed(int(i),power)
                self.setMotorDirection(int(i),dir)
            sleep(1/self.pidLoopsPerSecond)
            self.pid_loop()
        else:
            self.pidVariables["started"] = False
    def setMotorSpeed(self,motor,speed):
        self.motorSignals[str(motor)].changeDutyCycle(speed)
    def setMotorDirection(self,motor,forwards):
        if motor == 1:
            if forwards:
                g.output(self.motorPins["in1"],g.HIGH)
                g.output(self.motorPins["in2"],g.LOW)
            else:
                g.output(self.motorPins["in1"],g.LOW)
                g.output(self.motorPins["in2"],g.HIGH)
        elif motor == 2:
            if forwards:
                g.output(self.motorPins["in3"],g.HIGH)
                g.output(self.motorPins["in4"],g.LOW)
            else:
                g.output(self.motorPins["in3"],g.LOW)
                g.output(self.motorPins["in4"],g.HIGH)
    def stop(motor):
        if motor == 1:
            g.output(self.motorPins["in1"],g.HIGH)
            g.output(self.motorPins["in2"],g.LOW)

    def setTargetSpeed(self,motor,position):
        self.targetSpeeds[str(motor)] = position
        
    def readEncoders(self,encoderID):
        encoderB = g.input(self.encoderPins['e'+str(encoderID)]["b"])
        if(encoderB):
            self.encoders[str(encoderID)]-=1
        else:
            self.encoders[str(encoderID)]+=1
    def resetEncoders(self):
        for i in self.encoders:
            self.encoders[i] = 0
        

def main(args = None):
    ros.init()
    controller = Controller(7,11,12,13,15,16,18,22,29,31)
    ros.spin(controller)
    controller.destroy_node()
    ros.shutdown()

if __name__ == 'main':
    main()
