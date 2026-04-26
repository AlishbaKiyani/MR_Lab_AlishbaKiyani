from setuptools import setup, find_packages

package_name = 'my_turtle_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alishbakiyani',
    maintainer_email='alishbakiyani75@gmail.com',
    description='ROS2 package to move turtlesim',
    license='Apache License 2.0',
   entry_points={
    'console_scripts': [
        'move_turtle = my_turtle_package.move_turtle:main',
        'move_circle = my_turtle_package.move_circle:main',
        'move_triangle = my_turtle_package.move_triangle:main',
        'three_turtles = my_turtle_package.three_turtles:main',
        'move_to_location = my_turtle_package.move_to_location:main'
    ],
}
    
)
