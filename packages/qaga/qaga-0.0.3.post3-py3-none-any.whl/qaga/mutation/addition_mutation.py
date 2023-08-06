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

from .mutation import Mutator, Mutation
from ..problem import ProblemType


class AdditionMutator(Mutator[ProblemType]):
    """Adding the old population after mutation.

    An arbitrary `Mutator[ProblemType]` is injected, that performs
    mutation. Its result is then merged with the input population.

    Args:
        internal (Mutator[ProblemType]): Determines the mutation that
            is done first, before the original individuals are added.

    """
    def __init__(self, internal: Mutator[ProblemType]):
        self._internal = internal

    def mutate(self, population: SampleSet) -> SampleSet:
        new = self._internal.mutate(population)
        return concatenate((population, new)).aggregate()


class AdditionMutation(Mutation[ProblemType]):
    """Configuration of a mutation reusing the old population.

    An arbitrary `Mutation[ProblemType]` is used to perform mutation,
    whose individuals are then added the input population.

    It is the easiest way to achieve monotonicity for any mutation
    procedure.

    Args:
        internal (Mutation[ProblemType]): Configures the mutation that
            is done first, before the original individuals are added.

    """
    def __init__(self, internal: Mutation[ProblemType]):
        self._internal = internal


    def initialise(self, problem: ProblemType) -> Mutator[ProblemType]:
        return AdditionMutator[ProblemType](self._internal.initialise(problem))
