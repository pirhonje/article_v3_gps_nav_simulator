import os
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # --------------------------------------------------------------
    # Path to your virtual env's site-packages
    # >>>> CHANGE THIS IF YOUR VENV PATH MOVES <<<<
    # --------------------------------------------------------------
    venv_python_path = '/home/jesse/Desktop/python_projects/utm_venv/venv/lib/python3.10/site-packages'

    # Extend PYTHONPATH so ROS2 can import packages installed in your venv
    os.environ['PYTHONPATH'] = f"{venv_python_path}:{os.environ.get('PYTHONPATH', '')}"

    return LaunchDescription([

        # --------------------------------------------------------------
        # Launch your Pygame telemetry display node
        # executable = *entry point name* from setup.py
        # --------------------------------------------------------------
        Node(
            package='utm_pose_provider',
            executable='vehicle_telemetry',   # <--- uses your entry point
            name='vehicle_telemetry',
            output='screen',
        )

    ])
