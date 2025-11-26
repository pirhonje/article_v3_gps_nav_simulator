import rclpy
from rclpy.node import Node
from std_msgs.msg import String   # Replace with your message types

# An example ROS2 node that subscribes to two topics, processes the data, and publishes the result

class DualProcessorNode(Node):
    def __init__(self):
        super().__init__('dual_processor_node')

        # Storage for latest messages
        self.msg_one = None
        self.msg_two = None

        # Subscribers
        self.sub1 = self.create_subscription(
            String,
            '/topic_one',
            self.callback_one,
            10
        )

        self.sub2 = self.create_subscription(
            String,
            '/topic_two',
            self.callback_two,
            10
        )

        # Publisher
        self.pub = self.create_publisher(String, '/combined_output', 10)

        self.get_logger().info("DualProcessorNode started.")

    def callback_one(self, msg):
        self.msg_one = msg.data
        self.try_publish()

    def callback_two(self, msg):
        self.msg_two = msg.data
        self.try_publish()

    def try_publish(self):
        # Only publish when both messages have arrived at least once
        if self.msg_one is not None and self.msg_two is not None:
            combined_text = f"{self.msg_one} | {self.msg_two}"

            out_msg = String()
            out_msg.data = combined_text

            self.pub.publish(out_msg)
            self.get_logger().info(f"Publishing combined: {combined_text}")


def main(args=None):
    rclpy.init(args=args)
    node = DualProcessorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
