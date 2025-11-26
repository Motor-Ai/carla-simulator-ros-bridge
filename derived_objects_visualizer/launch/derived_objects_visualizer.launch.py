import os
import sys

import launch
import launch_ros.actions

def generate_launch_description():
    ld = launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            name='objects_topic',
            default_value='/carla/objects_with_covariance'
        ),
        launch_ros.actions.Node(
            package='derived_objects_visualizer',
            executable='derived_objects_visualizer',
            name='derived_objects_visualizer',
            output='screen',
            emulate_tty=True,
            parameters=[
                {
                    'objects_topic': launch.substitutions.LaunchConfiguration('objects_topic')
                }
            ]
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
