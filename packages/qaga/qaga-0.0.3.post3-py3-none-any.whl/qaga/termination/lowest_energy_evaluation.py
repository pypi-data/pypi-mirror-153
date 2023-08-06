# Copyright (C) 2022 PlanQK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from dimod import SampleSet
from typing import Callable

from .termination import Terminator, Termination
from ..problem import ProblemType


class LowestEnergyTerminator(Terminator[ProblemType]):
    """Terminating an algorithm by checking a predicate about the current
    populations's lowest energy.

    Args:
        predicate (Callable[[float], bool]): A predicate to check about the
            lowest energy.

    """
    def __init__(self, predicate: Callable[[float], bool]):
        self._predicate = predicate

    def should_terminate(self, population: SampleSet) -> bool:
        """Checks if `predicate` holds for for the current population's lowest
        energy.

        Returns:
            `True` to terminate if the lowest energy satisfies `predicate`;
            False` to proceed if not.

        """
        return self._predicate(population.first.energy)


class LowestEnergyTermination(Termination[ProblemType]):
    """Configuration on after how many generations an algorithm terminates.

    Offers rudimentary support to terminate early due to sufficient population
    quality.

    Args:
        predicate (Callable[[float], bool]): A predicate to check about the
            lowest energy. One must be aware, that those pure values are
            unintuitive and highly problem dependent, i.e. it is impossible to
            estimate what are good values.

    """
    def __init__(self, predicate: Callable[[float], bool]):
        self._predicate = predicate

    def initialise(self, problem: ProblemType) -> Terminator[ProblemType]:
        """Configurates a `LowestEnergyTerminator[ProblemType]` with the respective predicate.

        Returns:
            A `LowestEnergyTerminator[ProblemType]` checking the respective predicate.

        """
        return LowestEnergyTerminator[ProblemType](self._predicate)
