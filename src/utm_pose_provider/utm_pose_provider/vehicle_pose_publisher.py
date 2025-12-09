import math
import rclpy
from rclpy.node import Node

from novatel_oem7_msgs.msg import INSPVA
from geometry_msgs.msg import PoseStamped, Quaternion, TransformStamped
from tf2_ros import TransformBroadcaster
import utm


class VehiclePosePublisher(Node):
    def __init__(self):
        super().__init__('vehicle_pose_publisher')

        # Store latest INSPVA so we can publish at 1 Hz
        self.latest_inspva = None

        # UTM origin for utm_local (set on first message)
        self.origin_easting = None
        self.origin_northing = None

        # TF broadcaster for utm_local -> base_link
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscriber to NovAtel INSPVA
        self.subscription = self.create_subscription(
            INSPVA,
            '/novatel/oem7/inspva',
            self.inspva_callback,
            10
        )

        # Publisher for PoseStamped
        self.publisher = self.create_publisher(PoseStamped, '/vehicle_pose', 10)

        # Timer: publish latest pose + TF at 1 Hz
        self.timer = self.create_timer(0.1, self.publish_latest_pose)

    def inspva_callback(self, msg: INSPVA):
        """Just store the most recent INSPVA message."""
        self.latest_inspva = msg

    def publish_latest_pose(self):
        """Publish PoseStamped and TF at 1 Hz using the latest INSPVA."""
        if self.latest_inspva is None:
            return  # no data yet

        msg = self.latest_inspva

        # Extract raw GPS + heading
        lat = msg.latitude
        lon = msg.longitude
        heading_deg = msg.azimuth

        # Convert lat/lon → UTM (global)
        easting, northing, zone, letter = utm.from_latlon(lat, lon)

        # Initialize utm_local origin on first message
        if self.origin_easting is None:
            self.origin_easting = easting
            self.origin_northing = northing
            self.get_logger().info(
                f"Initialized utm_local origin at E={easting:.3f}, N={northing:.3f}"
            )

        # Convert to utm_local (relative to origin)
        local_easting = easting #- self.origin_easting
        local_northing = northing #- self.origin_northing

        # Convert heading → quaternion (yaw-only)
        #yaw = math.radians(heading_deg)
        yaw = math.radians(90.0 - heading_deg)
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)

        # Construct PoseStamped in utm_local frame
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        #pose_msg.header.frame_id = "utm_local"   # <<< important #9.12
        pose_msg.header.frame_id = "utm"

        pose_msg.pose.position.x = local_easting
        pose_msg.pose.position.y = local_northing
        pose_msg.pose.position.z = 0.0

        pose_msg.pose.orientation = q

        # Publish pose at 1 Hz
        self.publisher.publish(pose_msg)

        # Also publish TF: utm_local -> base_link
        t = TransformStamped()
        t.header.stamp = pose_msg.header.stamp
        
        #t.header.frame_id = "utm_local" # <<< important #9.12
        #t.child_frame_id = "base_link" # <<< important #9.12   
        t.header.frame_id = "utm"
        t.child_frame_id = "vehicle"


        t.transform.translation.x = local_easting
        t.transform.translation.y = local_northing
        t.transform.translation.z = 0.0
        t.transform.rotation = q

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = VehiclePosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
