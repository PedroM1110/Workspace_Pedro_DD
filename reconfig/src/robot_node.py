#!/usr/bin/env python3

##################################################################
# Nó que lê o topico /wsn e recalcula a rota
##################################################################

import rospy
import tf
from std_msgs.msg import Float64MultiArray
from std_srvs.srv import Empty
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import math 
import angles

move_Goal = MoveBaseGoal()
move_Goal_Test = MoveBaseGoal()


def validate_goal(plan):
    

    if (plan.poses == [ ]):
        
        pub_vel.publish(stop)
    pass


def get_goal(current_Goal):
    

	
    move_Goal.target_pose.header.seq         = current_Goal.header.seq
    move_Goal.target_pose.header.frame_id    = current_Goal.header.frame_id
    move_Goal.target_pose.header.stamp       = current_Goal.header.stamp
    move_Goal.target_pose.pose.position.x    = float(current_Goal.pose.position.x)
    move_Goal.target_pose.pose.position.y    = float(current_Goal.pose.position.y)
    move_Goal.target_pose.pose.position.z    = float(current_Goal.pose.position.z)
    move_Goal.target_pose.pose.orientation.x = float(current_Goal.pose.orientation.x)
    move_Goal.target_pose.pose.orientation.y = float(current_Goal.pose.orientation.y)
    move_Goal.target_pose.pose.orientation.z = float(current_Goal.pose.orientation.z)
    move_Goal.target_pose.pose.orientation.w = float(current_Goal.pose.orientation.w)
	
    pass

def get_odom(odom):
	

    move_Goal_Test.target_pose.pose.position.x    = float(odom.pose.pose.position.x)
    move_Goal_Test.target_pose.pose.position.y    = float(odom.pose.pose.position.y)
    move_Goal_Test.target_pose.pose.orientation.x = float(odom.pose.pose.orientation.x)
    move_Goal_Test.target_pose.pose.orientation.y = float(odom.pose.pose.orientation.y)
    move_Goal_Test.target_pose.pose.orientation.z = float(odom.pose.pose.orientation.z)
    move_Goal_Test.target_pose.pose.orientation.w = float(odom.pose.pose.orientation.w)
	
    pass
    

def robot_node(dado):


    clear_srv()
    
    quaternion_Goal = (
        move_Goal.target_pose.pose.orientation.x,\
        move_Goal.target_pose.pose.orientation.y,\
        move_Goal.target_pose.pose.orientation.z,\
        move_Goal.target_pose.pose.orientation.w)
    euler_Goal = tf.transformations.euler_from_quaternion(quaternion_Goal)
    yaw_Goal = euler_Goal[2]
    
    quaternion_Goal_Test = (
        move_Goal_Test.target_pose.pose.orientation.x,\
        move_Goal_Test.target_pose.pose.orientation.y,\
        move_Goal_Test.target_pose.pose.orientation.z,\
        move_Goal_Test.target_pose.pose.orientation.w)
    euler_Goal_Test = tf.transformations.euler_from_quaternion(quaternion_Goal_Test)
    yaw_Goal_Test = euler_Goal_Test[2]
    
    if  (math.hypot(move_Goal.target_pose.pose.position.x - move_Goal_Test.target_pose.pose.position.x,\
                    move_Goal.target_pose.pose.position.y - move_Goal_Test.target_pose.pose.position.y) > 0.10 or \
         (abs(angles.shortest_angular_distance(yaw_Goal_Test, yaw_Goal)) > 0.17) ):
        
        rospy.sleep(1)
        client.send_goal(move_Goal)
        
    pass


		
if __name__ == '__main__':
	
    try:
        
        global stop
        stop = Twist()
        stop.linear.x  = 0.0
        stop.linear.y  = 0.0
        stop.linear.z  = 0.0
        stop.angular.x = 0.0
        stop.angular.y = 0.0
        stop.angular.z = 0.0

        sub_Goal  = rospy.Subscriber("/move_base/current_goal", PoseStamped, get_goal)
        sub_Odom  = rospy.Subscriber("/odom", Odometry, get_odom)
        sub_WSN   = rospy.Subscriber("/wsn", Float64MultiArray, robot_node)
        sub_plan = rospy.Subscriber("/move_base/GlobalPlanner/plan", Path, validate_goal)
        pub_Stop  = rospy.Publisher("/move_base/cancel", GoalID, queue_size=10)
        pub_vel   = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
        client    = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        clear_srv = rospy.ServiceProxy('move_base/clear_costmaps', Empty)
        rospy.init_node('robot_node')
        rospy.loginfo("Robot_node_init")
        rospy.spin()
			
			
			
    except rospy.ROSInterruptException: pass