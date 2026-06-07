#source
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger
#gazebo
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
#rviz
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
use_sim_time:=True \
map:=$HOME/maps/my_map.yaml
# Check Nav2 action server is up
ros2 action list

# Echo AMCL pose
ros2 topic echo /amcl_pose

#costmap topic 
ros2 topic list | grep costmap

# Check costmap
ros2 topic echo /global_costmap/costmap
# Watch local costmap update in real-time near obstacle
ros2 topic echo /local_costmap/costmap_updates
# Check inflation radius parameter
ros2 param get /local_costmap/local_costmap inflation_layer.inflation_radius

# Monitor navigation status
ros2 topic echo /navigate_to_pose/_action/status

#waypoint node
ros2 run autonomous_navigation waypoint_navigator

#with arguments
ros2 run autonomous_navigation waypoint_navigator 1.20 -1.27 0.99 2.77 -1.18 0.99 3.74 -0.47 0.80

