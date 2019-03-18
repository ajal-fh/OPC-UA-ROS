#!/usr/bin/env python

import sys
import rospy



from teleop_rover.srv import *



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

if __name__ == "__main__":
	print "hola"
#to connect
	endpoint = "opc.tcp://localhost:4840"	
	connect_client(endpoint)
#to disconnect	
	disconnect_client()	
	print "end" 


