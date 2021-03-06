import simpy
from random import randint
from elevator_playground.elevators import Elevator
from elevator_playground.utils import print_status, rand_call
from abc import ABC, abstractmethod


class Building(ABC):
    """A building containing elevators that handles generated calls."""
    def __init__(self, num_floors, num_elevators):
        """Create a building with specified number of floors and elevators.

        env            -- simpy.Environment instance that runs the simulation
        call generator -- simpy process for generating calls
        call assigner  -- simpy process for assigning calls
        call queue     -- queue for holding generated calls yet to be assigned
        call history   -- list of all calls that have been generated
        num floors     -- number of floors in building
        num elevators  -- number of elevators in building
        elevators      -- list of elevator instances contained in building
        service ranges -- dictionary mapping each elevator to the floors that
                          they are able to access
        """
        self.env = simpy.Environment()
        self.call_generator = self.env.process(self._generate_calls())
        self.call_assigner = self.env.process(self._assign_calls())
        self.call_queue = simpy.Store(self.env)
        self.call_history = []
        self.num_floors = num_floors
        self.num_elevators = num_elevators
        self.elevators = self._init_elevators(num_elevators)
        self.service_ranges = self._init_service_ranges()

    def _init_elevators(self, num_elevators):
        """Create specified number of elevators and return them as a list."""
        elevators = []
        for i in range(num_elevators):
            elevators.append(Elevator(self, self.env, i))
        return elevators

    def _init_service_ranges(self):
        """Set service range for each elevator."""
        ranges = {}
        for i in range(self.num_elevators):
            lower_bound = 1
            upper_bound = self.num_floors
            service_range = (lower_bound, upper_bound)
            ranges[self.elevators[i]] = service_range
            self.elevators[i].set_service_range(lower_bound, upper_bound)
        return ranges

    @abstractmethod
    def _generate_calls(self):
        """Periodically generate a call and place it into the call queue."""
        pass

    @abstractmethod
    def _generate_single_call(self):
        """Generate a random call."""
        pass

    @abstractmethod
    def _assign_calls(self):
        """Periodically check the call queue for any calls and assign them."""
        pass

    @abstractmethod
    def _select_elevator(self, call):
        """Judiciously select an elevator to handle a call."""
        pass


class BasicBuilding(Building):
    """A building that assigns calls randomly."""

    def _generate_calls(self):
        print_status(self.env.now, f"Building has started generating calls...")
        while True:
            yield self.env.timeout(100)
            call = self._generate_single_call()
            self.call_queue.put(call)
            self.call_history.append(call)

    def _generate_single_call(self):
        """Return a single, random call."""
        call = rand_call(self.env.now, self.num_floors)
        print_status(self.env.now, f"[Generate] call {call.id}:"
                                   f" floor {call.source} to {call.dest}")
        return call

    def _assign_calls(self):
        """Periodically check the call queue for any calls and assign them."""
        print_status(self.env.now, "Building has started assigning calls...")
        while True:
            call = yield self.call_queue.get()
            elevator = self._select_elevator(call)
            elevator.enqueue(call)

    def _select_elevator(self, call):
        """Select an elevator at random to handle the given call."""
        selected = self.elevators[randint(0, self.num_elevators - 1)]
        print_status(self.env.now,
                     f"[Select] call {call.id}: Elevator {selected.id}")
        return selected


class BasicSectorBuilding:
    pass


class DynamicLoadBalancingBuilding:
    pass


class DeepReinforcementLearningBuilding:
    pass
