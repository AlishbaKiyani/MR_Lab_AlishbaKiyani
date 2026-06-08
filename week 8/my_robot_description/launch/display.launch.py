import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    description_dir = get_package_share_directory("my_robot_description")

    model_arg = DeclareLaunchArgument(
        "model",
        default_value=os.path.join(description_dir, "urdf", "vista_robot.urdf.xacro"),
        description="Absolute path to the robot URDF/Xacro file",
    )

    use_joint_state_publisher_gui_arg = DeclareLaunchArgument(
        "use_joint_state_publisher_gui",
        default_value="false",
        description="Start joint_state_publisher_gui for movable joints",
    )

    use_joint_state_publisher_arg = DeclareLaunchArgument(
        "use_joint_state_publisher",
        default_value="true",
        description="Start joint_state_publisher for movable joints",
    )

    use_rviz_arg = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Start RViz",
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen",
        condition=IfCondition(LaunchConfiguration("use_joint_state_publisher_gui")),
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        output="screen",
        condition=IfCondition(LaunchConfiguration("use_joint_state_publisher")),
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        condition=IfCondition(LaunchConfiguration("use_rviz")),
    )

    return LaunchDescription([
        model_arg,
        use_joint_state_publisher_gui_arg,
        use_joint_state_publisher_arg,
        use_rviz_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node,
    ])
