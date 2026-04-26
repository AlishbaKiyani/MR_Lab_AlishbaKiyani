cd ~/ros2_ws_alishba
colcon build
source install/setup.bash
sudo apt install gh
sudo snap install gh --classic
gh auth logout
gh auth login
ros2 run turtlesim turtlesim_node
ros2 run my_turtle_package move_to_location
ros2 run my_turtle_package move_circle
ros2 run my_turtle_package move_triangle
ros2 run my_turtle_package move_turtle
ros2 service call /reset std_srvs/srv/Empty
