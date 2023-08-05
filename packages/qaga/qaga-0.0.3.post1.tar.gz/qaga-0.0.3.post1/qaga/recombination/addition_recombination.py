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


from dimod.sampleset import SampleSet, concatenate

from .recombination import Recombinator, Recombination
from ..problem import ProblemType


class AdditionRecombinator(Recombinator[ProblemType]):
    """Adding the old population after recombination.

    An arbitrary `Recombinator[ProblemType]` is injected, that performs
    recombination. Its result is then merged with the input population.

    Args:
        internal (Recombinator[ProblemType]): Determines the recombination that
            is done first, before original individuals are added.

    """
    def __init__(self, internal: Recombinator[ProblemType]):
        self._internal = internal

    def recombine(self, population: SampleSet) -> SampleSet:
        """Performs internal recombination on the current population and merge
        it with the result.

        Returns:
            A `dimod.SampleSet` that preserves the guarantees of `internal`. In
            addition, it contains any element of `population` and no duplicates.

        """
        return concatenate([population, self._internal.recombine(population)]).aggregate()


class AdditionRecombination(Recombination[ProblemType]):
    """Configuration of a recombination reusing the old population.

    An arbitrary `Recombination[ProblemType]` is used to perform recombination,
    whose individuals are then added the input population.

    It is the easiest way to achieve monotonicity for any recombination
    procedure.

    Args:
        internal (Recombination[ProblemType]): Configures the recombination that
            is done first, before original individuals are added.

    """
    def __init__(self, internal: Recombination[ProblemType]):
        self._internal = internal

    def initialise(self, problem: ProblemType) -> Recombinator[ProblemType]:
        """Configures a `AdditionRecombination[ProblemType]` with the respective
        internal recombination.

        Args:
            problem (ProblemType): A concrete problem instance,
                that is used to configure the internal recombination.

        """
        return AdditionRecombinator[ProblemType](self._internal.initialise(problem))
