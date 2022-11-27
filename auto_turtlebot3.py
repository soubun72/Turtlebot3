#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, BatteryState

distance_travel = 0 #initial value
battery_voltage = 12 #initial value
minVoltage = 10 #robot stop moving if battery_voltage < 10
maxDistanceTravel = 100 #robot stop moving if it has travelled for more than 100m

maxDistance= 0.4 #maximum distance to consider the object to be an obstactle

command = False

def callback(message):
    global command
    command = False
    for i in range(330,360):
        if message.ranges[i] < maxDistance and message.ranges[i]!=0:
            command = True

    for i in range(0,30):
        if message.ranges[i] < maxDistance and message.ranges[i]!=0:
            command = True

    #command = True -> rotate
    #command = False -> go forward


def battery_check(message):
    global battery_voltage
    battery_voltage = message.voltage

def auto_nav():
    global command
    global distance_travel
    global battery_voltage

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber("/scan", LaserScan, callback)
    rospy.Subscriber("/battery_state", BatteryState, battery_check)
    rospy.init_node('auto_lab2', anonymous=False)
    
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        vel = Twist()
        
        if command == True: #rotate
            vel.linear.x = 0
            vel.angular.z = 0.6
            
        else: #go forward
            vel.angular.z = 0
            vel.linear.x = 0.3

        distance_travel = distance_travel + vel.linear.x * 0.1 #y = y + y'Ts (integration)


        if distance_travel < maxDistanceTravel and battery_voltage > minVoltage:
            pub.publish(vel) #publish only if the above condition is satisfied

        rate.sleep()

if __name__ == '__main__':
    try:
        auto_nav()
    except rospy.ROSInterruptException:
        pass
