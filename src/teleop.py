#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Int16
from std_msgs.msg import Bool

rospy.init_node('teleop',anonymous=True)

speed_pwm = Int16()
reverse_bool = Bool()

def callback(data_1):
	#print 	data.axes[2]
	#print data.buttons[3]
	if data_1.buttons[3] == 1:
		speed_pwm.data = 255
		reverse_bool.data = False
		
	elif data_1.buttons[0] == 1:
		speed_pwm.data = 255
		reverse_bool.data = True
	else:
		speed_pwm.data = 0
		

rospy.Subscriber("joy",Joy,callback)
pub1 = rospy.Publisher('speed_pwm',Int16,queue_size=10)
pub2 = rospy.Publisher('reverse_bool',Bool,queue_size=10)

rate =rospy.Rate(10)

while not rospy.is_shutdown():
	pub1.publish(speed_pwm)
	pub2.publish(reverse_bool)
	rate.sleep()
		


