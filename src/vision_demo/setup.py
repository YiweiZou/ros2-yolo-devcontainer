from setuptools import setup

package_name = 'vision_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='ROS2 vision demo with YOLO inference',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [
            'pub = vision_demo.publisher_node:main',
            'yolo = vision_demo.yolo_node:main',
        ],
    },
)