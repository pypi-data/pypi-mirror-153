"""Mobil behavior model for CommonRoad agents.

Authors: Matthias Rowold <matthias.rowold@tum.de> & Konstantin Ikonomou
"""


from commonroad.scenario.scenario import Scenario
from commonroad_helper_functions.spacial import lanelet2spline
from commonroad_helper_functions.spacial import (
    get_left_lanelet,
    get_right_lanelet,
    get_follower_on_lanelet,
    get_leader_on_lanelet,
)
from commonroad_helper_functions.visualization import get_plot_limits_from_scenario
from commonroad.visualization.draw_dispatch_cr import draw_object

import numpy as np
from matplotlib import pyplot as plt
import os
import sys
from agent_sim.agent import Agent

module_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(module_path)


class MOBILAgent(Agent):
    """
    Class to model MOBIL behaviour. Second version.
    """

    def __init__(
        self,
        scenario: Scenario,
        agent_id: int,
        enable_logging: bool = True,
        log_path: str = '/log',
        debug_step: bool = False,
        idm_parameters: dict = {
            'v_0': 20,
            's_0': 4,
            'T': 2,
            'a_max': 4,
            'a_min': -8,
            'b': 1.5,
            'delta': 4,
        },
        mobil_parameters: dict = {
            'b_safe': 2,
            'p': 0.1,
            'a_th': 0.1,
            'a_bias': 0.3,
            'v_crit': 10,
        },
    ):
        # parent class
        super().__init__(
            scenario=scenario,
            agent_id=agent_id,
            enable_logging=enable_logging,
            log_path=log_path,
            debug_step=debug_step,
        )

        self.__idm_parameters = idm_parameters
        self.__mobil_parameters = mobil_parameters

        # parent class
        super().__init__(
            scenario=scenario,
            agent_id=agent_id,
            enable_logging=enable_logging,
            log_path=log_path,
            debug_step=debug_step,
        )

        self.__idm_parameters = idm_parameters
        self.__mobil_parameters = mobil_parameters

    def _step_agent(self, delta_time):
        """Step function for MOBIL agent."""
        # --------------------------------------------------------------------------------------------------------------
        # ALL LEADERS AND ALL FOLLOWERS
        # --------------------------------------------------------------------------------------------------------------

        # get current ego lanelet
        ego_lanelet = self.scenario.lanelet_network.find_lanelet_by_id(
            self.current_lanelet_id
        )

        # approximate center lane with cubic spline
        ego_lanelet_spline = lanelet2spline(lanelet=ego_lanelet)

        # calculate arclength of ego vehicle at current position
        self.ego_arclength = ego_lanelet_spline.get_min_arc_length(self.state.position)[
            0
        ]

        # Get all positions (arc length along the corresponding lanelet) and velocity of leaders and followers on the
        # current, left, and right lanelet
        (
            leader_id,
            leader_arclength,
            leader_distance,
            leader_velocity,
            leader_approaching_rate,
            follower_id,
            follower_arclength,
            follower_distance,
            follower_velocity,
            follower_approaching_rate,
            left_leader_id,
            left_leader_arclength,
            left_leader_distance,
            left_leader_velocity,
            left_leader_approaching_rate,
            left_follower_id,
            left_follower_arclength,
            left_follower_distance,
            left_follower_velocity,
            left_follower_approaching_rate,
            right_leader_id,
            right_leader_arclength,
            right_leader_distance,
            right_leader_velocity,
            right_leader_approaching_rate,
            right_follower_id,
            right_follower_arclength,
            right_follower_distance,
            right_follower_velocity,
            right_follower_approaching_rate,
        ) = self.__get_all_follower_and_leader_info()

        # --------------------------------------------------------------------------------------------------------------
        # BEFORE A LANECHANGE / NO LANECHANGE
        # --------------------------------------------------------------------------------------------------------------
        # idm acceleration if no lanechange is conducted
        ego_acceleration_no_lanechange = self.__calc_idm_acceleration(
            target_velocity=self.idm_parameters['v_0'],
            current_velocity=self.state.velocity,
            approaching_rate_to_leader=leader_approaching_rate,
            distance_to_leader=leader_distance,
        )

        # acceleration of followers if no lanechange is conducted
        # this is equal to the acceleration before a potential lane change
        if follower_id is not None:
            follower_acceleration_no_lanechange = self.__calc_idm_acceleration(
                target_velocity=follower_velocity,
                current_velocity=follower_velocity,
                approaching_rate_to_leader=follower_approaching_rate,
                distance_to_leader=-follower_distance,
            )
        else:
            follower_acceleration_no_lanechange = 0.0

        if left_follower_id is not None:
            if left_leader_id is not None:
                left_follower_acceleration_no_lanechange = self.__calc_idm_acceleration(
                    target_velocity=left_follower_velocity,
                    current_velocity=left_follower_velocity,
                    approaching_rate_to_leader=left_follower_approaching_rate
                    + left_leader_approaching_rate,
                    distance_to_leader=left_leader_distance - left_follower_distance,
                )
            else:
                left_follower_acceleration_no_lanechange = self.__calc_idm_acceleration(
                    target_velocity=left_follower_velocity,
                    current_velocity=left_follower_velocity,
                    approaching_rate_to_leader=None,
                    distance_to_leader=None,
                )
        else:
            left_follower_acceleration_no_lanechange = 0.0

        if right_follower_id is not None:
            if right_leader_id is not None:
                right_follower_acceleration_no_lanechange = (
                    self.__calc_idm_acceleration(
                        target_velocity=right_follower_velocity,
                        current_velocity=right_follower_velocity,
                        approaching_rate_to_leader=right_follower_approaching_rate
                        + right_leader_approaching_rate,
                        distance_to_leader=right_leader_distance
                        - right_follower_distance,
                    )
                )
            else:
                right_follower_acceleration_no_lanechange = (
                    self.__calc_idm_acceleration(
                        target_velocity=right_follower_velocity,
                        current_velocity=right_follower_velocity,
                        approaching_rate_to_leader=None,
                        distance_to_leader=None,
                    )
                )
        else:
            right_follower_acceleration_no_lanechange = 0.0

        # --------------------------------------------------------------------------------------------------------------
        # LANECHANGE TO LEFT
        # --------------------------------------------------------------------------------------------------------------
        # if left lanelet exists
        left_lanelet_id = self.__check_side_lanelet_id(side='left')

        if left_lanelet_id is not None:
            # new ego acceleration
            ego_acceleration_change_left = self.__calc_idm_acceleration(
                target_velocity=self.idm_parameters['v_0'],
                current_velocity=self.state.velocity,
                approaching_rate_to_leader=left_leader_approaching_rate,
                distance_to_leader=left_leader_distance,
            )

            # acceleration of new follower (if exists)
            if left_follower_id is not None:
                new_follower_acceleration_change_left = self.__calc_idm_acceleration(
                    target_velocity=left_follower_velocity,
                    current_velocity=left_follower_velocity,
                    approaching_rate_to_leader=left_follower_approaching_rate,
                    distance_to_leader=-left_follower_distance,
                )
            else:
                new_follower_acceleration_change_left = 0

            # acceleration of old follower (if exists)
            if follower_id is not None:
                if leader_id is not None:
                    old_follower_acceleration_change_left = (
                        self.__calc_idm_acceleration(
                            target_velocity=follower_velocity,
                            current_velocity=follower_velocity,
                            approaching_rate_to_leader=follower_approaching_rate
                            + leader_approaching_rate,
                            distance_to_leader=leader_distance - follower_distance,
                        )
                    )
                else:
                    old_follower_acceleration_change_left = (
                        self.__calc_idm_acceleration(
                            target_velocity=follower_velocity,
                            current_velocity=follower_velocity,
                            approaching_rate_to_leader=None,
                            distance_to_leader=None,
                        )
                    )
            else:
                old_follower_acceleration_change_left = 0

            total_acceleration_left_lanechange = (
                ego_acceleration_change_left
                - ego_acceleration_no_lanechange
                + self.mobil_parameters['p']
                * (
                    old_follower_acceleration_change_left
                    - follower_acceleration_no_lanechange
                    + new_follower_acceleration_change_left
                    - left_follower_acceleration_no_lanechange
                )
            )

        else:
            total_acceleration_left_lanechange = 0

        # --------------------------------------------------------------------------------------------------------------
        # LANECHANGE TO RIGHT
        # --------------------------------------------------------------------------------------------------------------
        # if right lanelet exists
        right_lanelet_id = self.__check_side_lanelet_id(side='right')

        if right_lanelet_id is not None:
            # new ego acceleration
            ego_acceleration_change_right = self.__calc_idm_acceleration(
                target_velocity=self.idm_parameters['v_0'],
                current_velocity=self.state.velocity,
                approaching_rate_to_leader=right_leader_approaching_rate,
                distance_to_leader=right_leader_distance,
            )

            # acceleration of new follower (if exists)
            if right_follower_id is not None:
                new_follower_acceleration_change_right = self.__calc_idm_acceleration(
                    target_velocity=right_follower_velocity,
                    current_velocity=right_follower_velocity,
                    approaching_rate_to_leader=right_follower_approaching_rate,
                    distance_to_leader=-right_follower_distance,
                )
            else:
                new_follower_acceleration_change_right = 0

            # acceleration of old follower (if exists)
            if follower_id is not None:
                if leader_id is not None:
                    old_follower_acceleration_change_right = (
                        self.__calc_idm_acceleration(
                            target_velocity=follower_velocity,
                            current_velocity=follower_velocity,
                            approaching_rate_to_leader=follower_approaching_rate
                            + leader_approaching_rate,
                            distance_to_leader=leader_distance - follower_distance,
                        )
                    )
                else:
                    old_follower_acceleration_change_right = (
                        self.__calc_idm_acceleration(
                            target_velocity=follower_velocity,
                            current_velocity=follower_velocity,
                            approaching_rate_to_leader=None,
                            distance_to_leader=None,
                        )
                    )
            else:
                old_follower_acceleration_change_right = 0

            total_acceleration_right_lanechange = (
                ego_acceleration_change_right
                - ego_acceleration_no_lanechange
                + self.mobil_parameters['p']
                * (
                    old_follower_acceleration_change_right
                    - follower_acceleration_no_lanechange
                    + new_follower_acceleration_change_right
                    - right_follower_acceleration_no_lanechange
                )
            )

        else:
            total_acceleration_right_lanechange = 0

        # --------------------------------------------------------------------------------------------------------------
        # LANECHANGE DECISION
        # --------------------------------------------------------------------------------------------------------------
        if (
            total_acceleration_left_lanechange > total_acceleration_right_lanechange
            and total_acceleration_left_lanechange > self.mobil_parameters['a_th']
        ):
            if (
                new_follower_acceleration_change_left
                >= -self.mobil_parameters['b_safe']
            ):
                # lane change to the left
                new_lanelet_id = left_lanelet_id
                projected_position = self.__project_position(lanelet_id=new_lanelet_id)
                acceleration = ego_acceleration_change_left
            else:
                # no lane change
                new_lanelet_id = self.current_lanelet_id
                projected_position = self.state.position
                acceleration = ego_acceleration_no_lanechange

        elif (
            total_acceleration_right_lanechange >= total_acceleration_left_lanechange
            and total_acceleration_right_lanechange > self.mobil_parameters['a_th']
        ):
            if (
                new_follower_acceleration_change_right
                >= -self.mobil_parameters['b_safe']
            ):
                # lane change to the right
                new_lanelet_id = right_lanelet_id
                projected_position = self.__project_position(lanelet_id=new_lanelet_id)
                acceleration = ego_acceleration_change_right
            else:
                # no lane change
                new_lanelet_id = self.current_lanelet_id
                projected_position = self.state.position
                acceleration = ego_acceleration_no_lanechange
        else:
            # no lane change
            new_lanelet_id = self.current_lanelet_id
            projected_position = self.state.position
            acceleration = ego_acceleration_no_lanechange

        # new velocity
        velocity = self.state.velocity + acceleration * delta_time

        # covered distance along the center line of the current lanelet
        ds = self.state.velocity * delta_time + 1 / 2 * acceleration * delta_time ** 2

        # approximate the center line of the new lanelet as a cubic spline
        new_lanelet_spline = lanelet2spline(
            lanelet=self.scenario.lanelet_network.find_lanelet_by_id(new_lanelet_id)
        )

        # calculate the new position (arc length) travelled along the spline
        s_new = new_lanelet_spline.get_min_arc_length(projected_position)[0] + ds

        # new position
        x, y = new_lanelet_spline.calc_position(s_new)
        position = np.array([x, y])

        # new orientation
        orientation = new_lanelet_spline.calc_yaw(s_new)

        # update the state
        self._state.position = position
        self._state.orientation = orientation
        self._state.velocity = velocity
        self._state.acceleration = acceleration

        # DEBUGGING
        if False:
            ######################################################################################
            # DEBUGGING
            plot_limits = get_plot_limits_from_scenario(scenario=self.scenario)
            plt.figure(figsize=(15, 8))

            draw_object(
                obj=self.scenario,
                plot_limits=plot_limits,
                draw_params={'time_begin': self.time_step},
            )

            # mark the ego vehicle
            draw_object(
                obj=self.scenario.obstacle_by_id(self.agent_id),
                plot_limits=plot_limits,
                draw_params={'time_begin': self.time_step, 'facecolor': 'r'},
            )

            # mark the leader vehicle
            if self.leader_id is not None:
                draw_object(
                    obj=self.scenario.obstacle_by_id(self.leader_id),
                    plot_limits=plot_limits,
                    draw_params={'time_begin': self.time_step, 'facecolor': 'g'},
                )

            # mark the following vehicle
            if self.follower_id is not None:
                draw_object(
                    obj=self.scenario.obstacle_by_id(self.follower_id),
                    plot_limits=plot_limits,
                    draw_params={'time_begin': self.time_step, 'facecolor': 'y'},
                )

            plt.title(
                'Time step: '
                + str(self.time_step)
                + '\n'
                + 'Ego ID: '
                + str(self.agent_id)
                + ' ('
                + str(self.state.velocity * 3.6)
                + 'km/h)'
                + '(red) \n'
                + 'Leader ID: '
                + str(self.leader_id)
                + ' (distance: '
                + str(self.distance_to_leader)
                + 'm)'
                + ' (green) \n'
                + 'Follower ID: '
                + str(self.follower_id)
                + ' (distance: '
                + str(self.distance_to_follower)
                + 'm)'
                + ' (yellow)'
            )

            # Obstacle IDs
            for dynamic_obstacle in self.scenario.dynamic_obstacles:
                try:
                    x = dynamic_obstacle.prediction.trajectory.state_list[
                        self.time_step
                    ].position[0]
                    y = dynamic_obstacle.prediction.trajectory.state_list[
                        self.time_step
                    ].position[1]
                    plt.text(x, y, str(dynamic_obstacle.obstacle_id), zorder=100)
                except Exception:
                    pass

            plt.text(
                40,
                20,
                'Follower ID: '
                + str(follower_id)
                + ' (distance: '
                + str(follower_distance)
                + 'm)'
                + '\n'
                + 'Left Follower ID: '
                + str(left_follower_id)
                + ' (distance: '
                + str(left_follower_distance)
                + 'm)'
                + '\n'
                + 'Right Follower ID: '
                + str(right_follower_id)
                + ' (distance: '
                + str(right_follower_distance)
                + 'm)'
                + '\n'
                + 'Leader ID: '
                + str(leader_id)
                + ' (distance: '
                + str(leader_distance)
                + 'm)'
                + '\n'
                + 'Left Leader ID: '
                + str(left_leader_id)
                + ' (distance: '
                + str(left_leader_distance)
                + 'm)'
                + '\n'
                + 'Right Leader ID: '
                + str(right_leader_id)
                + ' (distance: '
                + str(right_leader_distance)
                + 'm)',
            )

            plt.gca().set_aspect('equal')
            plt.show()
            ############################################################################################

    def __calc_idm_acceleration(
        self,
        target_velocity,
        current_velocity,
        approaching_rate_to_leader,
        distance_to_leader,
    ):
        """Get acceleration

        This method calculates the new acceleration depending on the leading vehicle and the desired velocity

        :param target_velocity: target velocity of the considered vehicle
        :param current_velocity: current velocity of the considered vehicle
        :param approaching_rate_to_leader: approaching rate of the considered vehicle to the current leading vehicle in the same lane
        :param distance_to_leader: distance between the current leading vehicle in the same lane and the considered vheicle
        :return: acceleration in m/s^2
        """
        # standstill
        if target_velocity == 0:
            if current_velocity > 0:
                return self.idm_parameters['a_min']
            else:
                return 0

        # free road term
        a_free = self.idm_parameters['a_max'] * (
            1
            - (current_velocity / self.idm_parameters['v_0'])
            ** self.idm_parameters['delta']
        )

        if approaching_rate_to_leader and distance_to_leader is not None:
            # interaction term
            a_int = (
                -self.idm_parameters['a_max']
                * (
                    (
                        self.idm_parameters['s_0']
                        + current_velocity * self.idm_parameters['T']
                    )
                    / distance_to_leader
                    + current_velocity
                    * approaching_rate_to_leader
                    / (
                        2
                        * np.sqrt(
                            self.idm_parameters['a_max'] * self.idm_parameters['b']
                        )
                        * distance_to_leader
                    )
                )
                ** 2
            )
        else:
            a_int = 0

        # disable going backwards
        if current_velocity <= 0 and (a_free + a_int) <= 0:
            return 0

        return max(a_free + a_int, self.idm_parameters['a_min'])

    def __get_all_follower_and_leader_info(self):
        """Get relevant information of all necessary leaders and followers

        Saves the parameters arclength and velocity for every leader and follower necessary
        to calculate IDM accelerations for the later use in MOBIL algorithm.

        :return: arclength and velocity of leaders and followers of ego lanelets, left and right lanelet
        """
        # save leader data
        (
            leader_id,
            leader_arclength,
            leader_velocity,
        ) = self.__get_leader_data_by_lanelet(lane='ego')
        if leader_id is None:
            leader_distance = None
            leader_approaching_rate = None
        else:
            leader_distance = leader_arclength - self.ego_arclength
            leader_approaching_rate = self.state.velocity - leader_velocity

        # save follower data
        (
            follower_id,
            follower_arclength,
            follower_velocity,
        ) = self.__get_follower_data_by_lanelet(lane='ego')
        if follower_id is None:
            follower_distance = None
            follower_approaching_rate = None
        else:
            follower_distance = follower_arclength - self.ego_arclength
            follower_approaching_rate = follower_velocity - self.state.velocity

        # save left leader data
        (
            left_leader_id,
            left_leader_arclength,
            left_leader_velocity,
        ) = self.__get_leader_data_by_lanelet(lane='left')
        if left_leader_id is None:
            left_leader_distance = None
            left_leader_approaching_rate = None
        else:
            left_leader_distance = left_leader_arclength - self.ego_arclength
            left_leader_approaching_rate = self.state.velocity - left_leader_velocity

        # save left follower data
        (
            left_follower_id,
            left_follower_arclength,
            left_follower_velocity,
        ) = self.__get_follower_data_by_lanelet(lane='left')
        if left_follower_id is None:
            left_follower_distance = None
            left_follower_approaching_rate = None
        else:
            left_follower_distance = left_follower_arclength - self.ego_arclength
            left_follower_approaching_rate = (
                left_follower_velocity - self.state.velocity
            )

        # save right leader data
        (
            right_leader_id,
            right_leader_arclength,
            right_leader_velocity,
        ) = self.__get_leader_data_by_lanelet(lane='right')
        if right_leader_id is None:
            right_leader_distance = None
            right_leader_approaching_rate = None
        else:
            right_leader_distance = right_leader_arclength - self.ego_arclength
            right_leader_approaching_rate = self.state.velocity - right_leader_velocity

        # save right follower data
        (
            right_follower_id,
            right_follower_arclength,
            right_follower_velocity,
        ) = self.__get_follower_data_by_lanelet(lane='right')
        if right_follower_id is None:
            right_follower_distance = None
            right_follower_approaching_rate = None
        else:
            right_follower_distance = right_follower_arclength - self.ego_arclength
            right_follower_approaching_rate = (
                right_follower_velocity - self.state.velocity
            )

        return (
            leader_id,
            leader_arclength,
            leader_distance,
            leader_velocity,
            leader_approaching_rate,
            follower_id,
            follower_arclength,
            follower_distance,
            follower_velocity,
            follower_approaching_rate,
            left_leader_id,
            left_leader_arclength,
            left_leader_distance,
            left_leader_velocity,
            left_leader_approaching_rate,
            left_follower_id,
            left_follower_arclength,
            left_follower_distance,
            left_follower_velocity,
            left_follower_approaching_rate,
            right_leader_id,
            right_leader_arclength,
            right_leader_distance,
            right_leader_velocity,
            right_leader_approaching_rate,
            right_follower_id,
            right_follower_arclength,
            right_follower_distance,
            right_follower_velocity,
            right_follower_approaching_rate,
        )

    def __get_leader_data_by_lanelet(self, lane: str):
        """Get data for leader vehicle

        Gives information about the parameters arclength (distance) and velocity of a leading vehicle.
        Arclength and velocity are calculated through the delta between the ego vehicle state and
        the leading vehicle, of which approaching rate and distance from the ego vehicle are known.

        :param lane: str which specifies on which lanelet to look for a leader vehicle ("ego" / "left" / "right" )

        :return: arclength in m, velocity in m/s
        """
        lanelet_id = self.__check_side_lanelet_id(side=lane)

        if lanelet_id is not None:
            (
                leader_id,
                distance_to_leader,
                approaching_rate_to_leader,
            ) = get_leader_on_lanelet(
                scenario=self.scenario,
                ego_obstacle_id=self.agent_id,
                leader_lanelet_id=lanelet_id,
                time_step=self.time_step,
            )

            if leader_id is not None:
                # save future leader velocity
                leader_velocity = self.state.velocity - approaching_rate_to_leader

                # save future leader position
                leader_arclength = self.ego_arclength + distance_to_leader
            else:
                leader_id, leader_velocity, leader_arclength = None, None, None

        else:
            leader_id, leader_velocity, leader_arclength = None, None, None

        return leader_id, leader_arclength, leader_velocity

    def __get_follower_data_by_lanelet(self, lane: str):
        """Get data for sidelane follower

        Gives information about the parameters arclength (distance) and velocity of a following vehicle.
        Arclength and velocity are calculated through the delta between the ego vehicle state and
        the follower vehicle, of which approaching rate and distance from the ego vehicle are known.

        :param lane: str which specifies on which lanelet to look for a follower vehicle ("ego" / "left" / "right" )

        :return: arclength in m, velocity in m/s
        """

        lanelet_id = self.__check_side_lanelet_id(side=lane)

        if lanelet_id is not None:
            (
                follower_id,
                distance_to_follower,
                approaching_rate_of_follower,
            ) = get_follower_on_lanelet(
                scenario=self.scenario,
                ego_obstacle_id=self.agent_id,
                follower_lanelet_id=lanelet_id,
                time_step=self.time_step,
            )

            if follower_id is not None:
                # save future follower velocity
                follower_velocity = self.state.velocity + approaching_rate_of_follower

                # save future follower position
                follower_arclength = self.ego_arclength + distance_to_follower
            else:
                follower_id, follower_velocity, follower_arclength = None, None, None

        else:
            follower_id, follower_velocity, follower_arclength = None, None, None

        return follower_id, follower_arclength, follower_velocity

    def __check_side_lanelet_id(self, side: str):
        """Get lanelet id from a lanelet to either side of the current lanelet"""
        if side == 'left':
            return get_left_lanelet(
                scenario=self.scenario,
                ego_obstacle_id=self.agent_id,
                time_step=self.time_step,
            )
        elif side == 'right':
            return get_right_lanelet(
                scenario=self.scenario,
                ego_obstacle_id=self.agent_id,
                time_step=self.time_step,
            )
        elif side == 'ego':
            return self.current_lanelet_id
        else:
            return None

    def __project_position(self, lanelet_id):

        lanelet = self.scenario.lanelet_network.find_lanelet_by_id(lanelet_id)
        lanelet_spline = lanelet2spline(lanelet=lanelet)
        projected_ego_arclength = lanelet_spline.get_min_arc_length(
            self.state.position
        )[0]

        projected_x, projected_y = lanelet_spline.calc_position(projected_ego_arclength)
        projected_position = np.array([projected_x, projected_y])

        return projected_position

    @property
    def idm_parameters(self):
        """IDM parameters"""
        return self.__idm_parameters

    @property
    def mobil_parameters(self):
        """MOBIL parameters"""
        return self.__mobil_parameters


# EOF
