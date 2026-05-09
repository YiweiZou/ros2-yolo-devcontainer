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
    description='minimal ros2 vision demo without camera',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'pub = vision_demo.publisher_node:main',
            'sub = vision_demo.subscriber_node:main',
        ],
    },
)