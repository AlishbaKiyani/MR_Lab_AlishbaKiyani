# my_robot_description

A ROS 2 package containing URDF robot descriptions and launch files for visualizing robots in RViz. This package covers two robots:
1. **my_robot** — a simple custom mobile robot built from primitive shapes
2. **Vista** — a full differential-drive museum tour robot with real STL meshes

---

## Package Structure

```
my_robot_description/
├── urdf/
│   ├── my_robot.urdf               # Simple custom robot (primitives)
│   └── vista_robot.urdf.xacro      # Vista museum robot (STL meshes)
├── meshes/
│   ├── base_link.STL
│   ├── right_wheel_link.STL
│   ├── left_wheel_link.STL
│   └── lidar_link.STL
├── launch/
│   └── display.launch.py
└── rviz/
```

---

##  Dependencies

Make sure the following ROS 2 packages are installed:

```bash
sudo apt install ros-$ROS_DISTRO-robot-state-publisher \
                 ros-$ROS_DISTRO-joint-state-publisher \
                 ros-$ROS_DISTRO-joint-state-publisher-gui \
                 ros-$ROS_DISTRO-xacro \
                 ros-$ROS_DISTRO-rviz2
```

---

##  Build

Run from the **workspace root**:

```bash
cd ~/ros2_ws_alishba
colcon build --packages-select my_robot_description
source install/setup.bash
```

---

## 1️ My Robot — `my_robot.urdf`

### About

`my_robot.urdf` is a minimal mobile robot model built entirely from **primitive geometric shapes** (no STL meshes required). It serves as the starting point for understanding URDF structure and ROS 2 transforms.

### Robot Structure

| Link | Shape | Size | Color |
|---|---|---|---|
| `base_link` | Box | 0.4 × 0.3 × 0.1 m | Blue |
| `camera` | Cylinder | radius 0.05 m, length 0.05 m | Black |

### Joint Summary

| Joint | Type | Parent → Child | Offset |
|---|---|---|---|
| `base_camera_joint` | fixed | `base_link` → `camera` | xyz: 0.15 0.0 0.1 |

The camera is fixed at the **front-top** of the base body.

### How to Run

**Option A — Directly with `robot_state_publisher`:**

```bash
# Source your workspace first
source ~/ros2_ws_alishba/install/setup.bash

# Run from the package share directory
ros2 run robot_state_publisher robot_state_publisher \
  --ros-args -p robot_description:="$(cat ~/ros2_ws_alishba/install/my_robot_description/share/my_robot_description/urdf/my_robot.urdf)"
```

Then open RViz in a separate terminal:

```bash
rviz2
```

**Option B — Via the launch file (pointing to my_robot.urdf):**

```bash
ros2 launch my_robot_description display.launch.py \
  model:=$(ros2 pkg prefix my_robot_description)/share/my_robot_description/urdf/my_robot.urdf
```

### RViz Setup

1. Set **Fixed Frame** → `base_link`
2. Click **Add** → **RobotModel** → OK
3. Set **Description Topic** → `/robot_description`
4. The blue box body and black cylinder camera will appear

---

## 2️ Custom Robot

The **custom robot** extends the basic `my_robot.urdf` concept by demonstrating how to design your own unique robot configuration from scratch using only URDF primitives — no external mesh files, no CAD software needed.

### Design Principles

- **Links** are defined using primitive shapes: `<box>`, `<cylinder>`, `<sphere>`
- **Joints** connect links with defined types: `fixed`, `revolute`, `continuous`, `prismatic`
- **Materials** assign colors using RGBA values
- **Origins** set position (`xyz`) and orientation (`rpy`) of each link/joint

### URDF Primitives Reference

| Element | Purpose | Example |
|---|---|---|
| `<box size="L W H"/>` | Rectangular body | chassis, platforms |
| `<cylinder radius="R" length="L"/>` | Round shapes | wheels, cameras, sensors |
| `<sphere radius="R"/>` | Ball shapes | caster wheels |

### Key Concepts

```xml
<!-- A link with a visual primitive -->
<link name="base_link">
  <visual>
    <geometry>
      <box size="0.4 0.3 0.1"/>
    </geometry>
    <material name="blue">
      <color rgba="0 0 1 1"/>
    </material>
  </visual>
</link>

<!-- A joint connecting two links -->
<joint name="base_camera_joint" type="fixed">
  <parent link="base_link"/>
  <child link="camera"/>
  <origin xyz="0.15 0 0.1" rpy="0 0 0"/>
</joint>
```

### How to Visualize Any Custom URDF

```bash
# Build first
cd ~/ros2_ws_alishba
colcon build --packages-select my_robot_description
source install/setup.bash

# Launch with your custom URDF file
ros2 launch my_robot_description display.launch.py \
  model:=/absolute/path/to/your_robot.urdf
```

### Verify the TF Tree

```bash
# In a separate terminal
ros2 run tf2_tools view_frames
```

This generates a `frames.pdf` in the current directory showing all parent → child frame relationships.

---

## 3️ Vista Robot — `vista_robot.urdf.xacro`

### About

Vista is a **differential-drive museum tour robot** with a full physical model using real **STL mesh files** exported from SolidWorks/Fusion 360. It includes full inertial properties for realistic physics simulation and is designed to navigate museum galleries autonomously.

### Robot Links

| Link | Type | Description |
|---|---|---|
| `base_footprint` | Dummy (empty) | Root frame at ground level |
| `base_link` | Mesh (STL) | Main robot body chassis |
| `right_wheel_link` | Mesh (STL) | Right continuous-rotation drive wheel |
| `left_wheel_link` | Mesh (STL) | Left continuous-rotation drive wheel |
| `lidar_link` | Mesh (STL) | 2D LiDAR sensor mounted on top |

### Joint Summary

| Joint | Type | Parent → Child | Notes |
|---|---|---|---|
| `base_joint` | fixed | `base_footprint` → `base_link` | Raises body 41 mm off ground |
| `right_wheel_joint` | continuous | `base_link` → `right_wheel_link` | Drive wheel, y = −0.191 m |
| `left_wheel_joint` | continuous | `base_link` → `left_wheel_link` | Drive wheel, y = +0.191 m |
| `lidar_joint` | fixed | `base_link` → `lidar_link` | Sensor at top of chassis |

### Physical Properties

| Component | Mass |
|---|---|
| Base body | 1.895 kg |
| Each drive wheel | 2.999 kg |
| LiDAR sensor | 1.335 kg |

> All links include full `<inertial>` blocks (mass + inertia tensor) and `<collision>` geometry for physics simulation.

### How to Launch in RViz

**Default launch (Vista robot):**

```bash
ros2 launch my_robot_description display.launch.py
```

This starts:
- `robot_state_publisher` — processes the xacro file and publishes URDF to `/robot_description`
- `joint_state_publisher` — publishes joint states for the two continuous wheel joints
- `rviz2` — opens the visualization window

### Launch Arguments

| Argument | Default | Description |
|---|---|---|
| `model` | `vista_robot.urdf.xacro` | Path to URDF/Xacro file |
| `use_joint_state_publisher` | `true` | Auto-publish joint states |
| `use_joint_state_publisher_gui` | `false` | Enable GUI sliders for joints |
| `use_rviz` | `true` | Launch RViz |

**Launch with GUI joint sliders** (to manually rotate wheels):

```bash
ros2 launch my_robot_description display.launch.py \
  use_joint_state_publisher_gui:=true \
  use_joint_state_publisher:=false
```

**Launch without RViz** (headless):

```bash
ros2 launch my_robot_description display.launch.py use_rviz:=false
```

### RViz Setup (First Time)

1. Set **Fixed Frame** → `base_footprint`
2. Click **Add** → **RobotModel** → OK
3. Set **Description Topic** → `/robot_description`
4. Vista robot will appear with all four STL meshes rendered

### Vista AI Capabilities

Vista is not just a URDF model — it runs a full **voice-activated AI tour assistant**:

-  **Wake word** — "Hey Vista" activates the assistant
-  **Gallery navigation** — voice-commanded Nav2 autonomous navigation to museum galleries
-  **AI Q&A** — powered by Google Gemini Flash for dynamic, context-aware visitor answers
-  **Multilingual** — supports English and Urdu language switching
- **TTS** — Edge-TTS neural voice for natural speech output

---

##  Verify TF Tree

In a separate terminal, inspect the transform tree:

```bash
ros2 run tf2_tools view_frames
```

This generates a `frames.pdf` in the current directory showing all parent-child frame relationships.

---

##  Maintainer

**Alishba Kiyani** — alishbakiyani75@gmail.com
