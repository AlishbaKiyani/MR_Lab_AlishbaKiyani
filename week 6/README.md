# reactive_navigation

**MCT-454L Mobile Robotics — Lab 6: Reactive Navigation Using TurtleBot3 LiDAR**

A ROS 2 Python package that implements LiDAR-based reactive navigation for the TurtleBot3 Burger robot in a Gazebo simulation. The node reads `/scan` data, partitions the 360° scan into directional regions, and publishes velocity commands to `/cmd_vel` to detect obstacles and avoid collisions.


## Overview

This package implements **reactive navigation** — a paradigm in which a robot makes real-time motion decisions purely from raw sensor data, without using maps or pre-planned paths. The `lidar_navigator` node:

1. Subscribes to the `/scan` topic (`sensor_msgs/msg/LaserScan`)
2. Cleans invalid range values (`inf`, `NaN`)
3. Partitions the 360° scan into **front**, **left**, and **right** regions
4. Computes the minimum distance in each region
5. Publishes `Twist` commands to `/cmd_vel` (`geometry_msgs/msg/Twist`) based on obstacle proximity

---

## Package Structure

```
reactive_navigation/
├── reactive_navigation/
│   ├── __init__.py
│   └── lidar_navigator.py      # Main navigation node
├── resource/
│   └── reactive_navigation
├── test/
├── package.xml
├── setup.cfg
├── setup.py
└── README.md
```

---

## Dependencies

| Dependency        | Purpose                              |
|-------------------|--------------------------------------|
| `rclpy`           | ROS 2 Python client library          |
| `sensor_msgs`     | `LaserScan` message type             |
| `geometry_msgs`   | `Twist` message type                 |
| `numpy`           | Efficient array processing of ranges |
| `python3-pytest`  | Testing (dev dependency)             |

Make sure you have **ROS 2 Humble** (or compatible) and **TurtleBot3** packages installed:

```bash
sudo apt install ros-humble-turtlebot3 ros-humble-turtlebot3-gazebo
```

---

## Build & Install

```bash
# Navigate to your ROS 2 workspace
cd ~/ros2_ws_alishba

# Build
colcon build --packages-select reactive_navigation

# Source the workspace
source install/setup.bash
```

---

## Running the Node

### 1. Launch the Gazebo Simulation

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

### 2. Run the LiDAR Navigator Node

```bash
ros2 run reactive_navigation lidar_navigator
```

### 3. (Optional) Visualize in RViz2

```bash
ros2 run rviz2 rviz2
```

Add the `/scan` topic as a `LaserScan` display in RViz2 to visualize the sensor data.

---

## Node Details

### Scan Processing

Raw LiDAR ranges are loaded into a NumPy array. Invalid readings (`inf` and `NaN`) are replaced with a safe maximum value of **3.5 m** (typical LiDAR max range):

```python
ranges = np.where(np.isfinite(ranges), ranges, 3.5)
```

This prevents division-by-zero and ensures stable minimum-distance calculations.

### Region Definitions

The TurtleBot3 LiDAR produces a full 360° scan where **index 0 points forward** and indices increase counter-clockwise:

| Region | Index Range              | Angular Coverage |
|--------|--------------------------|-----------------|
| Front  | `[0:20]` + `[340:360]`   | ±20° of forward |
| Left   | `[60:120]`               | ~60°–120° left  |
| Right  | `[240:300]`              | ~240°–300° (right side) |

```python
front = np.concatenate([ranges[0:20], ranges[340:360]])
left  = ranges[60:120]
right = ranges[240:300]
```

Minimum distance per region is used to represent the closest obstacle:

```python
front_dist = float(np.min(front))
left_dist  = float(np.min(left))
right_dist = float(np.min(right))
```

### Navigation Logic

```
if front_dist < front_threshold (0.5 m):
    ├── if left_dist > right_dist  → turn LEFT  (angular.z = +0.5 rad/s)
    └── else                       → turn RIGHT (angular.z = -0.5 rad/s)
    linear.x = 0.0  (stop while turning)
else:
    linear.x  = 0.0  (default: stationary — extend for forward motion)
    angular.z = 0.0
```

> **Note:** The current implementation focuses on obstacle detection and avoidance turning. Extend `twist.linear.x = 0.15` in the `else` branch to enable continuous forward motion for wall-following.

---

## Key Parameters

| Parameter          | Value   | Description                                    |
|--------------------|---------|------------------------------------------------|
| `front_threshold`  | `0.5 m` | Stop/turn if obstacle is closer than this      |
| `side_threshold`   | `0.4 m` | Target wall-following distance (left/right)    |
| Turn speed         | `±0.5 rad/s` | Angular velocity during avoidance turn    |
| Max replace value  | `3.5 m` | Value used to replace `inf`/`NaN` readings     |

---

## Helpful Commands

```bash
# Verify LiDAR topic is publishing
ros2 topic list
ros2 topic echo /scan

# Monitor velocity commands being published
ros2 topic echo /cmd_vel

# View the node graph (requires rqt)
ros2 run rqt_graph rqt_graph

# Check node info
ros2 node info /lidar_navigator
```

---

## Lab Tasks Coverage

| Task | Description                          | Status |
|------|--------------------------------------|--------|
| Task 1 | Scan processing & region extraction |  Complete |
| Task 2 | Stop-on-obstacle (front threshold)  |  Complete |
| Task 3 | Obstacle avoidance with turn direction | Complete |
| Task 4 | Wall following (proportional control) | Extendable via `side_threshold` |
| Task 5 | Behavior sequencing                  | Extendable |

---

## Author

**Alishba Kiyani**
Email: alishbakiyani75@gmail.com
Course: MCT-454L Mobile Robotics — Lab 6

