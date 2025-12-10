#!/usr/bin/env python
#
# Copyright (c) 2018-2020 Intel Corporation
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
#
"""
Rosclient class:

Class that handle communication between CARLA and ROS
"""

import carla

import ros_compatibility as roscomp

from carla_ros_client.actor_factory import ActorFactory


def main(args=None):
    """
    main function for carla simulator ROS client
    maintaining the communication client and the CarlaClient object
    """
    roscomp.init("client", args=args)

    actor_factory = None
    carla_world = None
    carla_client = None
    executor = None
    parameters = {}

    executor = roscomp.executors.MultiThreadedExecutor()
    actor_factory = ActorFactory()
    executor.add_node(actor_factory)

    roscomp.on_shutdown(actor_factory.destroy)

    parameters['host'] = actor_factory.get_param('host', 'localhost')
    parameters['port'] = actor_factory.get_param('port', 2000)
    parameters['timeout'] = actor_factory.get_param('timeout', 2)

    actor_factory.loginfo("Trying to connect to {host}:{port}".format(
        host=parameters['host'], port=parameters['port']))

    try:
        carla_client = carla.Client(
            host=parameters['host'],
            port=parameters['port'])
        carla_client.set_timeout(parameters['timeout'])

        carla_world = carla_client.get_world()

        actor_factory.start(carla_world)

        actor_factory.spin()

    except (IOError, RuntimeError) as e:
        actor_factory.logerr("Error: {}".format(e))
    except KeyboardInterrupt:
        pass
    finally:
        roscomp.shutdown()
        del carla_world
        del carla_client


if __name__ == "__main__":
    main()
