"""Agent class for Commonroad multi-agent simulation.

Author: Matthias Rowold <matthias.rowold@tum.de>
"""

from commonroad.scenario.scenario import Scenario
from commonroad.prediction.prediction import Occupancy
from commonroad.scenario.trajectory import State
from commonroad.visualization.draw_dispatch_cr import draw_object
from copy import deepcopy
from matplotlib import pyplot as plt
from commonroad_helper_functions.logger import ObjectStateLogger
from commonroad_helper_functions.visualization import get_plot_limits_from_scenario
from commonroad_helper_functions.spacial import (
    get_leader_on_lanelet,
    get_follower_on_lanelet,
)


class Agent(object):
    """Agent class for CommonRoad.

    Class to represent agents in a scenario.
    """

    def __init__(
        self,
        scenario: Scenario,
        agent_id: int,
        enable_logging: bool = True,
        log_path: str = '/log',
        debug_step: bool = False,
    ):
        """Initialize an agent.

        :param scenario: commonroad scenario
        :param agent_id: ID of the agent: should be equal to the commonroad dynamic obstacle ID
        :param enable_logging: True for logging
        :param log_path: path for logging files
        :param debug_step: True for figure with current scenario in every time step
        """

        # commonroad scenario in which the agent is moving
        self.__scenario = scenario

        # agent ID
        self.__agent_id = agent_id

        # agent shape
        self.__agent_shape = self.scenario.obstacle_by_id(self.agent_id).obstacle_shape

        # initial state
        self.__initial_state = self.scenario.obstacle_by_id(self.agent_id).initial_state

        # current state
        self._state = deepcopy(self.__initial_state)

        # predefined state_list
        self._predefined_state_list = self.scenario.obstacle_by_id(
            self.agent_id
        ).prediction.trajectory.state_list

        # simulation time step size
        self.__dt = scenario.dt
        # current simulation time step
        self._time_step = 0
        # current simulation time
        self.__time = 0.0

        # validity
        self._valid = True

        # initial lanelet
        self.__current_lanelet_id = None
        self.update_current_lanelet()

        # initial leader
        self.__leader_id = (
            self.__distance_to_leader
        ) = self.__approaching_rate_to_leader = None
        self.update_leader()

        # initial follower
        self.__follower_id = (
            self.__distance_to_follower
        ) = self.__approaching_rate_of_follower = None
        self.update_follower()

        # debugging
        self.__debug_step = debug_step

        # debugging figure
        if self.debug_step:
            self.plot_debug()

        # logging
        self.__logging_enabled = enable_logging
        self.__log_path = log_path

        if self.logging_enabled:
            # create logging object
            self._agent_state_logger = ObjectStateLogger(
                log_path=self.log_path, object_id=self.agent_id
            )
            # initialize the logger for writing
            self._agent_state_logger.initialize()

            # log initial state
            self._log_agent_state()

    def step(self, scenario: Scenario):
        """Main step function.

        This step method is called for every agent moving in the scenario.
        It is a wrapper for the agent-type depending actual step method "_step_agent()" that updates the state.
        "_step_agent()" must be overloaded by inheriting classes that implement a certain agent behavior or plan trajectories.

        :param scenario: current commonroad scenario
        """

        # get current commonroad scenario
        self.__scenario = scenario

        # update lanelet
        self.update_current_lanelet()

        # if the agent is inside the lanelet network and valid
        if self.current_lanelet_id is not None and self._valid:
            # update leader
            self.update_leader()
            # update follower
            self.update_follower()

        else:
            self._valid = False

        # debugging figure
        if self.debug_step:
            self.plot_debug()

        # save the current time step temporarily
        time_step_temp = self.time_step

        # update the state depending on the behavior or planned trajectory
        self._step_agent(delta_time=self.scenario.dt)

        # increase the time step by one (this ensures that the time step is not changed by _step_agent())
        self._time_step = time_step_temp + 1

        # ensure correct time step of the new state
        self._state.time_step = self.time_step

        # simulation time
        self.__time = self.time_step * self.dt

        # log the current state
        self._log_agent_state()

    def set_to_time_step(self, time_step: int):
        """Set to time step.

        This function sets an agent to the specified time step.
        """
        self._time_step = time_step
        self.update_current_lanelet()
        if self.current_lanelet_id is not None:
            # update leader
            self.update_leader()
            # update follower
            self.update_follower()

    def _log_agent_state(self):
        """Log agent state.

        Write the current state to the logging file
        """
        if self.logging_enabled:
            self._agent_state_logger.log_state(state=self.state, time=self.time)

    def _step_agent(self, delta_time):
        """Agent step function.

        This method directly changes the state of the agent.
        It must be overloaded to enforce a desired behavior of the agent.
        The is the basic behavior prescribed by the predefined trajectories in the commonroad scenario.

        :param delta_time: time difference to the previous step (may be needed for integration)
        """
        if self.time_step < len(self._predefined_state_list):
            # take the state defined by the scenario
            self._state = self._predefined_state_list[self.time_step]
            self._state.acceleration = 0.0
        else:
            self._valid = False

    def update_leader(self):
        """Update leader.

        This function updates the current leader, distance to it and the approaching rate.
        """
        (
            self.__leader_id,
            self.__distance_to_leader,
            self.__approaching_rate_to_leader,
        ) = self.__get_leader_commonroad()

    def update_follower(self):
        """Update follower.

        This function updates the current follower, distance to it and the approaching rate.
        """
        (
            self.__follower_id,
            self.__distance_to_follower,
            self.__approaching_rate_of_follower,
        ) = self.__get_follower_commonroad()

    def update_current_lanelet(self):
        """Update current lanelet.

        This function updates the ID current lanelet.
        """
        if (
            len(
                self.scenario.lanelet_network.find_lanelet_by_position(
                    [self.state.position]
                )[0]
            )
            > 0
        ):
            self.__current_lanelet_id = (
                self.scenario.lanelet_network.find_lanelet_by_position(
                    [self.state.position]
                )[0][0]
            )
        else:
            self.__current_lanelet_id = None

    def plot_debug(self):
        """Debug plot."""
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
            + ' (red) \n'
            + 'Leader ID: '
            + str(self.leader_id)
            + ' (green) \n'
            + 'Follower ID: '
            + str(self.follower_id)
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
            except ValueError:
                pass

        plt.gca().set_aspect('equal')
        plt.show()

    def __get_leader_commonroad(self):
        """Get leader commonroad.

        Identify the leader on the current lanelet based on the current commonroad scenario

        :return: obstacle id of the next leading vehicle, distance to the leader and approaching rate
        """
        return get_leader_on_lanelet(
            scenario=self.scenario,
            ego_obstacle_id=self.agent_id,
            leader_lanelet_id=self.current_lanelet_id,
            time_step=self.time_step,
        )

    def __get_follower_commonroad(self):
        """Get follower commonroad.

        Identify the follower on the current lanelet based on the current commonroad scenario

        :return: obstacle id of the next following vehicle, distance to the follower and approaching rate
        """
        return get_follower_on_lanelet(
            scenario=self.scenario,
            ego_obstacle_id=self.agent_id,
            follower_lanelet_id=self.current_lanelet_id,
            time_step=self.time_step,
        )

    ####################################################################################################################
    # PROPERTIES #######################################################################################################
    ####################################################################################################################

    @property
    def scenario(self):
        """Commonroad scenario."""
        return self.__scenario

    @property
    def dt(self):
        """Time step size of the senario."""
        return self.__dt

    @property
    def agent_id(self):
        """ID of the agent."""
        return self.__agent_id

    @property
    def agent_shape(self):
        """Shape of the agent."""
        return self.__agent_shape

    @property
    def time_step(self):
        """Current time step."""
        return self._time_step

    @property
    def time(self):
        """Current time."""
        return self.__time

    @property
    def state(self):
        """State of the agent."""
        return self._state

    @property
    def initial_state(self):
        """Initial state of the agent."""
        return self.__initial_state

    @property
    def logging_enabled(self):
        """Logging enabled."""
        return self.__logging_enabled

    @property
    def log_path(self):
        """Path for logging files."""
        return self.__log_path

    @property
    def current_lanelet_id(self):
        """Current lanelet."""
        return self.__current_lanelet_id

    @property
    def debug_step(self):
        """Debug plot after every step."""
        return self.__debug_step

    @property
    def leader_id(self):
        """ID of the current leader on the same lanelet."""
        return self.__leader_id

    @property
    def distance_to_leader(self):
        """Distance to the current leader on the same lanelet."""
        return self.__distance_to_leader

    @property
    def approaching_rate_to_leader(self):
        """Approaching rate to the current leader on the same lanelet."""
        return self.__approaching_rate_to_leader

    @property
    def follower_id(self):
        """ID of the current follower on the same lanelet."""
        return self.__follower_id

    @property
    def distance_to_follower(self):
        """Distance to the current follower on the same lanelet."""
        return self.__distance_to_follower

    @property
    def approaching_rate_of_follower(self):
        """Approaching rate of the current follower on the same lanelet."""
        return self.__approaching_rate_of_follower


def clean_scenario(scenario: Scenario, agent_list: list):
    """Clean scenario.

    This functions cleans the scenario from specified agents.
    All predefined trajectories and assignments to lanelets for the agents in the list of agents are removed (except for the initial state)
    Other dynamic obstacles with IDs that are not equal to any of the agents remain.

    :param scenario: commonroad scenario
    :param agent_list: list of considered agents
    :return: new scenario with cleaned trajectories and lanelet assignments
    """
    for agent in agent_list:
        dynamic_obstacle = scenario.obstacle_by_id(agent.agent_id)
        dynamic_obstacle.prediction.trajectory.state_list = [
            dynamic_obstacle.initial_state
        ]
        # dynamic_obstacle.prediction.occupancy_set = []  # TODO: Workaround - this raises an error with commonroad io 2020.3
        dynamic_obstacle.prediction.center_lanelet_assignment = {}
        dynamic_obstacle.prediction.shape_lanelet_assignment = {}

        for lanelet in scenario.lanelet_network.lanelets:
            for t in range(1, len(agent._predefined_state_list) + 1):
                if lanelet.dynamic_obstacles_on_lanelet.get(t) is not None:
                    lanelet.dynamic_obstacles_on_lanelet.get(t).discard(agent.agent_id)

    return scenario


def update_scenario(scenario: Scenario, agent_list: list):
    """Update scenario.

    This function updates the scenario and should be called after every simulated time step.
    The new states of the specified agents are appended to the trajectories in the commonroad scenario and assigned to
    the lanelets for the corresponding time step.

    :param scenario: commonroad scenario
    :param agent_list: list of considered agents
    :return: updated scenario
    """
    for agent in agent_list:
        # create a new commonroad state
        state = State(
            position=agent.state.position,
            orientation=agent.state.orientation,
            velocity=agent.state.velocity,
            acceleration=agent.state.acceleration,
            time_step=agent.time_step,
        )

        # calculate the occupancy for the new state
        occupied_region = agent.agent_shape.rotate_translate_local(
            agent.state.position, agent.state.orientation
        )
        occupancy = Occupancy(agent.time_step, occupied_region)

        if agent.time_step == 0:
            # initial state already in scenario
            pass
        elif agent.time_step == 1:
            # add occupancy and state list
            scenario.obstacle_by_id(
                agent.agent_id
            ).prediction.trajectory.state_list = [state]
            scenario.obstacle_by_id(agent.agent_id).prediction.occupancy_set = [
                occupancy
            ]
        elif agent.time_step > 1:
            # append the new state
            scenario.obstacle_by_id(
                agent.agent_id
            ).prediction.trajectory.state_list.append(state)
            # append the new occupancy
            scenario.obstacle_by_id(agent.agent_id).prediction.occupancy_set.append(
                occupancy
            )

        # lanelet occupancy
        if agent.current_lanelet_id is not None:
            if (
                scenario.lanelet_network.find_lanelet_by_id(
                    agent.current_lanelet_id
                ).dynamic_obstacles_on_lanelet.get(agent.time_step)
                is None
            ):
                scenario.lanelet_network.find_lanelet_by_id(
                    agent.current_lanelet_id
                ).dynamic_obstacles_on_lanelet[agent.time_step] = set()
            scenario.lanelet_network.find_lanelet_by_id(
                agent.current_lanelet_id
            ).dynamic_obstacles_on_lanelet[agent.time_step].add(agent.agent_id)

    return scenario


# EOF
