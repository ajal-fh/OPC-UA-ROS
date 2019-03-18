#!/usr/bin/env python

import sys
import rospy



from teleop_rover.srv import *
from teleop_rover.msg import *

node = Address()
data= TypeValue()

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
	print "inside write_client"
	rospy.wait_for_service('/opcua/opcua_client/write')

	try:			
		write = rospy.ServiceProxy('/opcua/opcua_client/write',Write)
		resp1 = write(node,data)
		return resp1.success, resp1.error_message
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e


if __name__ == "__main__":
	print "hola"
	node.nodeId = 'ns=2;i=8'
	node.qualifiedName = 'MyVariable'

	data.type = 'float64'
	data.bool_d = False
	data.int8_d = 0
	data.uint8_d = 0
	data.int16_d = 0
	data.uint16_d = 0
	data.int32_d = 0
	data.uint32_d = 0
	data.int64_d =0
	data.uint64_d = 0
	data.float_d = 0.0
	data.double_d =4.1
	data.string_d =''

	write_client(node,data)
'''#to connect
	endpoint = "opc.tcp://localhost:4840"	
	connect_client(endpoint)
#to disconnect	
	disconnect_client()'''
 



