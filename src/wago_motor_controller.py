#!/usr/bin/env python

import sys
import rospy


from sensor_msgs.msg import Joy
from std_msgs.msg import Int16
from std_msgs.msg import Bool

from teleop_rover.srv import *
from teleop_rover.msg import *
#defining opcua variables for sending
speed_pwm_opcua_node = Address()
speed_pwm_opcua_data = TypeValue()

direction_opcua_node = Address()
direction_opcua_data = TypeValue()

brake_opcua_node     = Address()
brake_opcua_data     = TypeValue()

rospy.init_node('teleop_opcua',anonymous=True)

speed_pwm 	= Int16()
reverse_bool    = Bool()
brake_bool 	= Bool()

def callback(data_1):
	#print 	data.axes[2]
	#print data.buttons[3]
	if data_1.buttons[3] == 1:
		speed_pwm.data    = 255
		reverse_bool.data = False
		brake_bool.data   = False
	elif data_1.buttons[0] == 1:
		speed_pwm.data    = 255
		reverse_bool.data = True
		brake_bool.data   = False
	elif data_1.buttons[7] == 1:
		speed_pwm.data  = 0
		brake_bool.data = True
	else:
		speed_pwm.data  = 0
		brake_bool.data = False

def disconnect_client():
	
	rospy.wait_for_service('/opcua/opcua_client/disconnect')	
		
	try:			
		disconnect = rospy.ServiceProxy('/opcua/opcua_client/disconnect',Disconnect)
		resp1 = disconnect()
		return resp1.success, resp1.error_message
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e


def connect_client(endpoint):
	
	rospy.wait_for_service('/opcua/opcua_client/connect')	
		
	try:			
		connect = rospy.ServiceProxy('/opcua/opcua_client/connect',Connect)
		resp1 = connect(endpoint)
		return resp1.success, resp1.error_message
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

def write_client(node,data):
	
	rospy.wait_for_service('/opcua/opcua_client/write')

	try:			
		write = rospy.ServiceProxy('/opcua/opcua_client/write',Write)
		resp1 = write(node,data)
		return resp1.success, resp1.error_message
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e
def trial():
	disconnect_client()

if __name__ == "__main__":

# connecting to the opc_ua server
	endpoint = "opc.tcp://149.201.218.162:4840"	
	connect_client(endpoint)

	rospy.Subscriber("joy",Joy,callback)
	pub1 = rospy.Publisher('speed_pwm',Int16,queue_size=10)
	pub2 = rospy.Publisher('reverse_bool',Bool,queue_size=10) 
	pub3 = rospy.Publisher('brake_bool',Bool,queue_size=10)

# assign the variables from the opc_ua server	
	#node for direction give the nodeId and qualifiedName accordingly	
	direction_opcua_node.nodeId = 'ns=4;s=|var|WAGO 750-8206 PFC200 CS 2ETH RS CAN DPS.Application.PLC_PRG.Reverse_Left'
	direction_opcua_node.qualifiedName = 'Reverse_Left'
	direction_opcua_data.type = 'bool'
	

	#node for speed give the nodeId and qualifiedName accordingly	
	speed_pwm_opcua_node.nodeId = 'ns=4;s=|var|WAGO 750-8206 PFC200 CS 2ETH RS CAN DPS.Application.PLC_PRG.Throttle_Left'
	speed_pwm_opcua_node.qualifiedName = 'Throttle_Left'
	speed_pwm_opcua_data.type = 'uint8'
	
	#node for brake give the nodeId and qualifiedName accordingly
	brake_opcua_node.nodeId = 'ns=4;s=|var|WAGO 750-8206 PFC200 CS 2ETH RS CAN DPS.Application.PLC_PRG.Brake_Left'
	brake_opcua_node.qualifiedName = 'Brake_Left'
	brake_opcua_data.type = 'bool'
		
	
	rate =rospy.Rate(10)

	while not rospy.is_shutdown():	
		#writing current values to the nodes(opcua)	
		direction_opcua_data.bool_d = reverse_bool.data
		speed_pwm_opcua_data.uint8_d = speed_pwm.data
		brake_opcua_data.bool_d = brake_bool.data

		# write the data to the opc server 
		write_client(direction_opcua_node,direction_opcua_data)
		write_client(speed_pwm_opcua_node,speed_pwm_opcua_data)	
		write_client(brake_opcua_node,brake_opcua_data)
	
		#publish the speed,reverse and brake boolean for reference			
		pub1.publish(speed_pwm)
		pub2.publish(reverse_bool)
		pub3.publish(brake_bool)
		
		rospy.on_shutdown(trial)
		rate.sleep()
	
	


