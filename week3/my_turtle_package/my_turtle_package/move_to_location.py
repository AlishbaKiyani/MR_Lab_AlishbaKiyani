import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class MoveToLocation(Node):

    def __init__(self):
        super().__init__('move_to_location')

        # Publisher for velocity
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Subscriber for pose
        self.subscriber_ = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        # Timer
        self.timer = self.create_timer(0.1, self.move_to_goal)

        self.pose = Pose()

        # Target position
        self.goal_x = 7.0
        self.goal_y = 2.0


    def pose_callback(self, msg):
        self.pose = msg


    def move_to_goal(self):
        msg = Twist()

        # Distance error
        distance = math.sqrt(
            (self.goal_x - self.pose.x) ** 2 +
            (self.goal_y - self.pose.y) ** 2
        )

        # Angle to goal
        angle_to_goal = math.atan2(
            self.goal_y - self.pose.y,
            self.goal_x - self.pose.x
        )

        # Angle error (normalized)
        angle_error = angle_to_goal - self.pose.theta
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))

        # ONLY move to position (NO orientation fix)
        if distance > 0.05:
            msg.linear.x = 1.5 * distance
            msg.angular.z = 4.0 * angle_error

        else:
            # STOP immediately
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)

            self.get_logger().info("Reached Goal (7,2) ")
            self.timer.cancel()
            return

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MoveToLocation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
