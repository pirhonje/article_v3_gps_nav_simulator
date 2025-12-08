# GPS Navigation System — README

## Running the Simulator

To start the simulation environment:

```bash
ros2 launch gps_nav simulation_demo.launch.py
```

## Running on the Vehicle

Launch the main vehicle stack:

```bash
ros2 launch gps_nav vehicle.launch.py
```

Launch visualization:

```bash
ros2 launch gps_nav visualization.launch.py
```

## GPS to UTM Conversion (on Vehicle)

To run the GPS→UTM pose provider:

```bash
ros2 launch utm_pose_provider vehicle_pose_publisher.launch.py
```

Python environment required:

```
/home/jesse/Desktop/python_projects/utm_venv
```

## Test Route Data (Rosbag)

Path to the bag file used for testing:

```
/home/jesse/Desktop/article_v3_gps_test/rosbag2_2025_11_20-15_08_39
```

## Creating Goal Points

1. Record GPS data from the vehicle (e.g., `inspvax`).
2. Convert bag to CSV using:

```
/home/jesse/Desktop/python_projects/navigation_help_files/bag_to_csv_nav_gps.py
```

3. Import the generated CSV into **Google My Maps**.
4. Draw/export the route from My Maps as a **KML file**.
5. Convert the KML file to a route format using:

```
/home/jesse/Desktop/python_projects/kml_path/kml_to_route.py
```

## Notes

* Ensure all Python scripts run within their proper virtual environments.
* KML conversion tools may require additional Python dependencies; check within each script for details.
