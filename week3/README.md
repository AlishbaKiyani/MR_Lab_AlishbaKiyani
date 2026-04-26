#  Lab Manual 3: ROS 2 Workspace, Package Creation & Turtle Control

##  Objective

- Set up a ROS 2 workspace  
- Learn GitHub for version control  
- Create a ROS 2 Python package  
- Develop nodes to control turtle movement in different patterns  


## Brief Description

In this lab, we implemented the complete workflow of setting up a ROS 2 workspace, creating a custom package, and developing Python nodes to control turtle motion in the turtlesim environment. We learned how to build and source a workspace, configure GitHub for version control, and create ROS 2 packages using `ament_python`.

We developed multiple nodes to move the turtle in different patterns such as square, circular, and triangular trajectories. Additionally, we implemented motion control to move the turtle to a specific location. The lab also involved running multiple nodes simultaneously and understanding how ROS 2 topics and services are used for robot control. By the end of the lab, we successfully executed different motion patterns and managed our project using GitHub.

---

## Commands Used

### Create and Build Workspace
```bash
mkdir -p ~/ros2_ws_alishba/src
cd ~/ros2_ws_alishba
colcon build
```

### Source Workspace
```bash
source install/setup.bash
```

### Add Auto Source to bashrc
```bash
echo 'source ~/ros2_ws_alishba/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

---

## GitHub Setup

### Install GitHub CLI
```bash
sudo apt install gh
sudo snap install gh --classic
```

### Authenticate GitHub
```bash
gh auth logout
gh auth login
```

---

## Package Creation

```bash
cd ~/ros2_ws_alishba/src

ros2 pkg create --build-type ament_python \
--dependencies rclpy turtlesim \
--node-name my_node my_turtle_package
```

---

## Running Turtlesim

```bash
ros2 run turtlesim turtlesim_node
```

---

## Running Custom Nodes

```bash
ros2 run my_turtle_package move_turtle
ros2 run my_turtle_package move_circle
ros2 run my_turtle_package move_triangle
ros2 run my_turtle_package move_to_location
```

---

## Reset Simulation

```bash
ros2 service call /reset std_srvs/srv/Empty
```

---

## Tasks Performed

1. **Square Motion**  
   Implemented linear and angular velocity control to move the turtle in a square path.

2. **Circular Motion**  
   Applied continuous linear and angular velocity to generate a circular trajectory.

3. **Triangular Motion**  
   Controlled angular turns (120°) to create a triangular path.

4. **Move to Specific Location**  
   Designed logic to move turtle to a desired coordinate using velocity commands.

5. **Multiple Turtles (Advanced Task)**  
   Spawned multiple turtles and controlled them independently using separate topics.

---

## Problems Faced and How They Were Solved

1. **Problem:** Workspace not recognized  
   **Solution:** Forgot to source workspace. Fixed by running:
```bash
source install/setup.bash
```

2. **Problem:** Package not found while running node  
   **Solution:** Workspace was not rebuilt after creating package. Fixed using:
```bash
colcon build
```

3. **Problem:** Node not executing  
   **Solution:** Python file was not executable. Fixed by:
```bash
chmod +x move_turtle.py
```

4. **Problem:** Turtle not moving correctly  
   **Solution:** Adjusted linear and angular velocity values and timing logic.

---

## Reflection

This lab provided a strong foundation in ROS 2 development by combining workspace setup, package creation, and node programming. I learned how to structure a ROS 2 project and implement motion control using Python. Writing different motion patterns improved my understanding of robot kinematics and velocity control.

The integration of GitHub helped in managing project files efficiently. Running multiple nodes and controlling different turtle behaviors enhanced my understanding of ROS 2 communication through topics and services. Overall, this lab improved my practical skills in ROS 2 and prepared me for more advanced robotic applications.
