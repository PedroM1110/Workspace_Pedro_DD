#! /usr/bin/env python3

import rospy
import sys
import subprocess


def kill_node():
	#Kiling the node
	subprocess.Popen("rosnode kill map_server", shell=True)
	
	pass 

def change_map(mapa):

	kill_node()
	
	#Launching Z1
	if mapa == 1:
		
		subprocess.Popen("roslaunch turtlebot3_navigation map_server.launch map_file:=$HOME/map_Z1.yaml", shell=True)
		
	#Launching Z2
	elif mapa == 2:
		
		subprocess.Popen("roslaunch turtlebot3_navigation map_server.launch map_file:=$HOME/map_Z2.yaml",shell=True)
		
	#Launching Z0
	elif mapa == 0:
		
		subprocess.Popen("roslaunch turtlebot3_navigation map_server.launch map_file:=$HOME/map.yaml",shell=True)
	
	
	pass



if __name__ == "__main__":
	
	try:
		a = 1
		while a < 3 :	
			change_map(a)
			rospy.sleep(5.0)
			a += 1

	except: 
		sys.exit("ERROR")
	

