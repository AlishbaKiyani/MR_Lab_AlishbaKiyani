from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction, ExecuteProcess

def generate_launch_description():
    return LaunchDescription([

        # Turtlesim
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim'
        ),

        # Teleop for turtle1
        Node(
            package='turtlesim',
            executable='turtle_teleop_key',
            name='teleop1',
            prefix='xterm -e',
            remappings=[
                ('/turtle1/cmd_vel', '/turtle1/cmd_vel')
            ]
        ),

        # Spawn turtle2
        TimerAction(
            period=2.0,
            actions=[
                ExecuteProcess(
                    cmd=[
                        'ros2', 'service', 'call',
                        '/spawn',
                        'turtlesim/srv/Spawn',
                        "{x: 5.0, y: 5.0, theta: 0.0, name: 'turtle2'}"
                    ],
                    output='screen'
                )
            ]
        ),

        # Teleop for turtle2 (second xterm)
        TimerAction(
            period=3.0,
            actions=[
                Node(
                    package='turtlesim',
                    executable='turtle_teleop_key',
                    name='teleop2',
                    prefix='xterm -e',
                    remappings=[
                        ('/turtle1/cmd_vel', '/turtle2/cmd_vel')
                    ]
                )
            ]
        )

    ])
