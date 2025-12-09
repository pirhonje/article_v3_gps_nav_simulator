from setuptools import find_packages, setup

package_name = 'utm_pose_provider'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        #launch definition for vehicle pose
        ('share/' + package_name + '/launch',
            ['launch/vehicle_pose_publisher.launch.py']),
        #launch definition for vehicle telemetry display
        ('share/' + package_name + '/launch',
            ['launch/vehicle_telemetry.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jesse',
    maintainer_email='jessek.pirhonen@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # executable name   =   python path to file : function
            'vehicle_pose_publisher = utm_pose_provider.vehicle_pose_publisher:main',
            'vehicle_telemetry = utm_pose_provider.vehicle_telemetry:main',
        ],
    },
)
