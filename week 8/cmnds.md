#simple urdf launch
ros2 launch urdf_tutorial display.launch.py model:=/home/alishbakiyani/ros2_ws_alishba/src/my_robot_description/urdf/my_robot.urdf
# custom urdf launch
ros2 launch urdf_tutorial display.launch.py model:=/home/alishbakiyani/ros2_ws_alishba/src/my_robot_description/urdf/custom_robot.urdf
#tf frame
ros2 run tf2_tools view_frames
#vista urdf  launch
cd ~/ros2_ws_alishba
source install/setup.bash
ros2 launch my_robot_description display.launch.py

