#include<simple_layers/simple_layer.h>  
#include <pluginlib/class_list_macros.h>  
#include <ros/ros.h>
#include <tf/tf.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/Pose.h>
#include <nav_msgs/Odometry.h>
#include <costmap_2d/layer.h>  
#include <costmap_2d/layered_costmap.h> 
#include "std_msgs/Float64MultiArray.h"
#include "std_msgs/Float64.h"
#include <string>
#include <dynamic_reconfigure/DoubleParameter.h>
#include <dynamic_reconfigure/Reconfigure.h>
#include <dynamic_reconfigure/Config.h>
#include <ros/service_client.h>
#include <pthread.h>
#include <base_local_planner/goal_functions.h>
#include <nav_msgs/Path.h>
  
PLUGINLIB_EXPORT_CLASS(simple_layer_namespace::SimpleLayer, costmap_2d::Layer)//Register plug-in
  
#define Nothing -999

using costmap_2d::LETHAL_OBSTACLE;  
using costmap_2d::FREE_SPACE; 
  
namespace simple_layer_namespace  
{  
  
SimpleLayer::SimpleLayer() {}  
  
void SimpleLayer::onInitialize()  
{  
	
  ros::NodeHandle n("~/" + name_);
	
  ros::NodeHandle nh("~/" + name_);
  
  sub = n.subscribe("/wsn", 1000, &SimpleLayer::callback, this);
  
  pthread_mutex_init(&mutex, NULL);
	
  current_ = true;								
  
  dsrv_ = new dynamic_reconfigure::Server<costmap_2d::GenericPluginConfig>(nh);
  
  dynamic_reconfigure::Server<costmap_2d::GenericPluginConfig>::CallbackType cb = boost::bind( &SimpleLayer::reconfigureCB, this, _1, _2);
  
  dsrv_->setCallback(cb);

}  
  
  

//Callback que recebe os dados da WSN (incrito no tópico /wsn)	
void SimpleLayer::callback(const std_msgs::Float64MultiArray::ConstPtr& array){
  
	ROS_INFO("Zona 1: %f, %f", array->data[0],array->data[1]);
  ROS_INFO("Zona 2: %f, %f", array->data[2],array->data[3]);
  ROS_INFO("Zona 3: %f, %f", array->data[4],array->data[5]);
  ROS_INFO("Zona 4: %f, %f", array->data[6],array->data[7]);

	place_1x = array->data[0];
  place_1y = array->data[1];
  place_2x = array->data[2];
  place_2y = array->data[3];
  place_3x = array->data[4];
  place_3y = array->data[5];
  place_4x = array->data[6];
  place_4y = array->data[7];
  
    
}
//******************************

void SimpleLayer::reconfigureCB(costmap_2d::GenericPluginConfig &config, uint32_t level)  
{  
  enabled_ = config.enabled; 
}  
  
void SimpleLayer::updateBounds(double origin_x, double origin_y, double origin_yaw, double* min_x,  
                                           double* min_y, double* max_x, double* max_y)
  
{  
  if (!enabled_)
  
    return;
  
  mark_x_ = origin_x + cos(origin_yaw);
  
  mark_y_ = origin_y + sin(origin_yaw);
  
  *min_x = std::min(*min_x, mark_x_);
  
  *min_y = std::min(*min_y, mark_y_);
  
  *max_x = std::max(*max_x, mark_x_);
  
  *max_y = std::max(*max_y, mark_y_);
  

}  
  
void SimpleLayer::updateCosts(costmap_2d::Costmap2D& master_grid, int min_i, int min_j, int max_i,  int max_j)
{  
  if (!enabled_)
  
    return;
//############################################################################################
  if ((place_1x != Nothing) && (place_1y != Nothing)){
    master_grid.worldToMap(place_1x,place_1y,mx[0],my[0]);
    for ( unsigned int aux1 = 0; aux1 < inflation; aux1++){
      for (unsigned int aux2 = 0; aux2 < inflation; aux2++){
        master_grid.setCost(mx[0]+aux1,my[0]+aux2,LETHAL_OBSTACLE);
      }
    }
  }
//############################################################################################
  if ((place_2x != Nothing) && (place_2y != Nothing)){
    master_grid.worldToMap(place_2x,place_2y,mx[0],my[0]);
    for (unsigned int aux1 = 0; aux1 < inflation; aux1++){
      for (unsigned int aux2 = 0; aux2 < inflation; aux2++){
        master_grid.setCost(mx[0]+aux1,my[0]+aux2,LETHAL_OBSTACLE);
      }
    }
  }
//############################################################################################
  if ((place_3x != Nothing) && (place_3y != Nothing)){
    master_grid.worldToMap(place_3x,place_3y,mx[0],my[0]);
    for (unsigned int aux1 = 0; aux1 < inflation; aux1++){
      for (unsigned int aux2 = 0; aux2 < inflation; aux2++){
        master_grid.setCost(mx[0]+aux1,my[0]+aux2,LETHAL_OBSTACLE);
      }
    }
  }
//############################################################################################
  if ((place_4x != Nothing) && (place_4y != Nothing)){
    master_grid.worldToMap(place_4x,place_4y,mx[0],my[0]);
    for (unsigned int aux1 = 0; aux1 < inflation; aux1++){
      for (unsigned int aux2 = 0; aux2 < inflation; aux2++){
        master_grid.setCost(mx[0]+aux1,my[0]+aux2,LETHAL_OBSTACLE);
      }
    }
  }  
 }  
} //end namespace