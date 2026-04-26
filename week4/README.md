
# Week 4 Lab ROS 2 Launch, Rosbag, and RQT Plot

## Brief Description

In Week 4 lab, we explored advanced ROS 2 tools including the launch system, rosbag, and rqt_plot. We learned how to create and use a launch file to run multiple nodes simultaneously in the turtlesim environment. A second turtle was introduced, and a follow-the-leader behavior was implemented where turtle2 follows turtle1 based on its pose.

We also recorded real-time topic data using rosbag and replayed it to analyze robot motion. Additionally, we used rqt_plot to visualize velocity commands (`/turtle1/cmd_vel`) and understand system behavior. This lab provided practical experience in managing multiple nodes, recording data, and analyzing robotic systems.

---

## Commands Used

### Source ROS 2 environment

```bash
source /opt/ros/humble/setup.bash
```

### Build workspace

```bash
cd ~/ros2_ws_alishba
colcon build
source install/setup.bash
```

---

### Launch two turtles

```bash
ros2 launch my_launch_pkg two_turtles_launch.py
```

---

### Run follow-the-leader node

```bash
ros2 run my_launch_pkg follow_leader
```

---

### Record rosbag data

```bash
ros2 bag record /turtle1/pose /turtle1/cmd_vel /turtle2/cmd_vel
```

### Stop recording

Press `CTRL + C`

---

### Play recorded data

```bash
ros2 bag play <bag_file_name>
```

---

### Open RQT

```bash
rqt
```

### Plot velocity

* Go to: Plugins → Visualization → Plot
* Add topic:

```
/turtle1/cmd_vel
```

---

## Additional Tasks

### Spawn second turtle (if not in launch file)

```bash
ros2 service call /spawn turtlesim/srv/Spawn "{x: 5.0, y: 5.0, theta: 0.0, name: 'turtle2'}"
```

---

## Problems Faced and Solutions

1. **Problem:** Launch file not running
   **Solution:** Ensured correct package build and sourced workspace using:

```bash
source install/setup.bash
```

2. **Problem:** Turtle2 not following properly
   **Solution:** Corrected logic in `follow_leader.py` for angle and distance calculation.

3. **Problem:** rosbag not recording topics
   **Solution:** Verified topic names using:

```bash
ros2 topic list
```

4. **Problem:** rqt_plot not showing graph
   **Solution:** Ensured correct topic `/turtle1/cmd_vel` and active publishing.

---

## Reflection

This lab enhanced my understanding of ROS 2 system-level tools such as launch files, rosbag, and rqt. I learned how to manage multiple nodes efficiently using launch files and how to record and replay data for analysis. Implementing the follow-the-leader behavior improved my understanding of control systems and topic communication.

Using rqt_plot helped visualize velocity changes in real-time, making it easier to analyze system performance. Overall, this lab provided valuable hands-on experience in building, controlling, and analyzing robotic systems using ROS 2.

---

