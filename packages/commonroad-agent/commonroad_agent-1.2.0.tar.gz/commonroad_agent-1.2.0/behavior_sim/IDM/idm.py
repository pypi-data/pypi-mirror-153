"""IDM behavior model for CommonRoad agents.

Authors: Matthias Rowold <matthias.rowold@tum.de> & Annika Kirner
"""


from commonroad.scenario.scenario import Scenario
from commonroad.visualization.draw_dispatch_cr import draw_object
from commonroad_helper_functions.spacial import lanelet2spline
from commonroad_helper_functions.visualization import get_plot_limits_from_scenario
import numpy as np
from matplotlib import pyplot as plt
import os
import sys

module_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(module_path)

from agent_sim.agent import Agent


class IDMAgent(Agent):
    """IDM Agent.

    Class to model IDM behavior
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
            'a_max': 3,
            'a_min': -4,
            'b': 1.5,
            'delta': 4,
        },
    ):
        """Initialize an IDM agent.

        :param scenario: commonroad scenario
        :param agent_id: ID of the IDM agent: should be equal to the commonroad dynamic obstacle ID
        :param enable_logging: True for logging
        :param log_path: path for logging files
        :param debug_step: True for figure with current scenario in every time step
        :param idm_parameters: IDM parameters
        """

        # initialize the parent class
        super().__init__(
            scenario=scenario,
            agent_id=agent_id,
            enable_logging=enable_logging,
            log_path=log_path,
            debug_step=debug_step,
        )

        # idm parameters
        self.__idm_parameters = idm_parameters

    def _step_agent(self, delta_time: float):
        """IDM step.

        This methods overloads the basic step method. It calculates the new state according to the IDM behavior.
        An acceleration depending on the leading vehicle is integrated twice to obtain the new position.

        :param delta_time: time difference to the previous step
        """

        if not self._valid:
            return

        # new acceleration
        acceleration = self.__get_acceleration()

        # new velocity
        velocity = self.state.velocity + acceleration * delta_time

        # covered distance along the center line of the current lanelet
        ds = self.state.velocity * delta_time + 1 / 2 * acceleration * delta_time ** 2

        # approximate the center line of the current lanelet as a cubic spline
        ego_lanelet_spline = lanelet2spline(
            lanelet=self.scenario.lanelet_network.find_lanelet_by_id(
                self.current_lanelet_id
            )
        )

        # calculate the new position (arc length) travelled along the spline
        s_new = ego_lanelet_spline.get_min_arc_length(self.state.position)[0] + ds

        # new position
        x, y = ego_lanelet_spline.calc_position(s_new)
        position = np.array([x, y])

        # new orientation
        orientation = ego_lanelet_spline.calc_yaw(s_new)

        # update the state
        self._state.position = position
        self._state.orientation = orientation
        self._state.velocity = velocity
        self._state.acceleration = acceleration

    def __get_acceleration(self):
        """Get acceleration.

        This method calculates the new acceleration depending on the leading vehicle and the desired velocity

        :return: acceleration in m/s^2
        """
        # standstill
        if self.idm_parameters['v_0'] == 0:
            if self._state.velocity > 0:
                return self.idm_parameters['a_min']
            else:
                return 0

        # free road term
        a_free = self.idm_parameters['a_max'] * (
            1
            - (self.state.velocity / self.idm_parameters['v_0'])
            ** self.idm_parameters['delta']
        )

        # interaction term
        if self.leader_id is not None:
            a_int = (
                -self.idm_parameters['a_max']
                * (
                    (
                        self.idm_parameters['s_0']
                        + self.state.velocity * self.idm_parameters['T']
                    )
                    / self.distance_to_leader
                    + self.state.velocity
                    * self.approaching_rate_to_leader
                    / (
                        2
                        * np.sqrt(
                            self.idm_parameters['a_max'] * self.idm_parameters['b']
                        )
                        * self.distance_to_leader
                    )
                )
                ** 2
            )
        else:
            a_int = 0

        # disable going backwards
        if self.state.velocity <= 0 and (a_free + a_int) <= 0:
            return 0

        return max(a_free + a_int, self.idm_parameters['a_min'])

    ####################################################################################################################
    # PROPERTIES #######################################################################################################
    ####################################################################################################################

    @property
    def idm_parameters(self):
        """IDM parameters."""
        return self.__idm_parameters


# EOF
