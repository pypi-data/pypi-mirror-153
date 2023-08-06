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


class Recombinator(Generic[ProblemType], ABC):
    """An interface for combining individuals.

    """
    @abstractmethod
    def recombine(self, population: SampleSet) -> SampleSet:
        """Combines individuals to create a new population.

        Args: population (dimod.SampleSet): Nonempty population from which
            individuals are chosen to recombine.

        Returns:
            A nonempty `dimod.SampleSet`.

        """
        pass


class Recombination(Generic[ProblemType], ABC):
    """Interface to configure recombination procedure of a genetic algorithm.

    It determines how individuals are combined to create new improved ones.

    """
    @abstractmethod
    def initialise(self, problem: ProblemType) -> Recombinator[ProblemType]:
        """Problem-specific configuration of recombination.

        Args:
            problem (ProblemType): A concrete problem instance,
                for which a bespoke recombination can be prepared.

        Returns:
            A `Recombinator[ProblemType]` implementation.
        """
        pass
