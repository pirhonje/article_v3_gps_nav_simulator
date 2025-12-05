import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Path to your virtual env's site-packages
    venv_python_path = '/home/jesse/Desktop/python_projects/utm_venv/venv/lib/python3.10/site-packages'

    # Extend PYTHONPATH so the node can see utm from the venv
    os.environ['PYTHONPATH'] = f"{venv_python_path}:{os.environ.get('PYTHONPATH', '')}"

    return LaunchDescription([
        Node(
            package='utm_pose_provider',
            executable='vehicle_pose_publisher',
            name='vehicle_pose_publisher',
            output='screen',
        )
    ])
