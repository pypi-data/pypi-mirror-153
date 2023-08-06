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

from dimod import SampleSet, BinaryQuadraticModel, Sampler

from .startup import Startup
from ..problem import ProblemType


class SamplingStartup(Startup[ProblemType]):
    """Population creation by sampling.

    If the starting population of a genetic algorithm is created by means of a
    sampler performing global search, it is guaranteed that the first performs
    statistically at least as good as the latter because the population quality
    must not decrease per generation.

    Args:
        desired_population_size (int): Positive, maximal number of solutions to
            find.

        sampler (dimod.Sampler): A sampler that can minimise a
            `dimod.BinaryQuadraticModel`. It is advised to perform a global
            search.

    """
    def __init__(self, desired_population_size: int, sampler: Sampler):
        assert desired_population_size > 0
        self._desired_population_size = desired_population_size
        self._sampler = sampler

    def startup(self, problem: ProblemType) -> SampleSet:
        """Creates a population by minimising the given problem.

        Args:
            problem (ProblemType): The problem that is optimised
                to create a population.

        Returns:
            A `dimod.SampleSet` that contains at most `desired_population_size`,
            distinct individuals. Note there is a high probability of small
            sizes because some solutions might be found multiple times by the
            sampler. Variable type and number of qubit coincide with `problem.bqm`.

        """
        return self._sampler.sample(
            problem.bqm,
            num_reads=self._desired_population_size
        ).aggregate() # Remove duplicates
