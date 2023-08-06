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


class Mutator(Generic[ProblemType], ABC):
    """An interface for improving individuals.

    """
    @abstractmethod
    def mutate(self, population: SampleSet) -> SampleSet:
        """
        Improves individuals of the calling algorithm's current population.

        Implementations of this interface must ensure that in the result population no individual appears twice.
        Moreover, the best individual of the new population must be at least as good as the best one of the old population.

        :param population: The calling algorithm's current population.
        """
        pass


class Mutation(Generic[ProblemType], ABC):
    """Interface to configure mutation procedure of a genetic algorithm.

    It determines how solution candidates are improved individually, often by
    some local search.

    """

    @abstractmethod
    def initialise(self, problem: ProblemType) -> Mutator[ProblemType]:
        """Problem-specific configuration of mutation.

        Args:
            problem (ProblemType): A concrete problem instance,
                for which a bespoke mutation can be prepared.

        Returns:
            A `Mutator[ProblemType]` implementation.
        """
        pass
