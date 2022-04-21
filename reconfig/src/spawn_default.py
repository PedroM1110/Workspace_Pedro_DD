#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import DeleteModel
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
import actionlib

def spawn_node():

    rospy.init_node('spawn_node')
    rospy.loginfo('Initializing...')
    

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

    goal = MoveBaseGoal()

    goal.target_pose.header.frame_id = 'map' 
    goal.target_pose.pose.position.x = 2.0
    goal.target_pose.pose.position.y = -11.0
    goal.target_pose.pose.orientation.z = 0.99
    goal.target_pose.pose.orientation.w = 0.0

    spawn_model_client = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)

    delete_model_client = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)

    rospy.sleep(5)

    spawn_model_client(
        model_name='trash_can_1',
        model_xml=open("/home/pedro/modelo/first_2015_trash_can/model.sdf",'r').read(),
        initial_pose = Pose(position= Point(6.8,-8,0),orientation=Quaternion(0,0,0,2))
    )

    

    rospy.sleep(0.5)

    spawn_model_client(
        model_name='person_1',
        model_xml=open("/home/pedro/modelo/person_standing/model.sdf",'r').read(),
        initial_pose = Pose(position= Point(4.5,-10.5,0),orientation=Quaternion(0,0,0,2))
    )

    

    rospy.sleep(0.5)

    spawn_model_client(
        model_name='person_2',
        model_xml=open("/home/pedro/modelo/person_standing/model.sdf",'r').read(),
        initial_pose = Pose(position= Point(6.0,-12.5,0),orientation=Quaternion(0,0,0,2))
    )

    

    
    client.send_goal(goal)
    rospy.sleep(50)

    rospy.sleep(0.5)

    goal.target_pose.header.frame_id = 'map' 
    goal.target_pose.pose.position.x = 8.0
    goal.target_pose.pose.position.y = -2.0
    goal.target_pose.pose.orientation.z = 0.99
    goal.target_pose.pose.orientation.w = 0.0

    
    client.send_goal(goal)

    rospy.sleep(10)

    delete_model_client(
        model_name = 'trash_can_1'
    )
    
    
    
    pass
		
if __name__ == '__main__':
    try:
        spawn_node()
        
    except rospy.ROSInterruptException: pass
