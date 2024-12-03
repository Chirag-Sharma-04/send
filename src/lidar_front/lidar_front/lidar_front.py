import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class RPLidarFilterNode(Node):
    def __init__(self):
        super().__init__('rplidar_filter_node')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(LaserScan, '/filtered_scan', 10)

        # Define the desired angular range (adjust as needed)
        self.min_angle = -45 * (3.14159 / 180)  # -45 degrees
        self.max_angle = 45 * (3.14159 / 180)   # 45 degrees

    def listener_callback(self, msg):
        # Filter the scan data
        filtered_scan = self.filter_scan(msg)
        self.publisher.publish(filtered_scan)

    def filter_scan(self, scan_msg):
        filtered_ranges = []
        filtered_intensities = []

        for i in range(len(scan_msg.ranges)):
            angle = scan_msg.angle_min + i * scan_msg.angle_increment
            if self.min_angle <= angle <= self.max_angle:
                filtered_ranges.append(scan_msg.ranges[i])
                filtered_intensities.append(scan_msg.intensities[i])

        # Create a new LaserScan message with the filtered data
        filtered_scan = LaserScan()
        filtered_scan.header = scan_msg.header
        filtered_scan.angle_min = self.min_angle
        filtered_scan.angle_max = self.max_angle
        filtered_scan.angle_increment = scan_msg.angle_increment
        filtered_scan.time_increment = scan_msg.time_increment
        filtered_scan.range_min = scan_msg.range_min
        filtered_scan.range_max = scan_msg.range_max
        filtered_scan.ranges = filtered_ranges
        filtered_scan.intensities = filtered_intensities

        return filtered_scan

def main(args=None):
    rclpy.init(args=args)
    node = RPLidarFilterNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()