#!/usr/bin/env python3

import sys
import pygame
import math
import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped


class AckermannDisplay(Node):
    def __init__(self):
        super().__init__('ackermann_display')

        self.sub = self.create_subscription(
            AckermannDriveStamped,
            '/vehicle_command_ackermann',
            self.callback,
            10
        )

        self.latest_angle = None
        self.latest_speed = None

    def callback(self, msg):
        self.latest_angle = msg.drive.steering_angle
        self.latest_speed = msg.drive.speed


def main(args=None):
    rclpy.init(args=args)
    node = AckermannDisplay()

    # ---------------------------------------------------------
    # CHOOSE YOUR WINDOW SIZE HERE (width, height)
    WINDOW_WIDTH = 400
    WINDOW_HEIGHT = 200
    # ---------------------------------------------------------

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ackermann Data Display")
    font = pygame.font.SysFont(None, 40)

    clock = pygame.time.Clock()
    running = True

    while running:
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spin ROS2 node
        rclpy.spin_once(node, timeout_sec=0.01)

        # Draw background
        screen.fill((20, 20, 20))

        # ---------------------------------------------------------
        # DISPLAY steering_angle AND speed
        # (You can change font size, position, or text color below)
        # ---------------------------------------------------------
        if node.latest_angle is None:
            text = font.render("Waiting for messages...", True, (200, 200, 200))
            screen.blit(text, (20, 80))
        else:
             angle_rad = node.latest_angle
             angle_deg = math.degrees(angle_rad)
             
             angle_rad_text = font.render(f"Steering (rad): {angle_rad:.3f}", True, (255, 255, 255))
             angle_deg_text = font.render(f"Steering (deg): {angle_deg:.1f}", True, (255, 255, 255))
             speed_text     = font.render(f"Speed   (m/s): {node.latest_speed:.3f}", True, (255, 255, 255))
             
             screen.blit(angle_rad_text, (20, 30))
             screen.blit(angle_deg_text, (20, 80))
             screen.blit(speed_text,     (20, 130))

        pygame.display.flip()
        clock.tick(30)  # Limit FPS

    pygame.quit()
    node.destroy_node()
    rclpy.shutdown()
    sys.exit(0)


if __name__ == '__main__':
    main()
