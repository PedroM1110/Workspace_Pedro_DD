#!/usr/bin/env python3

############################################################################################
# Nó que recebe dados dos sensores e publica no tópico /wsn
############################################################################################

import rospy
from std_msgs.msg import String

def fog_node():
	
    pub = rospy.Publisher('wsn', String)
    rospy.init_node('fog_node')
	
    while not rospy.is_shutdown():
		
        str = "1"
        rospy.loginfo(str)
        pub.publish(str)
        rospy.sleep(5.0)
		
        str = "2"
        rospy.loginfo(str)
        pub.publish(str)
        rospy.sleep(5.0)
		
    pass
		
if __name__ == '__main__':
    try:
        fog_node()
    except rospy.ROSInterruptException: pass