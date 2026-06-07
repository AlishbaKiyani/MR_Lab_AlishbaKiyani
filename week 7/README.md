# autonomous_navigation

Lab 7 — MCT-454L Mobile Robotics  
ROS 2 Humble | TurtleBot3 Burger | Gazebo + Nav2

---

## What this is

This package was built for Lab 7 of the Mobile Robotics course. The goal was to get a TurtleBot3 navigating autonomously through a set of waypoints using the Nav2 stack, with AMCL handling localization on a pre-built map.

The main node is `waypoint_navigator.py`. It sends goals to Nav2 one at a time using the `NavigateToPose` action server, waits for the robot to actually reach each point, pauses for 2 seconds, then moves on to the next one.

---

## Package structure

```
autonomous_navigation/
├── autonomous_navigation/
│   └── waypoint_navigator.py   # main navigation node
├── package.xml
├── setup.py
└── README.md
```

---

## Setup

Make sure you have TurtleBot3 and Nav2 installed. Source your workspace before running anything.

```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws_alishba/install/setup.bash
export TURTLEBOT3_MODEL=burger
```

Build the package (only needed if you change something):

```bash
cd ~/ros2_ws_alishba
colcon build --packages-select autonomous_navigation --symlink-install
```

---

## How to run

You need three things running before launching the navigator:

**Terminal 1 — Gazebo simulation**
```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

**Terminal 2 — Nav2 + AMCL**
```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map.yaml
```

**Terminal 3 — RViz** (set the 2D Pose Estimate here before running the navigator)
```bash
ros2 launch nav2_bringup rviz_launch.py
```

Once everything is up and you've set the initial pose in RViz:

**Terminal 4 — Run the navigator**
```bash
ros2 run autonomous_navigation waypoint_navigator
```

---

## Task 2 — Hardcoded waypoints

Five waypoints were picked after running the simulation and checking positions via `ros2 topic echo /amcl_pose`. These were chosen to avoid the obstacles in the default turtlebot3_world layout.

| # | x | y | Notes |
|---|---|---|-------|
| 1 | 1.20 | -1.27 | first corridor, slight left |
| 2 | 2.77 | -1.18 | further down same corridor |
| 3 | 3.74 | -0.47 | turning right toward center |
| 4 | 3.80 | 0.27 | upper right area |
| 5 | 2.69 | 2.48 | top section of the map |

The robot waits 2 seconds at each waypoint before continuing. That's controlled by `DWELL_SEC = 2.0` near the top of the file — easy to change.

---

## Task 3 — Passing waypoints from the command line

Instead of editing the file every time, you can pass waypoints directly when running the node. Each group of three numbers is `x y orientation_w` for one waypoint.

```bash
ros2 run autonomous_navigation waypoint_navigator 1.20 -1.27 0.99 2.77 -1.18 0.99 3.74 -0.47 0.80
```

If you pass nothing, it falls back to the five hardcoded waypoints from Task 2. If you give it a number of arguments that isn't divisible by 3, it'll print an error and exit cleanly.

---

## Task 4 — Costmap topics

To see all the costmap-related topics:

```bash
ros2 topic list | grep costmap
```

The ones that matter:

- `/global_costmap/costmap` — the full occupancy grid used by the global planner to find a path from start to goal. Updated from the static map plus sensor data.
- `/local_costmap/costmap` — a smaller rolling window (~4m around the robot) that updates in real time from the lidar. This is what the local planner uses to avoid obstacles moment to moment.

The clearest way to see the inflation in action is to add both costmap topics as Map displays in RViz and navigate the robot near a wall. You'll see the color gradient expanding outward from the obstacle — that's the inflation layer making sure the robot keeps a safe distance.

```bash
# Check what inflation radius is set to
ros2 param get /local_costmap/local_costmap inflation_layer.inflation_radius
```

---

## Task 5 — Recovery behaviors

To test this: while the robot is navigating, go into Gazebo, click the insert tab, drag a box into the robot's planned path, and watch what happens.

Nav2 handles it through a behavior tree managed by `/bt_navigator`. When the local planner can't find a valid path, it hands off to the `/behavior_server`, which tries a sequence of recoveries:

1. First it tries to replan the global path around the obstacle
2. If that doesn't work, it spins in place to refresh the costmap readings
3. Then it may back up slightly and try again

To watch it live:

```bash
# See which behavior is active
ros2 topic echo /behavior_server/transition_event

# Open rqt_graph to see the full node connection
rqt_graph
```

In rqt_graph, look for connections between `/bt_navigator`, `/behavior_server`, `/controller_server`, and `/planner_server`. The bt_navigator is the one deciding which recovery to trigger based on the behavior tree logic.

---

## Notes

- Always set the **2D Pose Estimate** in RViz before sending any goals, otherwise AMCL won't know where the robot is and navigation will fail or drift badly.
- If the robot gets stuck and the terminal freezes, Ctrl+C the navigator and re-run — the Nav2 stack keeps running.
- The `--symlink-install` flag means you don't need to rebuild every time you edit the Python file.
- Tested on ROS 2 Humble with turtlebot3_world map.

---

**Course:** MCT-454L Mobile Robotics  
**Maintainer:** alishbakiyani — alishbakiyani75@gmail.com
