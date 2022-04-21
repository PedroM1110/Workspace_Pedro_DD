#!/usr/bin/env python3

import rospy
from actionlib_msgs.msg import GoalStatusArray

def goal_status(dado):
    rospy.loginfo(dado.status_list[0].status)


def read_node():
    rospy.init_node('read_node')
    sub  = rospy.Subscriber("/move_base/status", GoalStatusArray, goal_status)

    
		
if __name__ == '__main__':
    try:
        read_node()
        rospy.spin()
    except rospy.ROSInterruptException: pass
