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
from copy import deepcopy

from .startup import Startup
from ..problem import ProblemType

class WarmStartup(Startup[ProblemType]):
    """Population creation by reusing an already existing one.

    If one has already a set of solutions with sufficient quality, a genetic
    algorithm can use it as initial population. This guarantees that the final
    one is at least as good as the initial one, however, there is the chance
    even better solutions are found.

    Args:
        population (dimod.SampleSet): A non-empty population to start with.

    """
    def __init__(self, population: SampleSet):
        assert len(population) > 0
        self._population = population

    def startup(self, problem: ProblemType) -> SampleSet:
        """Reuses the deposited population.

        Args:
            problem (ProblemType): The problem for which the
                deposited population is reused. Variable type and amount of
                qubits must fit.

        Returns:
            A `dimod.SampleSet` that is a deep copy of the deposited population.
            No augmentations are done.

        """
        assert self._population.variables == problem.bqm.variables
        assert self._population.vartype == problem.bqm.vartype

        return deepcopy(self._population)
