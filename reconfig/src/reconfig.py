#! /usr/bin/env python3

##############################################
# Reconfiguração dinâmica de parâmetros
##############################################

import roslib;roslib.load_manifest("move_base")
#import roslib;roslib.load_manifest("map_server")
import roslib;roslib.load_manifest("global_planner")
import rospy
import dynamic_reconfigure.client
import sys

def reconfig_local_costmap_size(i):

    client = dynamic_reconfigure.client.Client("move_base/local_costmap", timeout=4, config_callback=None)
    
    if(i == 2):
        
	    client.update_configuration({"width":2})
	    client.update_configuration({"height":2})
        
    elif(i == 1):
        
	    client.update_configuration({"width":1})
	    client.update_configuration({"height":1})
        
    pass
	
def reconfig_local_planner():

	client = dynamic_reconfigure.client.Client("move_base", timeout=4, config_callback=None)
	
	## CHANGE TO DWA
	client.update_configuration({"base_local_planner": "dwa_local_planner/DWAPlannerROS"})
	
	## CHANGE TO TEB
	#client.update_configuration({"base_local_planner": "teb_local_planner/TebLocalPlannerROS"})
	
	pass	
	
	
def reconfig_gobal_planner():

	client = dynamic_reconfigure.client.Client("move_base", timeout=4, config_callback=None)
	
	#PARA A*
	#client.update_configuration({"base_global_planner":"global_planner/GlobalPlanner"})
	
	#PARA DIJKSTRA
	client.update_configuration({"base_global_planner":"navfn/NavfnROS"})
	
	pass	


if __name__ == "__main__":


    try:
        rospy.init_node("reconfig_params")
        #while not rospy.is_shutdown():
            #reconfig_local_costmap_size(1)
            #rospy.sleep(5)
            #reconfig_local_costmap_size(2)
            #rospy.sleep(5)
            
        #reconfig_gobal_planner()
        reconfig_local_planner()
		#reconfig_map()
        pass
    except: 
		
        sys.exit("ERROR")
	

