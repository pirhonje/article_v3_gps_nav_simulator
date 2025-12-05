import math
import rclpy
from rclpy.node import Node

from novatel_oem7_msgs.msg import INSPVA
from geometry_msgs.msg import PoseStamped, Quaternion
import utm


class VehiclePosePublisher(Node):
    def __init__(self):
        super().__init__('vehicle_pose_publisher')

        # Subscriber to NovAtel INSPVA
        self.subscription = self.create_subscription(
            INSPVA,
            '/novatel/oem7/inspva',  # <= change to your actual topic
            self.inspva_callback,
            10
        )

        # Publisher for PoseStamped
        self.publisher = self.create_publisher(PoseStamped, '/vehicle_pose', 10)

    def inspva_callback(self, msg: INSPVA):
        # Extract raw GPS + heading
        lat = msg.latitude
        lon = msg.longitude
        heading_deg = msg.azimuth

        # Convert lat/lon → UTM
        easting, northing, zone, letter = utm.from_latlon(lat, lon)

        # Convert heading → quaternion (yaw-only)
        yaw = math.radians(heading_deg)
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)

        # Construct PoseStamped
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = "utm"

        pose_msg.pose.position.x = easting
        pose_msg.pose.position.y = northing
        pose_msg.pose.position.z = 0.0   # if no altitude needed

        pose_msg.pose.orientation = q

        # Publish
        self.publisher.publish(pose_msg)


def main(args=None):
    rclpy.init(args=args)
    node = VehiclePosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
