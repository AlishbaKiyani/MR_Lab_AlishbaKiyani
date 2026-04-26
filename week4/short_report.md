## Short Report: Approach, Findings, and Observations

### Approach

In this lab, the ROS 2 launch system was used to run multiple nodes simultaneously within the turtlesim environment. A custom launch file (`two_turtles_launch.py`) was created to start the main simulator and teleoperation node together. After setting up the environment, a second turtle was spawned to extend the simulation to a multi-agent system.

To implement interaction between robots, a follow-the-leader behavior was developed in `follow_leader.py`. This node subscribed to `/turtle1/pose` and used the received position data to generate velocity commands for `/turtle2/cmd_vel`. A basic proportional control strategy was applied to adjust linear and angular velocities based on distance and heading error between the two turtles.

For data acquisition, rosbag was used to record important topics such as `/turtle1/pose`, `/turtle1/cmd_vel`, and `/turtle2/cmd_vel`. The recorded data was later replayed to analyze system behavior. Additionally, rqt_plot was used to visualize the `/turtle1/cmd_vel` topic in real time to understand how velocity commands change during motion.

---

### Findings

* ROS 2 launch files significantly simplify the execution of multiple nodes by reducing manual terminal operations.
* The follow-the-leader behavior successfully demonstrated basic inter-node communication using topics.
* The second turtle was able to track the first turtle with acceptable delay and smoothness when proportional control was applied.
* Rosbag effectively captured all topic data, allowing accurate playback of robot motion for debugging and analysis.
* rqt_plot provided clear visualization of velocity variations, helping in understanding motion dynamics of the turtle.

---

### Observations

* Small delays were observed in the follower turtle due to processing and message publishing rates.
* If proportional gain values were too high, the follower became unstable and overshot the leader’s path.
* Lower gain values resulted in smoother but slower tracking behavior.
* The rosbag replay accurately replicated the recorded motion, confirming correct data logging.
* Visualization through rqt_plot made it easier to correlate velocity commands with actual turtle movement.

---

### Conclusion

This lab improved understanding of ROS 2 system integration, especially in launching multiple nodes, inter-process communication, and data recording. The follow-the-leader implementation demonstrated how simple control logic can create coordinated multi-robot behavior. Overall, the lab strengthened practical skills in ROS 2-based robotic simulation, debugging, and data analysis.

