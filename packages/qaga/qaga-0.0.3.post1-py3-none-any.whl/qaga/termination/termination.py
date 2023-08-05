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

from abc import ABC, abstractmethod
from typing import Generic

from dimod import SampleSet
from ..problem import ProblemType


class Terminator(Generic[ProblemType], ABC):
    """Interface for terminating an algorithm.

    """
    @abstractmethod
    def should_terminate(self, population: SampleSet) -> bool:
        """Checks termination condition for the current population.

        Returns:
            `True` to terminate, `False` to proceed.

        """
        pass


class Termination(Generic[ProblemType], ABC):
    """Interface to configure termination of an algorithm.
    """

    @abstractmethod
    def initialise(self, problem: ProblemType) -> Terminator[ProblemType]:
        """Problem-specific configuration of termination.

        Args:
            problem (Problem): A concrete problem instance, for which a
                bespoke termination condition can be prepared.

        Returns:
            A `Terminator[ProblemType]` implementation.

        """
        pass
