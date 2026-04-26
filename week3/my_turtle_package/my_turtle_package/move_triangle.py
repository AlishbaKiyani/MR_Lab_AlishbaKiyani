import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class TrianglePublisher(Node):
    def __init__(self):
        super().__init__('triangle_publisher')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        # Triangle sides and turns: (linear_x, angular_z, duration)
        # Linear speed = 2, angular speed = 1.57 rad/sec for 90 deg approx
        # For triangle: turn 120 degrees = 2.09 rad
        self.steps = [
            (2.0, 0.0, 2.0),   # Side 1
            (0.0, 2.09, 1.0),  # Turn 120 deg
            (2.0, 0.0, 2.0),   # Side 2
            (0.0, 2.09, 1.0),  # Turn 120 deg
            (2.0, 0.0, 2.0),   # Side 3
            (0.0, 2.09, 1.0),  # Turn 120 deg to original heading
        ]

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.step_index = 0

    def timer_callback(self):
        linear_x, angular_z, duration = self.steps[self.step_index]

        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher_.publish(msg)

        # Sleep for the duration of this step
        time.sleep(duration)

        # Move to next step
        self.step_index = (self.step_index + 1) % len(self.steps)

def main(args=None):
    rclpy.init(args=args)
    node = TrianglePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
